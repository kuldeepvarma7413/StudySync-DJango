from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from base.models import Courses, files ,Syllabus , subscribers , Profile
from .forms import userForm , PasswordUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Report , User_Email_verification, cafiles
from django.urls import reverse
from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
import random , smtplib , email.message , uuid
from django.conf import settings
from platformdirs import user_runtime_dir
from django.core.mail import EmailMessage , send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime , timedelta
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.core.files.base import ContentFile
from django.db import IntegrityError , transaction
from PyPDF2 import PdfFileMerger , PdfMerger
from django.core.files.uploadedfile import InMemoryUploadedFile , TemporaryUploadedFile
from datetime import date, datetime
from django.forms.models import model_to_dict
from subprocess import TimeoutExpired
from io import BytesIO
from PIL import Image
from io import StringIO
import img2pdf
import re , os , sys , contextlib , threading , shutil , tempfile
import json , subprocess
import cloudinary.api
import cloudinary



# Create your views here.
@login_required
def google_authentication_view(request):
    try:
        # This will initiate the Google authentication process
        return request.socialaccount_login('google')
    except OAuth2Error:
        # Handle any OAuth2 errors as needed
        # For example, you could redirect to an error page
        return render(request, 'base/Error.html')
    
    
    
    
    
        
def Errorpage(request):
    return redirect('Error')


# checking email validation for checking user entered email or username
# email regex
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def checkEmail(emailOrUsername):
    if (re.fullmatch(regex, emailOrUsername)):
        return True
    else:
        return False
        
def loginPage(request):
    page = 'login'

    # all admins
    admins = User.objects.filter(is_staff=True)

    if request.user.is_authenticated:
        if request.user in admins:
            return redirect('admin-panel')
        else:
            return redirect('home')
    else:
        logout(request)

    if request.method == 'POST':
        email_or_username = request.POST['email'].lower()
        password = request.POST['password1']

        if checkEmail(email_or_username):
            # find username
            user = User.objects.filter(email__iexact=email_or_username).first()
        else:
            user = User.objects.filter(username__iexact=email_or_username).first()

        if user is not None:
            user = authenticate(request, username=user.username, password=password)
            profile_obj = Profile.objects.filter(user=user).first()

            if user is not None:
                if user in admins:
                    # Admins (staff) don't have profiles, so no need to check is_verified
                    login(request, user)
                    return redirect('admin-panel')

                # For non-admin users, check the profile for verification
                if profile_obj is not None and not profile_obj.is_verified:
                    resend_link = reverse('resend_email_verification', args=[user.id])
                    messages.error(request, f'Profile is not verified check your mail or Click resend to send the verification email. <a href="{resend_link}"> Resend</a>')
                    
    
                    
                    return redirect('login')

                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid password please enter correct password.")
                return redirect('login')
        else:
            messages.error(request, "User not found.")
            return redirect('login')

    context = {'page': page}
    return render(request, 'base/login.html', context)




def logoutUser(request):
    logout(request)
    return redirect('home')


# def admin_home(request):
#     if request.user.is_staff:
#         return()
#     # Your view logic here
#     return render(request, 'login.html')



# /////////////////////////////////////////////////////////////////
# @login_required(login_url='login')
# def homePage(request):
#     page='login'
#     form = UserCreationForm
#     if request.user.is_authenticated and not request.user.is_staff:
#         courses=Courses.objects.all()

