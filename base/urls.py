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
    path('Forgot_Password/',views.Forgot_password, name="Forgot_Password" ),
    path('otp-verification/',views.verify_user_otp, name="otp-verification" ),
    path('password_verification/',views. update_password_with_otp, name="password_verification" ),
    path('logout/',views.logoutUser, name="logout" ),
    path('register/',views.register, name="register" ),
    path('Error/',views.Errorpage, name="Error" ),
   
    
    path('home',views.homePage, name="home" ),
    path('ppt-page',views.pptPage, name="ppt-page" ),
    path('pdfview',views.pdfview, name="pdfview" ),
    path('report-bug/',views.reportBugPage, name="report-bug" ),
    
    path('google/',views.google_authentication_view ,name = "google"),

    # unavailable pages
    path('unavailable-app/',views.unavailableAppPage, name="unavailable-app" ),


]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
