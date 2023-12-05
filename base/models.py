from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Courses(models.Model):
    name=models.CharField(max_length=20)
    title=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class files(models.Model):
    courseCode=models.CharField(max_length=20)
    title=models.CharField(max_length=100)
    unit=models.CharField(max_length=3)
    uploaded=models.DateTimeField(auto_now_add=True)
    fileupload=models.FileField(upload_to="media/",max_length=250,null=True,default=None)
    
    
def __str__(self):
        return self.courseCode

    # class Meta:
    #     ordering = ['-unit']
class Syllabus(models.Model):
    courseCode=models.CharField(max_length=20)
    title=models.CharField(max_length=100)
    fileupload=models.FileField(upload_to="media/",max_length=250,null=True,default=None)
    
    
#creating a generic event table

class Report(models.Model):
    reportType=models.CharField(max_length=20)
    detail=models.CharField(max_length=500)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)

    def __str__(self):
        return self.email
    
    
    
class User_Email_verification(models.Model):
    email = models.EmailField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='email_verification')
    auth_token = models.CharField(max_length = 140, blank=True)
    otp = models.CharField(max_length = 6, blank=True)
    is_verified = models.BooleanField(default = False)
    
    def __str__(self):
        return self.user.username
    