from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from base.models import Courses, files ,Syllabus 
from .forms import userForm , PasswordUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Report , User_Email_verification
from django.urls import reverse
from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
import random , smtplib , email.message
from django.conf import settings
from django.core.mail import EmailMessage , send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import update_session_auth_hash
import re



# Create your views here.
@login_required
def google_authentication_view(request):
    try:
        # This will initiate the Google authentication process
        return request.socialaccount_login('google')
    except OAuth2Error:
        # Handle any OAuth2 errors as needed
        # For example, you could redirect to an error page
        return HttpResponse(status=201)
    
    
    
    
    
        
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
    page='login'

    if request.user.is_authenticated:
        return redirect('home')
    else:
        logout(request)

    if request.method=='POST':
        emailOrUsername=request.POST['email'].lower()
        password=request.POST['password1']
        username=""
        if(checkEmail(emailOrUsername)):
            # find username
            curruser=User.objects.filter(Q(email__icontains=emailOrUsername))
            username=curruser[0]
        else:
            username=emailOrUsername

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Email Id or password.")
            return redirect('login')
    else: 
        context={'page':page}
        return render(request, 'base/login.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')


# def admin_home(request):
#     if request.user.is_staff:
#         return()
#     # Your view logic here
#     return render(request, 'login.html')




@login_required(login_url='login')
def homePage(request):
    page='login'
    form = UserCreationForm
    if request.user.is_authenticated and not request.user.is_staff:
        courses=Courses.objects.all()

        if request.GET.get('q')==None:
            msgs=["Please select a course."]
            context={'courses':courses, 'messages':msgs}
            return render(request, 'base/home.html', context)

        q=request.GET.get('q') if request.GET.get('q')!=None else ''
        Files=files.objects.filter(Q(courseCode__icontains=q))
        
        if not Files:
            msgs=["No files found."]
            context={'courses':courses, 'messages':msgs}
            return render(request, 'base/home.html', context)

        context={'courses':courses, 'files':Files}
        return render(request, 'base/home.html', context)
    else:
        messages.error(request, "You are not allowed to login until you logout as the admin.")
        return render(request, 'base/login.html', {'form':form})


# work on it

#register





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
        
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'base/register.html', {'form': form})
        
        elif len(password1) < 6:
            messages.error(request, "Password length must be at least 6 characters.")
            return render(request, 'base/register.html', {'form': form})
        
        elif len(password1) > 15:
            messages.error(request, "Password length must not exceed 15 characters.")
            return render(request, 'base/register.html', {'form': form})
        
        else: 
            form = userForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username=username
                user.email = email
                user.password=password1
                form.save()
                messages.success(request, "Registration successful!")
                return redirect('login')  

            else:
                messages.error(request, "An error occurred during registration.")
            return render(request, 'base/register.html', {'form': form})
        
    else:
        form = userForm()
        
        return render(request, 'base/register.html', {'form': form})

    
    
    
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
    syllabus=Syllabus.objects.filter(Q(id__icontains=q))
    context={"files":Files , "syllabus":Syllabus}
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
        if user_data:
            request.session['email'] = email
            request.session['otp_token']=otp_token
            request.session['otp_generated_time'] = str(timezone.now()) 
            for user in user_data:
                user_verification = User_Email_verification.objects.create(user=user,otp = otp_token)
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
                expiration_time_in_minutes = 10 
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
    
    
    
    




