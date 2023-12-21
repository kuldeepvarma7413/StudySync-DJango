"""
URL configuration for studysync project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from allauth.socialaccount.views import SignupView

urlpatterns = [

    path('',views.homePage, name= "home" ),
    # path('admin_home/', views.admin_home, name='admin_home'),

    path('login/',views.loginPage, name="login" ),
    path('Forgot_Password/',views.Forgot_password, name="Forgot_Password" ), # type: ignore
    path('otp-verification/',views.verify_user_otp, name="otp-verification" ),
    path('resend_otp_verification/', views.resend_email_verification_with_otp, name="resend_otp_verification"), 
    path('password_verification/',views. update_password_with_otp, name="password_verification" ),
    path('logout/',views.logoutUser, name="logout" ),
    path('register/',views.register, name="register" ),
    path('Email_send/',views.email_template_after_mail, name="Email_send" ),
    path('verify_mail_after_registration/<str:auth_token>/', views.verify_mail_after_registration, name= "verify_mail_after_registration"),
    path('Email_success/', views.email_verification_successful, name= "Email_success"),
    path('resend_email_verification/<int:user_id>/', views.resend_email_verification, name='resend_email_verification'),
    path('Error/',views.Errorpage, name="Error" ),
    
    path('home',views.homePage, name="home" ),
    path('ppt-page',views.pptPage, name="ppt-page" ),
    path('ca-page',views.CaPage, name="ca-page" ),
    path('pdfview',views.pdfview, name="pdfview" ),
    path('compiler',views.CompilerPage, name="compiler" ),
    path('report-bug/',views.reportBugPage, name="report-bug" ),
    
    path('google/',views.google_authentication_view ,name = "google"),

    # unavailable pages
    path('unavailable-app/',views.unavailableAppPage, name="unavailable-app" ),

    # frontend requests
    path('get-courses',views.getCourses, name="get-courses" ),
    path('get-files',views.getFiles, name="get-files" ),
    path('get-cafiles',views.getCaFiles, name="get-cafiles" ),
    path('subscriber',views.addSubscriber, name="subscriber" ),


    # admin access
    path('admin-panel',views.showadmin, name="admin-panel" ),
    path('upload-file',views.uploadFileAsAdmin, name="upload-file" ), # type: ignore
    path('upload-course',views.uploadCourseAsAdmin, name="upload-course" ), # type: ignore
    path('delete-file',views.deleteFileAsAdmin, name="upload-file" ), # type: ignore
    path('delete-cafile',views.deleteCaFileAsAdmin, name="upload-cafile" ), # type: ignore
    path('approve-cafile',views.ApproveCaFileAsAdmin, name="approve-cafile" ), # type: ignore

    # admin analysis
    path('get-analysis/',views.noofusers, name="get-analysis" ), # type: ignore


    # user access
    path('upload-ca',views.uploadCaAsUser, name="upload-ca" ), # type: ignore

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
