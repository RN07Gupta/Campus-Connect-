from cProfile import Profile
from django.http import HttpResponseForbidden
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Student, Faculty
from .models import Subject
import pandas as pd
from .models import Attendance, Student , Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'index.html')

# def log(request):
#     return render(request, 'log.html') 

# def reg(request):
#     return render(request, 'reg.html') 

# def std_dashboard(request):
#     return render(request, 'student_dashboard.html') 

# def cd_dashboard(request):
#     return render(request, 'coordinator_dashboard.html')

def logout(request):
    return render(request, 'log.html') 

def clubs(request):
    return render(request, 'clubs.html')

def events(request):
    return render(request, 'events.html')

def placements(request):   
    return render(request, 'placements.html')

def club_registration(request):
    return render(request, 'club_registration.html')

def event_registration(request):
    return render(request, 'event_registration.html')

def placement_apply(request):
    return render(request, 'placement_apply.html') 

# def upload_attendance(request):
#     if request.method == "POST":
#         excel_file = request.FILES["excel_file"]





# Home page
# def index(request):
    # return render(request, 'index.html')

# Registration
def register_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        department = request.POST.get("department")
        subject_code = request.POST.get('subject_code')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        user = User.objects.create_user(
            username=email,
            first_name=name,
            email=email,
            password=password
        )
        
        Profile.objects.create(
            user=user,
            role=role,
            department=department
            )

        if role == "Student":
            Student.objects.create(
                user=user,
                department=department,
            )

        elif role == "Coordinator":
            faculty = Faculty.objects.create(   # 🔥 STORE OBJECT
                user=user,
                department=department
            )

            SUBJECT_MAP = {
                "ML-101": "Machine Learning",
                "DA-102": "Data Analytics",
                "DAA-103": "Design & Analysis of Algorithms",
                "WT-104": "Web Technology",
                "ITCS-105": "ITCS",
                "DBMS-106": "Database Management System",
            }

            if subject_code:
                Subject.objects.create(
                    name=SUBJECT_MAP.get(subject_code),
                    subject_code=subject_code,
                    faculty=faculty      # ✅ PASS OBJECT
                )

        messages.success(request, "Registration successful! Please login.")
        return redirect("log")

    return render(request, "reg.html")



# Login


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("log")

        login(request, user)

        # ✅ ROLE DETECTION (CORRECT)
        if hasattr(user, "student"):
            return redirect("student_dashboard")

        elif hasattr(user, "faculty"):
            return redirect("coordinator_dashboard")

        else:
            messages.error(request, "Role not assigned")
            return redirect("log")

    return render(request, "log.html")




@login_required(login_url='log')
def coordinator_dashboard(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('log')  # or show error page

    faculty = request.user.faculty
    subject = faculty.subject 

    return render(request, "coordinator_dashboard.html", {
        "faculty": faculty,
        "subject": subject
    })
 





@login_required(login_url='log')
def upload_attendance(request, subject_id):
    subject = Subject.objects.get(id=subject_id)

    if not hasattr(request.user, 'faculty'):
        return HttpResponseForbidden()

    if subject.faculty != request.user.faculty:
        return HttpResponseForbidden()

    if request.method == "POST":
        df = pd.read_excel(request.FILES['excel_file'])

        for _, row in df.iterrows():
            email = str(row['email']).strip().lower()

            student = Student.objects.filter(
                user__username=email
            ).first()

            if not student:
                # 🔥 Skip unknown students
                continue

            Attendance.objects.update_or_create(
                student=student,
                subject=subject,
                date=row['date'],
                defaults={'status': row['status']}
            )

        messages.success(request, "Attendance uploaded successfully!")
        return redirect('coordinator_dashboard')

    
    
def student_dashboard(request):

    if not hasattr(request.user, 'student'):
        return redirect('log')   # or show "Not authorized"

    student = request.user.student

    subjects = Subject.objects.filter(
        attendance__student=student
    ).distinct()

    attendance_data = []

    for subject in subjects:
        total = Attendance.objects.filter(
            student=student,
            subject=subject
        ).count()

        present = Attendance.objects.filter(
            student=student,
            subject=subject,
            status='Present'
        ).count()

        percentage = (present / total) * 100 if total else 0

        attendance_data.append({
            'subject': subject.name,
            'total': total,
            'present': present,
            'percentage': round(percentage, 2)
        })

    return render(
        request,
        'student_dashboard.html',
        {'attendance_data': attendance_data},
        
    )