@login_required(login_url='login')
def getCourses(request):
    courses=Courses.objects.all()
    data=[{'name':course.name, 'title': course.title, 'id':course.id} for course in courses]
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required(login_url='login')
def getFiles(request):
    Files=files.objects.all()
    data=[{'title':file.title, 'id':file.id, 'uploaded':json_serial(file.uploaded), 'coursecode':file.courseCode, 'unit': file.unit} for file in Files]
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required(login_url='login')
def getCaFiles(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    Files=cafiles.objects.filter(isverified=q)
    data = []

    for file in Files:
        user_dict = model_to_dict(file.user, fields=['username']) if file.user else {}
        file_data = {
            'id': file.id,
            'uploaded': json_serial(file.uploaded),
            'courseCode': file.courseCode,
            'teachername': file.teachername,
            'cadate': json_serial(file.cadate),
            'user': user_dict,
            'canumber': file.canumber,
            
        }
        data.append(file_data)

    return HttpResponse(json.dumps(data), content_type="application/json")



def addSubscriber(request):
    email=request.GET.get('q') if request.GET.get('q')!=None else ''

    # Check if the email is already subscribed
    try:
        if subscribers.objects.filter(email=email).exists():

            data=[{'response':"You are already subscribed", 'result':'fail'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            # If not subscribed, save the subscriber
            subscriber = subscribers(email=email)
            subscriber.save()
            
            data=[{'response':"Thanks for Subscribing", 'result':'success'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
    except:
        data=[{'response':"Error Occured, try again", 'result':'fail'}]
        return HttpResponse(json.dumps(data), content_type="application/json")



@login_required(login_url='login')
def pptPage(request):

    if request.GET.get('q')==None:
        return render(request, 'base/ppt_page.html')

    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    Files=files.objects.filter(Q(courseCode__icontains=q))
    data=[{'title':file.title, 'id':file.id, 'uploaded':json_serial(file.uploaded), 'coursecode':file.courseCode, 'unit': file.unit} for file in Files]
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required(login_url='login')
def CaPage(request):
    if request.GET.get('q')==None:
        return render(request, 'base/ca-page.html')

    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    Files=cafiles.objects.filter(Q(courseCode__icontains=q)).filter(isverified=True)
    data=[{'canumber':file.canumber, 'id':file.id,'cadate':json_serial(file.cadate), 'uploaded':json_serial(file.uploaded), 'coursecode':file.courseCode, 'teachername': file.teachername} for file in Files]
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required(login_url='login')
def deleteFileAsAdmin(request):
    # all admins
    admins = User.objects.filter(is_staff=True)

    if request.user in admins:
        q=request.GET.get('q') if request.GET.get('q')!=None else ''
        q,type=q.split('?t=')
        if type=="ca":
            File=cafiles.objects.filter(Q(id__icontains=q))
            for file in File:
                cloudinary.api.delete_resources(file.fileupload, resource_type="raw", type="upload")
            File.delete()
            data=[{'response':"CA File deleted", 'result':'success'}]
            return HttpResponse(json.dumps(data), content_type="application/json")

        else:
            File=files.objects.filter(Q(id__icontains=q))
            for file in File:
                cloudinary.api.delete_resources(file.fileupload, resource_type="raw", type="upload")
            File.delete()
            data=[{'response':"Course File deleted", 'result':'success'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data=[{'response':"Unauthorized Access", 'result':'fail'}]
        return HttpResponse(json.dumps(data), content_type="application/json")



@login_required(login_url='login')
def deleteCaFileAsAdmin(request):
    if request.method=='POST':
        q=request.GET.get('q') if request.GET.get('q')!=None else ''
        File=cafiles.objects.filter(Q(id__icontains=q))
        for file in File:
            cloudinary.api.delete_resources(file.fileupload, resource_type="raw", type="upload")
        File.delete()
        return HttpResponse(["File deleted"], content_type="application/json")
    else:
        return HttpResponse(["Unauthorized access"], content_type="application/json")

@login_required(login_url='login')
def ApproveCaFileAsAdmin(request):
    # all admins
    admins = User.objects.filter(is_staff=True)
    if request.user in admins:
        try:
            q=request.GET.get('q') if request.GET.get('q')!=None else ''
            File=cafiles.objects.filter(Q(id__icontains=q))
            for file in File:
                file.isverified=True
                file.save()
                data=[{'response':"File Approved", 'result':'success'}]
                return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            data=[{'response':"Error Occured", 'result':'fail'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
    
    data=[{'response':"Unauthorized Access", 'result':'fail'}]
    return HttpResponse(json.dumps(data), content_type="application/json")


def register(request):
    form = userForm()  
    if request.method == 'POST': 
        username = request.POST.get('username', '').lower()  
        email = request.POST.get('email', '').lower()  
        password1 = request.POST.get('password1', '') 
        password2 = request.POST.get('password2', '') 

        
        if not username:
            messages.error(request, "Please fill the username.")
            return render(request, 'base/register.html', {'form': form})
        
        if not email:
            messages.error(request, "Please fill in the email.")
            return render(request, 'base/register.html', {'form': form})
    
        elif not password1:
            messages.error(request, "Please fill in the password.")
            return render(request, 'base/register.html', {'form': form})

        # password regex
        password_regex = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$'
        
        if password1 != password2:
            messages.error(request, "Passwords does'nt match.")
            return render(request, 'base/register.html', {'form': form})
        
        elif len(password1) < 8:
            messages.error(request, "Password length must be at least 8 characters.")
            return render(request, 'base/register.html', {'form': form})
        
        elif len(password1) > 15:
            messages.error(request, "Password length must not exceed 15 characters.")
            return render(request, 'base/register.html', {'form': form})
        elif isCommonPassword(password1):
            messages.error(request, "Password should not be common like abc or 123.")
            return render(request, 'base/register.html', {'form': form})
        
        else: 
            form = userForm(request.POST)
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.error(request, "user already exist.")
                return render(request, 'base/register.html', {'form': form})
                
            if form.is_valid():
                user = form.save(commit=False)
                user.username=username
                user.email = email
                user.password=password1
                form.save()
                auth_token = str(uuid.uuid4())
                request.session['auth_token']=auth_token
                profile_obj = Profile.objects.create(user = user, auth_token=auth_token)
                profile_obj.save()
                send_mail_after_registration(email , username, auth_token)
                messages.success(request, "Registration successful!")
                return redirect('Email_send')  

            else:
                messages.error(request, "An error occurred during registration.")
                return render(request, 'base/register.html', {'form': form})
        
    else:
        form = userForm()
        return render(request, 'base/register.html', {'form': form})
    
    
def send_mail_after_registration(email , username, token):
    
    verification_link = f"http://127.0.0.1:8000/verify_mail_after_registration/{token}/"  
    html_template = 'base/Email_verification.html'
    html_message = render_to_string(html_template, {'token': token, 'verification_link': verification_link, 'username': username})  
    text_content = strip_tags(html_message)          
    subject = "Welcome to StudySync"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email = EmailMultiAlternatives(subject, text_content, email_from, recipient_list )
    email.attach_alternative(html_message, "text/html")            # Send the email
    email.send()
    
    
def verify_mail_after_registration(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()

    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request, 'Your Account is already verified')
            return redirect('login')

        # Check if the verification link has expired
        current_time = timezone.now()
        time_difference = current_time - profile_obj.created_at  # Assuming you have a 'created_at' field in your Profile model
        if time_difference > timedelta(minutes=15 ):
            messages.error(request, 'The verification link has expired. Please request a new one.')
            return redirect('login')
        else:
            profile_obj.is_verified = True
            new_token = str(request.session.get('new_token', ''))
            request.session['auth_token'] = True
            request.session['new_token'] = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('Email_success')
    else:
        # User exists but does not have a profile, resend the verification email
        user = User.objects.filter(profile__auth_token=auth_token).first()

        if user:
            send_mail_after_registration(user.email, auth_token)
            messages.success(request, 'Verification email has been resent. Check your mail.')
            return redirect('login')
        else:
            return render(request, 'base/Error.html')



def resend_email_verification(request , user_id):
    user = get_object_or_404(User, id=user_id)
    profile_obj = Profile.objects.filter(user=user_id).first()

    if profile_obj is not None and not profile_obj.is_verified:
        # Generate a new verification token and send the verification email
        new_token = str(uuid.uuid4())  # Implement a function to generate a new token
        profile_obj. auth_token = new_token
        request.session['new_token']=new_token
        profile_obj.created_at = timezone.now()
        profile_obj.save()

        send_mail_after_registration(user.email,user.username, new_token)

        messages.success(request, 'Verification email resent. Check your mail.')
        return redirect('Email_send')
    else:
        messages.info(request, 'Your profile is already verified.')

    return redirect('home')



def email_template_after_mail(request):
    new_token = str(request.session.get('new_token', ''))
    auth_token = str(request.session.get('auth_token', ''))

    if new_token or auth_token:

        if 'auth_token' in request.session:
            del request.session['auth_token']

        if 'new_token' in request.session:
            del request.session['new_token']

        return render(request, 'base/Email_send.html')
    else:
        return render(request, 'base/Error.html')
        

def email_verification_successful(request):
    new_token = str(request.session.get('new_token', ''))
    auth_token = str(request.session.get('auth_token', ''))
    
    if new_token or auth_token:
        if 'auth_token' in request.session or 'new_token' in request.session:
            del request.session['auth_token']
            del request.session['new_token']
            
        return render(request, 'base/Email_success.html')
    else:
        return render(request, 'base/Error.html')

    
    
    
@login_required(login_url='login')   
def reportBugPage(request):
    if request.method=='POST':
        report_type=request.POST['type']
        report_Detail=request.POST['details']
        Reporter_name=request.POST['name']
        Reporter_email=request.user.email

        report=Report(reportType=report_type, detail=report_Detail, name=Reporter_name, email=Reporter_email)
        report.save()

        messages.success(request,'Thank you for helping us in development.')
        return redirect('/report-bug')
    return render(request, 'base/ReportBug.html')


@login_required(login_url='login')
def pdfview(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    q,type =q.split('?t=')
    if type=="ca":
        Files=cafiles.objects.filter(Q(id__icontains=q))
        context={"files":Files}
        return render(request, "base/pdfview.html", context)
    else:
        Files=files.objects.filter(Q(id__icontains=q))
        context={"files":Files}
        return render(request, "base/pdfview.html",context)
    
    
    
@csrf_exempt
def CompilerPage(request):
    temp_dir = None  

    if request.method == 'POST':
        try:
            
            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', '')
            input_data = data.get('input_data', '')
            inputs = input_data.split()      
            temp_dir = tempfile.mkdtemp()

            if language == 'python':
                if not input_data:    
                    process = subprocess.Popen(
                        ['python', '-c', code],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                        
                    )
                    try:
                        output, error = process.communicate(input='\n'.join(inputs), timeout=5)     
                        
                        result = {
                            'result': output, 
                            'error': error
                        }
                    except TimeoutExpired:      
                        result = {
                            'result': '',
                            'error': 'Time out'
                        }
                    
                    return JsonResponse(result)
                else:
                    process = subprocess.Popen(
                        ['python', '-c', code],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    output, error = process.communicate(input='\n'.join(inputs))
                    result = {
                        'result': output,
                        'error': error
                    }
                    
                    return JsonResponse(result)
                
            elif language == 'java':
                main_class = code.split('class ')[1].split('{')[0].strip() 
                code_file_path = os.path.join(temp_dir, 'Main.java')  
                with open(code_file_path, 'w') as code_file:
                    code_file.write(code)
                
                compile_command = ['javac', 'Main.java']
                process = subprocess.run(compile_command, cwd=temp_dir, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                if process.returncode != 0:
                    return JsonResponse({'error': process.stderr})
                
                try:
                    command = ['java', main_class]  
                    process = subprocess.run(command, cwd=temp_dir, text=True, input='\n'.join(inputs), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
                    
                    if process.returncode != 0:
                        return JsonResponse({'error': process.stderr})
                    
                    result = {
                        'result': process.stdout,
                        'error': process.stderr
                    }
                    return JsonResponse(result)
                    
                except subprocess.TimeoutExpired:
                    return JsonResponse({'error': 'Code execution timed out'})
                
                
            elif language == 'cpp':
                code_file_path = os.path.join(temp_dir, 'code.cpp') 
                exe_file_path = os.path.join(temp_dir, 'executable.exe')  
                with open(code_file_path, 'w') as code_file:
                    code_file.write(code)

                compile_command = ["g++", '-o', exe_file_path, 'code.cpp']
                process = subprocess.run(compile_command, cwd=temp_dir, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if process.returncode != 0:
                    return JsonResponse({'error': process.stderr})


                try:
                    if isinstance(input_data, bytes):
                        input_data_str = input_data.decode('utf-8')
                        process = subprocess.run([exe_file_path], input=input_data_str, cwd=temp_dir, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
                    elif isinstance(input_data, str):
                        process = subprocess.run([exe_file_path], input=input_data, cwd=temp_dir, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
                    else:
                        raise ValueError("Invalid type for input_data")
                except subprocess.TimeoutExpired:
                    return JsonResponse({'error': 'Code execution timed out'})


                
                if process.returncode != 0:
                    return JsonResponse({'error': process.stderr})

            return JsonResponse({'result': process.stdout})

        except Exception as e:
            return JsonResponse({'error': str(e)})

        finally:    
            if temp_dir:
                shutil.rmtree(temp_dir)

    return render(request, "base/compiler_page.html")




def Forgot_password(request):
    form = userForm()
    if request.method == 'POST':
        user = User
        email = request.POST.get('email')      
        if not email:
            messages.error(request, "Email is required Please enter the Email")
            return render(request, "base/Forgot_Password.html", {'form': form})          
        otp_token = random.randint(111111,999999)
        user_data = User.objects.filter(email=email)
        if user_data.exists():
            for user in user_data:
                User_Email_verification.objects.filter(user=user).delete()
                request.session['email'] = email
                request.session['otp_token']=otp_token
                request.session['otp_generated_time'] = str(timezone.now()) 
                auth_token = uuid.uuid4()
                auth_token_str = str(auth_token)
                user_verification = User_Email_verification.objects.create(user=user,email=email,otp = otp_token,auth_token=auth_token_str)
                html_template = 'base/Email_OTP_Template.html'
                html_message = render_to_string(html_template, {'otp_token': otp_token })  
                text_content = strip_tags(html_message)          
                
                
                subject = "Welcome to StudySync"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                email = EmailMultiAlternatives(subject, text_content, email_from, recipient_list )
                email.attach_alternative(html_message, "text/html")
                # Send the email
                email.send()

                messages.success(request , 'Enter the 6 digit OTP send on your Registered Email id')
                return render(request, 'base/otp-verification.html', {'form': form})
                
        else:
            messages.error(request, "Email Not Found Create account!!!")
            return render(request, "base/Forgot_Password.html", {'form': form})
        
    else:
        return render(request, "base/Forgot_Password.html", {'form': form})
    
    


def verify_user_otp(request):
    if not 'email' in request.session:
        return redirect('login')
    else:
        form = userForm()
        if request.method == 'POST':
            entered_otp = ''.join(request.POST.get(f'digit{i}', '') for i in range(1, 7))
        

            if not entered_otp:
                messages.error(request, "OTP is required. Please enter the OTP.")
                return render(request, "base/otp-verification.html",{'form':form})

            email = request.session.get('email')
            otp_token = str(request.session.get('otp_token', ''))
            
            if 'otp_generated_time' in request.session:
                otp_generated_time_str = request.session['otp_generated_time']
                otp_generated_time = datetime.strptime(otp_generated_time_str, "%Y-%m-%d %H:%M:%S.%f%z")
                current_time = timezone.now()
                time_difference = current_time - otp_generated_time
                expiration_time_in_minutes = 1 
                if time_difference.total_seconds() > expiration_time_in_minutes * 60:
            
                    messages.error(request, "Session expired. Please try again.")
                    return render(request, "base/otp-verification.html", {'form': form})

            user_verification = User_Email_verification.objects.filter(user__email=email).first()

            if user_verification and otp_token == entered_otp:  
                
                user_verification.is_verified = True
                user_verification.save()
                del request.session['otp_token']
                del request.session['otp_generated_time']
                
                request.session['otp_verified'] = True

                messages.success(request, "OTP verified successfully. You can now reset your password.")
                return render(request, 'base/password_verification.html', {'form':form})

            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, "base/otp-verification.html",{'form':form})

        return redirect('Forgot_Password')
    
    
    
def resend_email_verification_with_otp(request):
    if not 'email' in request.session:
        return redirect('login')
    else:
        email = request.session.get('email')
        otp_token = random.randint(111111, 999999)

        user_data = User.objects.filter(email=email)
        if user_data.exists():
            for user in user_data:
                # Delete previous email and associated records
                User_Email_verification.objects.filter(user=user).delete()
                request.session['otp_token']=otp_token
                request.session['otp_generated_time'] = str(timezone.now()) 

                # Save new OTP and send a new email
                auth_token = uuid.uuid4()
                auth_token_str = str(auth_token)
                user_verification = User_Email_verification.objects.create(user=user, email=email, otp=otp_token, auth_token=auth_token_str)

                html_template = 'base/Email_OTP_Template.html'
                html_message = render_to_string(html_template, {'otp_token': otp_token })  
                text_content = strip_tags(html_message)          
                
                subject = "Welcome to StudySync"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email,]

                email = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
                email.attach_alternative(html_message, "text/html")
                # Send the email
                email.send()
                
                if email.send() == True:
                    messages.success(request, 'Enter the new 6-digit OTP sent to your registered email id.')
                    return render(request, 'base/otp-verification.html', {'form': userForm()})
                else:
                    return render(request, 'base/Error.html')
        
        messages.error(request, "Session expired resend the OTP again")
        return render(request, "base/Forgot_Password.html", {'form': userForm()})
        
    

    
    
def update_password_with_otp(request):
    
    if 'otp_verified' not in request.session or not request.session['otp_verified']:
        return redirect('otp-verification')
    
    if 'email' not in request.session:
        return redirect('login')
    

    if request.method == 'POST':
        form = PasswordUpdateForm(request.POST)
        password1 = request.POST.get('new_password', '') 
        password2 = request.POST.get('confirm_password', '') 
        
        
        email = request.session.get('email')
        user = User.objects.filter(email=email).first()
        
        if user and check_password(password1, user.password):
            messages.error(request, 'New password must be different from the old one.')
            return render(request, 'base/password_verification.html', {'form': form})
        
        elif not password1:
            messages.error(request, "Please fill in the password.")
            return render(request, 'base/password_verification.html', {'form': form})
        
        elif password1 != password2:
            messages.error(request, "Passwords does'nt match.")
            return render(request, 'base/password_verification.html', {'form': form})
        
        elif len(password1) < 8:
            messages.error(request, "Password length must be at least 8 characters.")
            return render(request, 'base/password_verification.html', {'form': form})
        
        elif len(password1) > 15:
            messages.error(request, "Password length must not exceed 15 characters.")
            return render(request, 'base/password_verification.html', {'form': form})
        
        elif isCommonPassword(password1):
            messages.error(request, "Password should not be common like abc or 123.")
            return render(request, 'base/password_verification.html', {'form': form})
        
        
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password == confirm_password:
                reset_email = request.session.get('email')

                if reset_email:
                    user_queryset = User.objects.filter(email=reset_email)
                    if user_queryset.exists():
                        user = user_queryset.first()
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)
                        
                        user_verification = User_Email_verification.objects.filter(user__email=reset_email).first()
                        if user_verification:
                            user_verification.delete()
                        
                        
                        
                        request.session['otp_verified'] = True
                        
                        if 'email' in request.session:
                            del request.session['email']
                            messages.success(request, 'Your password was successfully updated!')
                            return redirect('login')
                    else:
                        messages.error(request, 'User with the specified email not found.')
                else:
                    messages.error(request, 'Email session no longer available. Session expired!!!')
            else:
                messages.error(request, 'New Password and Confirm Password do not match.')
        else:
            messages.error(request, 'Please enter the password below')
    else:
        form = PasswordUpdateForm()

    return render(request, "base/password_verification.html", {'form': form})
    
    
    
    


# temp views
def homePage(request):
    # logout(request)
    admins = User.objects.filter(is_staff=True)

    if request.user.is_authenticated:
        if request.user in admins:
            return redirect('admin-panel')
    return render(request, "base/landing.html")


# unavailable-app
def unavailableAppPage(request):
    msgs=["Application in progress"]
    context={'messages': msgs}
    return render(request, "base/unavailable.html", context)



# for admin access
@login_required(login_url='login')
def showadmin(request):
    admins = User.objects.filter(is_staff=True)

    if request.user.is_authenticated:
        if request.user in admins:
            return render(request,'base/admin_panel.html')
    return render(request, "base/Error.html")



def uploadFileAsAdmin(request):
    if request.method == 'POST':
        try:
            Title=request.POST.get('title')
            Coursecode=request.POST.get('courseCode')
            Unit=request.POST.get('unit')
            File=request.FILES['file']
            fileData=files(title=Title, courseCode=Coursecode, unit=Unit, fileupload=File)
            fileData.save()
            data=[{'response':"File Added", 'result':'success'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            data=[{'response':"Error Occured, try again", 'result':'fail'}]    
            return HttpResponse(json.dumps(data), content_type="application/json")        
        
        

def uploadCaAsUser(request):
    if request.method == 'POST':
        try:
            user = request.user
            Coursecode = request.POST.get('courseCode')
            teachername = request.POST.get('teachername')
            canumber = request.POST.get('ca-no')
            cadate = request.POST.get('cadate')
            files = request.FILES.getlist('fileupload')

            for file in files:
                file_extension = os.path.splitext(file.name)[1].lower()

                if file_extension in ('.jpg', '.jpeg', '.png'):
                    pdf_content = convert_images_to_pdf([file.read() for file in files])
                    cadate = timezone.make_aware(datetime.strptime(cadate, '%Y-%m-%d'))

                    with transaction.atomic():
                        existing_record = cafiles.objects.select_for_update().filter(user=user, cadate=cadate).first()

                        if existing_record:
                            existing_record.teachername = teachername
                            existing_record.fileupload.delete()  
                            existing_record.fileupload.save('merged_file.pdf', ContentFile(pdf_content), save=True)

                            data=[{'response':"File Updated", 'result':'success'}]
                            return HttpResponse(json.dumps(data), content_type="application/json")
                        else:
                            file_data = cafiles(
                                user=user,
                                courseCode=Coursecode,
                                teachername=teachername,
                                canumber=canumber,
                                cadate=cadate,
                            )
                            pdf_buffer = BytesIO(pdf_content)
                            file_data.fileupload.save('merged_file.pdf', ContentFile(pdf_buffer.getvalue()), save=True)

                            data=[{'response':"File Added", 'result':'success'}]
                            return HttpResponse(json.dumps(data), content_type="application/json")

                elif file_extension in ('.pdf'):
                    # function to Merge PDF files into a single PDF
                    pdf_content = merge_pdf_files(files)
                    file_data = cafiles(user=user,courseCode=Coursecode,teachername=teachername,canumber=canumber,cadate=cadate,)
                    file_data.save()

                    file_data.fileupload.save('merged_file.pdf', ContentFile(pdf_content), save=True)

                    data=[{'response':"File Added", 'result':'success'}]
                    return HttpResponse(json.dumps(data), content_type="application/json")

            data=[{'response':"File not found in the request", 'result':'fail'}]
            return HttpResponse(json.dumps(data), content_type="application/json")

        except Exception as e:
            data=[{'response':"Error Occured", 'result':'fail'}]
            return HttpResponse(json.dumps(data), content_type="application/json")

        
        
def uploadCourseAsAdmin(request):
    if request.method == 'POST':
        try:
            Title=request.POST.get('title')
            Coursecode=request.POST.get('courseCode')

            Course=Courses(title=Title, name=Coursecode)
            Course.save()
            data=[{'response':"Course Added", 'result':'success'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            data=[{'response':"Error Occured", 'result':'fail'}]
            return HttpResponse(json.dumps(data), content_type="application/json")

@login_required(login_url='login')
def deleteReportAsAdmin(request):
    # all admins
    admins = User.objects.filter(is_staff=True)

    if request.user in admins:
        q=request.GET.get('q') if request.GET.get('q')!=None else ''
        try:
            Reports=Report.objects.filter(Q(id__icontains=q))
            for report in Reports:
                report.delete()
            data=[{'response':"Report deleted", 'result':'success'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            data=[{'response':"Error in Report Deletion", 'result':'fail'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data=[{'response':"Unauthorized Access", 'result':'fail'}]
        return HttpResponse(json.dumps(data), content_type="application/json")
    
@login_required(login_url='login')
def deleteSubscriberAsAdmin(request):
    # all admins
    admins = User.objects.filter(is_staff=True)

    if request.user in admins:
        q=request.GET.get('q') if request.GET.get('q')!=None else ''
        try:
            Subscribers=subscribers.objects.filter(Q(id__icontains=q))
            for subscriber in Subscribers:
                subscriber.delete()
            data=[{'response':"Subscriber deleted", 'result':'success'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            data=[{'response':"Error in Subscriber Deletion", 'result':'fail'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data=[{'response':"Unauthorized Access", 'result':'fail'}]
        return HttpResponse(json.dumps(data), content_type="application/json")

@login_required(login_url='login')
def deleteCourseAsAdmin(request):
    # all admins
    admins = User.objects.filter(is_staff=True)

    if request.user in admins:
        q=request.GET.get('q') if request.GET.get('q')!=None else ''
        try:
            courses=Courses.objects.filter(Q(id__icontains=q))
            for course in courses:
                course.delete()
            data=[{'response':"Course deleted", 'result':'success'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            data=[{'response':"Error in Course Deletion", 'result':'fail'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data=[{'response':"Unauthorized Access", 'result':'fail'}]
        return HttpResponse(json.dumps(data), content_type="application/json")

        




##################### admin analysis ######################

@login_required(login_url='login')
def noofusers(request):
    # all admins
    admins = User.objects.filter(is_staff=True)

    if request.user.is_authenticated:
        if request.user in admins:
            try:
                users=User.objects.all()
                Files=files.objects.all()
                Cafiles=cafiles.objects.all()
                Reports=Report.objects.all()
                Subscribers=subscribers.objects.all()
                data=[{'usercount':users.count(), 'coursefilescount': Files.count(), 'cafilescount': Cafiles.count(), 'reportscount': Reports.count(), 'subscriberscount': Subscribers.count()}]
                return HttpResponse(json.dumps(data), content_type="application/json")
            except:
                data=[{'response':"Unauthorized Access", 'result':'fail'}]
                return HttpResponse(json.dumps(data), content_type="application/json")

    data=[{'response':"Unauthorized Access", 'result':'fail'}]
    return HttpResponse(json.dumps(data), content_type="application/json")


def is_Verified(username):
    profiles=Profile.objects.all()
    for profile in profiles:
        if str(profile.user) == str(username):
            return True
    return False


@login_required(login_url='login')
def returnReports(request):
    # all admins
    admins = User.objects.filter(is_staff=True)

    if request.user in admins:
        try:
            reports=Report.objects.all()
            data=[{'email':report.email, 'name':report.name, 'id': report.id, 'type': report.reportType, 'content': report.detail} for report in reports]
            return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            data=[{'response':"Unauthorized Access", 'result':'fail'}]
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data=[{'response':"Unauthorized Access", 'result':'fail'}]
        return HttpResponse(json.dumps(data), content_type="application/json")

@login_required(login_url='login')
def returnSubscribers(request):
    # all admins
    admins = User.objects.filter(is_staff=True)

    if request.user in admins:
        try:
            Subscribers=subscribers.objects.all()
            data=[{'email':subscribe.email, 'id': subscribe.id} for subscribe in Subscribers]
            return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            data=[{'response':"Unauthorized Access", 'result':'fail'}]
            return HttpResponse(json.dumps(data), content_type="application/json")

    data=[{'response':"Unauthorized Access", 'result':'fail'}]
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required(login_url='login')
def returnUsers(request):
    # all admins
    admins = User.objects.filter(is_staff=True)

    if request.user in admins:
        try:
            users=User.objects.all()
            data=[{'username':user.username, 'email': user.email, 'firstname': user.first_name, 'lastname': user.last_name,'isverified':is_Verified(user.username) , 'lastlogin': json_serial(user.last_login), 'id':user.id} for user in users]
            return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            data=[{'response':"Unauthorized Access", 'result':'fail'}]
            return HttpResponse(json.dumps(data), content_type="application/json")

    else:
        data=[{'response':"Unauthorized Access", 'result':'fail'}]
        return HttpResponse(json.dumps(data), content_type="application/json")




############################################################
###################### functions ###########################
############################################################

def isCommonPassword(password):
    commonPasswords = ["password", "123456", "qwerty", "admin", "letmein", "welcome", "123abc"]
    return password.lower() in commonPasswords

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()[:10]
    raise TypeError ("Type %s not serializable" % type(obj))
        
def convert_images_to_pdf(images):
    pdf_buffer = BytesIO()
    pdf_buffer.write(img2pdf.convert(images))
    return pdf_buffer.getvalue()


def merge_pdf_files(files_list):
    pdf_merger = PdfMerger()

    for file in files_list:
        if isinstance(file, InMemoryUploadedFile):
            pdf_merger.append(BytesIO(file.read()))
        elif isinstance(file, TemporaryUploadedFile):
            with open(file.temporary_file_path(), 'rb') as tmp_file:
                pdf_merger.append(tmp_file)
        else:
            pdf_merger.append(file.fileupload)  # Use the correct attribute name

    merged_pdf_content = BytesIO()
    pdf_merger.write(merged_pdf_content)

    return merged_pdf_content.getvalue()


