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
from .models import Report , User_Email_verification
from django.urls import reverse
from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
import random , smtplib , email.message , uuid
from django.conf import settings
from django.core.mail import EmailMessage , send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime , timedelta
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
import re
import json
from datetime import date, datetime
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

@login_required
def getCourses(request):
    courses=Courses.objects.all()
    data=[{'name':course.name, 'title': course.title} for course in courses]
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def getFiles(request):
    Files=files.objects.all()
    data=[{'title':file.title, 'id':file.id, 'uploaded':json_serial(file.uploaded), 'coursecode':file.courseCode, 'unit': file.unit} for file in Files]
    return HttpResponse(json.dumps(data), content_type="application/json")

# @csrf_exempt
# def addSubscriber(request):
#     print("Entry")
#     email = request.POST['email']
#     print("got mail")
#     subscriber=subscribers(email=email)
#     subscriber.save()
#     return HttpResponse([True], content_type="application/json")


def pptPage(request):

    if request.GET.get('q')==None:
        return render(request, 'base/ppt_page.html')

    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    Files=files.objects.filter(Q(courseCode__icontains=q))
    data=[{'title':file.title, 'id':file.id, 'uploaded':json_serial(file.uploaded), 'coursecode':file.courseCode, 'unit': file.unit} for file in Files]
    return HttpResponse(json.dumps(data), content_type="application/json")

def deleteFileAsAdmin(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    File=files.objects.filter(Q(id__icontains=q))
    for file in File:
        cloudinary.api.delete_resources(file.fileupload, resource_type="raw", type="upload")
    File.delete()
    return HttpResponse(["File deleted"], content_type="application/json")



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
        
        elif len(password1) < 6:
            messages.error(request, "Password length must be at least 6 characters.")
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
    recipient_list = [email,]
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
        # Uncomment the following line if you want to print the auth_token
        # print(auth_token)

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
        # print(auth_token)
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
    Files=files.objects.filter(Q(id__icontains=q))
    context={"files":Files}
    return render(request, "base/pdfview.html",context)



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
                print(email)
                print(otp_token)
                print(user_data)
                html_template = 'base/Email_OTP_Template.html'
                html_message = render_to_string(html_template, {'otp_token': otp_token })  
                text_content = strip_tags(html_message)          
                
                
                subject = "Welcome to StudySync"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email,]
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
        print(request.method)
        
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

                messages.success(request, 'Enter the new 6-digit OTP sent to your registered email id.')
                return render(request, 'base/otp-verification.html', {'form': userForm()})
        
        messages.error(request, "Session expired resend the OTP again")
        return render(request, "base/Forgot_Password.html", {'form': userForm()})
        
    

    
    
def update_password_with_otp(request):
    
    if 'otp_verified' not in request.session or not request.session['otp_verified']:
        return redirect('otp-verification')
    
    if 'email' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        form = PasswordUpdateForm(request.POST)
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
        Title=request.POST.get('title')
        Coursecode=request.POST.get('courseCode')
        Unit=request.POST.get('unit')
        File=request.FILES['file']

        try:
            fileData=files(title=Title, courseCode=Coursecode, unit=Unit, fileupload=File)
            data=fileData.save()
            print(data)
            return HttpResponse(["File Added."], content_type="application/json")
        except:
            return HttpResponse(["Error Occured"], content_type="application/json")
        
        
        
def uploadCourseAsAdmin(request):
    if request.method == 'POST':
        Title=request.POST.get('title')
        Coursecode=request.POST.get('courseCode')

        try:
            Course=Courses(title=Title, name=Coursecode)
            Course.save()
            return HttpResponse(["Course Added."], content_type="application/json")
        except:
            return HttpResponse(["Error Occured"], content_type="application/json")
        


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