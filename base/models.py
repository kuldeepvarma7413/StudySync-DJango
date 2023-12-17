from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import RawMediaCloudinaryStorage


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
    fileupload=models.FileField(upload_to='raw/', blank=True, storage=RawMediaCloudinaryStorage())
    
class cafiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    courseCode=models.CharField(max_length=20)
    teachername=models.CharField(max_length=100)
    canumber=models.IntegerField()
    cadate=models.DateTimeField(auto_now_add=True)
    uploaded=models.DateTimeField(auto_now_add=True)
    files_ca=models.FileField(upload_to='raw/ca/', blank=True, storage=RawMediaCloudinaryStorage())
    isverified = models.BooleanField(default = False)
    
    
    def __str__(self):
            return self.user.username

    # class Meta:
    #     ordering = ['-unit']
class Syllabus(models.Model):
    courseCode=models.CharField(max_length=20)
    title=models.CharField(max_length=100)
    fileupload=models.FileField(upload_to="media/",max_length=250,null=True,default=None)
    
class subscribers(models.Model):
    email=models.CharField(max_length=320)
    
#reports

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
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length = 140, blank=True)
    is_verified = models.BooleanField(default = False)
    created_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    