from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from base.models import Courses, files ,Syllabus
from .forms import userForm
from .models import Report 
from django.urls import reverse
from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.client import OAuth2Error



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

    
        
def loginPage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('ppt-page')
    else:
        logout(request)

    if request.method=='POST':
        email=request.POST['email'].lower()
        password=request.POST['password1']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('ppt-page')
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
def pptPage(request):
    courses=Courses.objects.all()

    if request.GET.get('q')==None:
        msgs=["Please select a course."]
        context={'courses':courses, 'messages':msgs}
        return render(request, 'base/ppt_page.html', context)

    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    Files=files.objects.filter(Q(courseCode__icontains=q))
    
    if not Files:
        msgs=["No files found."]
        context={'courses':courses, 'messages':msgs}
        return render(request, 'base/ppt_page.html', context)

    context={'courses':courses, 'files':Files}
    return render(request, 'base/ppt_page.html', context)


# work on it

#register




    
def register(request):
    form = userForm()
    
    if request.method == 'POST': 
        email = request.POST.get('email', '').lower()  
        password1 = request.POST.get('password1', '') 
        password2 = request.POST.get('password2', '') 

        
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
    
    
    
    
def Forgotpassword(request):
    if request.method == 'POST':
        password_reset_url = reverse('Forgot_Password')
        # Process the form and send password reset emails if necessary
        # You can add your password reset logic here
        

        # After handling the form, you can redirect to the password reset page
        return redirect(password_reset_url)

    return render(request, 'base/Forgot_Password.html')



def Otpverification(request):
    if request.method == 'POST':
        otp= reverse('OTP_Verification')
        
        return redirect(otp)
    return render(request ,'base/OTP_Verification.html')
    
    
    
@login_required(login_url='login')   
def reportBugPage(request):
    if request.method=='POST':
        report_type=request.POST['type']
        report_Detail=request.POST['details']
        Reporter_name=request.POST['name']
        Reporter_email=request.user.email

        report=Report(reportType=report_type, detail=report_Detail, name=Reporter_name, email=Reporter_email)
        report.save()

        messages.add_message(level= messages.INFO,request=request ,message="Thank you for helping us in development.")
        return redirect('/report-bug')
    return render(request, 'base/ReportBug.html')






def pdfview(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    Files=files.objects.filter(Q(id__icontains=q))
    syllabus=Syllabus.objects.filter(Q(id__icontains=q))
    context={"files":Files , "syllabus":Syllabus}
    return render(request, "base/pdfview.html",context)

<<<<<<< HEAD

# temp views
def homePage(request):
    return render(request, "base/landing.html")


# unavailable-app
def unavailableAppPage(request):
    msgs=["Application in progress"]
    context={'messages': msgs}
    return render(request, "base/unavailable.html", context)
=======
>>>>>>> f859343f23c6b9881bc84bd088f9dbd01435160b
