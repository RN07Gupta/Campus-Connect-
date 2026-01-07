"""
URL configuration for campus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from student import views
# from .views import upload_attendance


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('login/', views.login_user, name='log'),          # login page
    path('register/', views.register_user, name='register'),       # registration page

    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('coordinator/dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),

    # path('logout/', views.logout_user, name='logout'),  # logout
    
    path('clubs/', views.clubs, name='clubs'),
    path('events/', views.events, name='events'),   
    path('placements/', views.placements, name='placements'),
    path('club_registration/', views.club_registration, name='club_registration'),
    path('events/event_registration.html', views.event_registration, name='event_registration'),
    path('placements/placement_apply.html', views.placement_apply, name='placement_apply'),
    path("upload-attendance/", views.upload_attendance, name="upload_attendance"),
    path("attendance/upload/<int:subject_id>/",views.upload_attendance,name="upload_attendance")
] 

