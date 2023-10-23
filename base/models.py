from django.db import models


# Create your models here.

class Courses(models.Model):
    name=models.CharField(max_length=20)

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