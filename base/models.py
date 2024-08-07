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
    
    def __str__(self):
            return self.courseCode

    
class cafiles(models.Model):
    courseCode=models.CharField(max_length=20)
    fileupload=models.FileField(upload_to='raw/ca/', blank=True, storage=RawMediaCloudinaryStorage())
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    teachername=models.CharField(max_length=100)
    canumber=models.IntegerField()
    cadate=models.DateTimeField()
    uploaded=models.DateTimeField(auto_now_add=True)
    isverified = models.BooleanField(default = False)
    
    
    def __str__(self):
            return self.user.username

    # class Meta:
    #     ordering = ['-unit']
# class Syllabus(models.Model):
#     courseCode=models.CharField(max_length=20)
#     title=models.CharField(max_length=100)
#     fileupload=models.FileField(upload_to="media/syllabus/",null=True,default=None,storage=RawMediaCloudinaryStorage())
    
class subscribers(models.Model):
    email=models.CharField(max_length=320)
    
    def __str__(self):
            return self.email

    
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
    profile_photo=models.FileField(upload_to="media/profile_photos/",null=True,default=None, storage=RawMediaCloudinaryStorage())
    
    def __str__(self):
        return self.user.username
    
    
    
class Discuss(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    views = models.IntegerField()
    votes = models.IntegerField()
    title = models.CharField(max_length = 1000, blank=True)
    Description = models.CharField(max_length = 8000, blank=True)
    tags = models.CharField(max_length = 100, blank=True)
    Time = models.DateTimeField(auto_now_add=True)
    Images = models.FileField(upload_to="media/discussions/",null=True,default=None, storage=RawMediaCloudinaryStorage())
    
    def __str__(self):
        return self.title
    
    
    
    
    