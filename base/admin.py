from django.contrib import admin

# Register your models here.
from .models import Courses, cafiles
from .models import files
# from .models import Syllabus
from .models import Report, subscribers , Profile
from .models import User_Email_verification


admin.site.register(Courses)
admin.site.register(files)
# admin.site.register(Syllabus)
admin.site.register(Report)
admin.site.register(subscribers)
admin.site.register(User_Email_verification)
admin.site.register(Profile)
admin.site.register(cafiles)