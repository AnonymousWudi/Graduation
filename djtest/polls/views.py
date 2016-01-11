from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from polls.models import Student, Teacher


def index(request):
    name = request.session.get('s_id', None)
    if name:
        student = Student.objects.get(s_id=name)
        return render(request, 'student/student_index.html', {'student':student})
    return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

def teacher(request):
    name = request.session.get('t_id', None)
    if name:
        teacher = Teacher.objects.get(t_id=name)
        return render(request, 'teacher/teacher_index.html', {'teacher':teacher})
    return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

def student(request):
    name = request.session.get('s_id', None)
    if name:
        student = Student.objects.get(s_id=name)
        return render(request, 'student/student_index.html', {'student':student})

    return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

def manager(request):
    name = request.session.get('m_id', None)
    if name:
        return render(request, 'manager/manager_index.html')
    return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})