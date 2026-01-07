from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.user.first_name 

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.first_name}" 
    


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    

    def __str__(self):
        return f"{self.user.first_name}" 
    
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20, unique=True)
    faculty = models.OneToOneField(
        Faculty,
        on_delete=models.CASCADE,
        related_name="subject"
    )

    def __str__(self):
        return f"{self.subject_code} - {self.name}"



class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[('Present','Present'), ('Absent','Absent')]
    )

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date}" 

    