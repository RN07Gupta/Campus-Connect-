from django.contrib import admin
from .models import Profile , Student, Faculty , Subject, Attendance    

# Register your models here.

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Profile) 
admin.site.register(Subject)
admin.site.register(Attendance)