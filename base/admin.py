from django.contrib import admin

# Register your models here.
from .models import Courses
from .models import files
from .models import Syllabus
from .models import Report


admin.site.register(Courses)
admin.site.register(files)
admin.site.register(Syllabus)
admin.site.register(Report)