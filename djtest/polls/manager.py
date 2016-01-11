# coding=utf-8
import pdb

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from polls.classes import CourseInfo, GroupCheck
from polls.models import Manager, Student, Teacher, Course, Academy, Major, StudentToCourse, CourseInformation, Group, \
    StudentToGroup

def login(request):
    name = request.session.get('m_id', None)
    if name:
        return render(request, 'manager/manager_index.html')

    m_name = request.POST.get('manager_name')
    m_pwd = request.POST.get('manager_pwd')
    manager = Manager.objects.filter(m_name=m_name,
                                     m_pwd=m_pwd)
    if manager:
        request.session['m_name'] = m_name
        return render(request, 'manager/manager_index.html')
    else:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

def index(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    return render(request, 'manager/manager_index.html')

def student(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    student = Student.objects.all()
    return render(request, 'manager/manager_student.html', {'student':student})

def studentAdd(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    academy = Academy.objects.all()
    major = Major.objects.all()
    return render(request, 'manager/manager_student_add.html', {'academy':academy, 'major':major})

def studentSubmit(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    student_id = request.POST.get('student_id', None)

    check_student = Student.objects.filter(s_id=student_id)
    if check_student:
        return render(request, 'manager/manager_result.html', {'status':1})

    student_pwd = request.POST.get('password', None)
    student_name = request.POST.get('student_name', None)
    student_grade = request.POST.get('student_grade',None)
    student_class = request.POST.get('student_class', None)
    student_mail = request.POST.get('student_mail', None)
    student_academy = request.POST.get('student_academy', None)
    academy = Academy.objects.get(a_id=student_academy)
    student_major = request.POST.get('student_major', None)
    major = Major.objects.get(m_id=student_major)

    student = Student(s_id=student_id,
                      s_name=student_name,
                      s_pwd=student_pwd,
                      s_grade=student_grade,
                      s_class=student_class,
                      s_mail=student_mail,
                      s_academy=academy,
                      s_major=major)
    student.save()
    return render(request, 'manager/manager_result.html', {'status':0})

def studentInfo(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    student_id = request.POST.get('student_id', None)
    student = Student.objects.get(s_id=student_id)
    course = student.get_student.all()
    group = student.sTg_student.all()
    return render(request, 'manager/manager_student_info.html', {'student': student, 'course': course, 'group': group})

def stuModify(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    student_id = request.GET.get('sid', None)
    student = Student.objects.get(s_id=student_id)

    return render(request, 'manager/manager_student_modify.html', {'student': student})

def stuModCaG(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    student_id = request.GET.get('sid', None)
    student = Student.objects.get(s_id=student_id)
    sTc = student.get_student.all().order_by('c_id__c_id')
    group = []
    for c in sTc:
        temp = c.c_id.group_course.get()
        group.append(temp)
    sTg = student.sTg_student.all().order_by('g_id__g_course__c_id')
    result = calculateGroup(group, sTg)
    for r in result:
        r.set_student(student)
    return render(request, 'manager/manager_student_modCaG.html', {'student': student, 'sTc': sTc, 'sTg': result})

def stuSearch(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    student_id = request.POST.get('student_id', None)
    if not student_id:
        return render(request, 'manager/manager_student_search.html')
    else:
        student = Student.objects.filter(Q(s_id=student_id) | Q(s_name__contains=student_id))
        if not student:
            return render(request, 'manager/manager_student_search.html', {'status': 0})
        else:
            return render(request, 'manager/manager_student_search.html', {'status': 1, 'student': student})

def stuCouDel(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    student_id = request.POST.get('student_id', None)
    course_id = request.POST.get('course_id', None)
    student = Student.objects.get(s_id=student_id)
    course = Course.objects.get(c_id=course_id)
    group = course.group_course.get()
    sTc = StudentToCourse.objects.filter(s_id=student, c_id=course)
    sTg = StudentToGroup.objects.filter(s_id=student, g_id=group)
    if sTg:
        return render(request, 'manager/manager_result.html', {'status': 2})
    if sTc:
        sTc.delete()
        return render(request, 'manager/manager_result.html', {'status': 4, 'student_id': student_id})
    else:
        return render(request, 'manager/manager_result.html', {'status': 3})

def stuGroDel(request):
    # 踢出讨论组清空数据？？
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    student_id = request.POST.get('student_id', None)
    group_id = request.POST.get('group_id', None)
    student = Student.objects.get(s_id=student_id)
    group = Group.objects.get(id=group_id)
    sTg = StudentToGroup.objects.filter(s_id=student, g_id=group)
    if sTg:
        sTg.delete()
        return render(request, 'manager/manager_result.html', {'status': 4, 'student_id': student_id})
    else:
        return render(request, 'manager/manager_result.html', {'status': 3})

def teacher(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    teacher = Teacher.objects.all()
    return render(request, 'manager/manager_teacher.html', {'teacher':teacher})

def teacherAdd(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    academy = Academy.objects.all()
    return render(request, 'manager/manager_teacher_add.html', {'academy':academy})

def teacherSubmit(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    teacher_id = request.POST.get('teacher_id', None)
    check_teacher = Teacher.objects.filter(t_id=teacher_id)
    if check_teacher:
        return render(request, 'manager/manager_result.html', {'status':1})

    teacher_name = request.POST.get('teacher_name', None)
    teacher_pwd = request.POST.get('password', None)
    teacher_mail = request.POST.get('teacher_mail', None)
    teacher_academy = request.POST.get('teacher_academy', None)
    academy = Academy.objects.get(a_id=teacher_academy)

    teacher = Teacher(t_id=teacher_id,
                      t_name=teacher_name,
                      t_pwd=teacher_pwd,
                      t_mail=teacher_mail,
                      t_academy=academy)
    teacher.save()
    return render(request, 'manager/manager_result.html', {'status':0})

def teacherInfo(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    teacher_id = request.POST.get('teacher_id', None)
    teacher = Teacher.objects.get(t_id=teacher_id)
    course = teacher.course_teacher.all()
    group = teacher.group_teacher.all()
    return render(request, 'manager/manager_teacher_info.html', {'teacher':teacher, 'course':course, 'group': group})

def teaModify(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    teacher_id = request.GET.get('tid', None)
    teacher = Teacher.objects.get(t_id=teacher_id)
    return render(request, 'manager/manager_teacher_modify.html', {'teacher': teacher})

def teaModCaG(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    teacher_id = request.GET.get('tid', None)
    teacher = Teacher.objects.get(t_id=teacher_id)
    course = teacher.course_teacher.all().order_by('c_id')
    group = teacher.group_teacher.all().order_by('g_course__c_id')
    return render(request, 'manager/manager_teacher_modCaG.html', {'teacher': teacher, 'course': course, 'group': group})

def course(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    course = Course.objects.all()
    return render(request, 'manager/manager_course.html', {'course':course})

def courseAdd(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    academy = Academy.objects.all()
    teacher = Teacher.objects.all()
    major = Major.objects.all()
    return render(request, 'manager/manager_course_add.html', {'academy':academy, 'teacher':teacher, 'major':major})

def courseSubmit(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    course_id = request.POST.get('course_id', None)
    check_course = Course.objects.filter(c_id=course_id)
    if check_course:
        return render(request, 'manager/manager_result.html', {'status':1})

    course_name = request.POST.get('course_name', None)
    course_academy = request.POST.get('course_academy', None)
    academy = Academy.objects.get(a_id=course_academy)
    course_major = request.POST.get('course_major', None)
    major = Major.objects.get(m_id=course_major)
    course_teacher = request.POST.get('course_teacher', None)
    teacher = Teacher.objects.get(t_id=course_teacher)

    course = Course(c_id=course_id,
                    c_name=course_name,
                    c_academy=academy,
                    c_major=major,
                    c_teacher=teacher)
    course.save()
    return render(request, 'manager/manager_result.html', {'status':0})

def courseInfo(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', \
                                                              'pwd':'manager_pwd'})

    course_id = request.GET.get('cid', None)
    course = Course.objects.get(c_id=course_id)
    course_info = CourseInformation.objects.filter(ci_id=course)
    schedule = calculateSchedule(course_info)
    group = Group.objects.get(g_course=course)
    return render(request, 'manager/manager_course_info.html', {'course': course, 'schedule': schedule, \
                                                                'group': group})

def courseModify(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url': '/manager/login/', 'id': 'manager_name', \
                                                              'pwd': 'manager_pwd'})

    course_id = request.GET.get('cid', None)
    teacher = Teacher.objects.all()
    academy = Academy.objects.all()
    course = Course.objects.get(c_id=course_id)
    information = CourseInformation.objects.filter(ci_id=course)

    return render(request, 'manager/manager_course_modify.html', {'course': course, 'teacher': teacher, \
                                                                  'academy': academy, 'information': information})

def academy(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    academy = Academy.objects.all()
    return render(request, 'manager/manager_academy.html', {'academy':academy})

def academyInfo(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    academy_id = request.GET.get('aid', None)
    if not academy_id:
        return render(request, 'manager/manager_result.html', {'status': -1})
    else:
        academy = Academy.objects.get(a_id=academy_id)
        teacher = academy.teacher_academy.all()
        course = academy.course_academy.all()
        return render(request, 'manager/manager_academy_info.html', {'academy': academy, 'teacher': teacher, 'course': course})

def academyAdd(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    return render(request, 'manager/manager_academy_add.html')

def academySubmit(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    academy_id = request.POST.get('academy_id', None)
    check_academy = Academy.objects.filter(a_id=academy_id)
    if check_academy:
        return render(request, 'manager/manager_result.html', {'status':1})

    academy_name = request.POST.get('academy_name', None)

    academy = Academy(a_id=academy_id,
                      a_name=academy_name)
    academy.save()
    return render(request, 'manager/manager_result.html', {'status':0})

def academyDel(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    academy_id = request.POST.get('academy_id', None)
    academy = Academy.objects.get(a_id=academy_id)
    check_student = academy.student_academy.all()
    check_teacher = academy.teacher_academy.all()
    check_course = academy.course_academy.all()
    check_major = academy.major_academy.all()
    if check_student or check_teacher or check_major or check_course:
        return render(request, 'manager/manager_result.html', {'status':2})

    Academy.objects.get(a_id=academy_id).delete()
    return render(request, 'manager/manager_result.html', {'status':0})

def major(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    major = Major.objects.all()
    return render(request, 'manager/manager_major.html', {'major':major})

def majorAdd(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    academy = Academy.objects.all()
    return render(request, 'manager/manager_major_add.html', {'academy':academy})

def majorSubmit(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    major_id = request.POST.get('major_id', None)
    check_major = Major.objects.filter(m_id=major_id)
    if check_major:
        return render(request, 'manager/manager_result.html', {'status':1})

    major_name = request.POST.get('major_name', None)
    major_academy = request.POST.get('major_academy', None)
    academy = Academy.objects.get(a_id=major_academy)

    major = Major(m_id=major_id,
                  m_name=major_name,
                  m_academy=academy)
    major.save()
    return render(request, 'manager/manager_result.html', {'status':0})

def majorDel(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    major_id = request.POST.get('major_id', None)
    major = Major.objects.get(m_id=major_id)
    check_student = major.student_major.all()
    check_course = major.course_major.all()
    if check_course or check_student:
        return render(request, 'manager/manager_result.html', {'status':2})
    Major.objects.get(m_id=major_id).delete()
    return render(request, 'manager/manager_result.html', {'status':0})

def groupStuAdd(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    group_id = request.POST.get('group_id', None)
    student_id = request.POST.get('student_id', None)
    group = Group.objects.get(id=group_id)
    if group.g_total == group.g_number:
        return render(request, 'manager/manager_result.html', {'status': 5})
    student = Student.objects.get(s_id=student_id)

    sTg = StudentToGroup(s_id=student,
                         g_id=group)
    group.g_number += 1
    group.save()
    sTg.save()
    return render(request, 'manager/manager_result.html', {'status': 6, 'student': student, 'group': group})

def groupStuDel(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    group_id = request.POST.get('group_id', None)
    student_id = request.POST.get('student_id', None)
    group = Group.objects.get(id=group_id)
    student = Student.objects.get(s_id=student_id)

    sTg = StudentToGroup.objects.filter(s_id=student, g_id=group)
    if not sTg:
        return render(request, 'manager/manager_result.html', {'status': 7})

    group.g_number -= 1
    group.save()
    sTg.delete()
    return render(request, 'manager/manager_result.html', {'status': 8, 'student': student, 'group': group})

def groupSearch(request):
    name = request.session.get('m_name', None)
    if not name:
        return render(request, 'manager/manager_login.html', {'url':'/manager/login/', 'id':'manager_name', 'pwd':'manager_pwd'})

    group_info = request.POST.get('group_info', None)
    group = Group.objects.filter(g_name__contains=group_info)
    if group:
        return render(request, 'manager/manager_group_search.html', {'status': 0, 'group': group})

    course = Course.objects.filter(c_name__contains=group_info)
    group = []
    for cou in course:
        group.append(cou.group_course.get())
    if group:
        return render(request, 'manager/manager_group_search.html', {'status': 0, 'group': group})

    teacher = Teacher.objects.filter(t_name__contains=group_info)
    for tea in teacher:
        group.append(tea.group_teacher.get())
    if group:
        return render(request, 'manager/manager_group_search.html', {'status': 0, 'group': group})
    else:
        return render(request, 'manager/manager_group_search.html', {'status': 1})

def calculateSchedule(course_info):
    result = []
    j = 0
    for i in range(1, 41):
        if i % 8 == 1:
            tempCourse = CourseInfo(1, None, '第%d、%d节课' % ((i / 8)*2 + 1, (i / 8)*2 + 2))
        elif i % 8 == 0:
            if course_info[j].ci_time == i:
                tempCourse = CourseInfo(2, course_info[j], '')
                if j + 1 == len(course_info):
                    j = j
                else:
                    j += 1
            else:
                tempCourse = CourseInfo(3, None, '')
        elif course_info[j].ci_time == i:
            tempCourse = CourseInfo(4, course_info[j], '')
            if j + 1 == len(course_info):
                j = j
            else:
                j += 1
        else:
            tempCourse = CourseInfo(5, None, '')

        result.extend([tempCourse])

    return result

def calculateGroup(group_info, sTg_info):
    result = []
    j = 0
    if len(sTg_info) == 0:
        for i in group_info:
            tempGroup = GroupCheck(0, i)
            result.extend([tempGroup])
    else:
        for i in group_info:
            if sTg_info[j].g_id.g_course.c_id == i.g_course.c_id:
                tempGroup = GroupCheck(1, i)
                if j + 1 == len(sTg_info):
                    j = j
                else:
                    j += 1
            else:
                tempGroup = GroupCheck(0, i)
            result.extend([tempGroup])

    return result