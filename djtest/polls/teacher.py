# coding=utf-8
import pdb
from datetime import date, datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from polls.classes import CourseInfo, PageInfo
from polls.models import Teacher, Group, StudentToGroup, Course, CourseInformation, Information, Student, Academy

def register(request):
    academy = Academy.objects.all()
    return render(request, 'teacher/teacher_register.html', {'academy': academy})

def registerSubmit(request):
    teacher_id = request.POST.get('teacher_id', None)
    check_tea = Teacher.objects.filter(t_id=teacher_id)
    if check_tea:
        return render(request, 'base/result.html', {'status': 1})
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
    return render(request, 'base/result.html', {'status': 2})

def login(request):
    name = request.session.get('t_id', None)
    if name:
        teacher = Teacher.objects.get(t_id=name)
        return render(request, 'teacher/teacher_index.html', {'teacher':teacher})

    teacher_id = request.POST.get('teacher_id', None)
    teacher_pwd = request.POST.get('teacher_pwd', None)
    teacher = Teacher.objects.filter(t_id=teacher_id,
                                     t_pwd=teacher_pwd)
    if teacher:
        request.session['t_id'] = teacher_id
        return render(request, 'teacher/teacher_index.html', {'teacher':teacher[0]})
    else:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

def index(request):
    name = request.session.get('t_id', None)
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

    teacher = Teacher.objects.get(t_id=name)
    return render(request, 'teacher/teacher_index.html', {'teacher':teacher})

def mycourse(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

    teacher = Teacher.objects.get(t_id=name)
    course = teacher.course_teacher.all()

    sysPage = Paginator(course, 10)
    current = request.GET.get('page', None)
    if not current:
        current = 1
    else:
        current = int(current)

    if current > sysPage.num_pages:
        return render(request, 'student/student_result.html', {'status': 12})

    page = PageInfo(current, sysPage.num_pages)
    course = sysPage.page(current).object_list

    return render(request, 'teacher/teacher_mycourse.html', {'course':course, 'page': page})

def courseInfo(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

    course_id = request.GET.get('cid', None)
    course = Course.objects.get(c_id=course_id)
    course_info = CourseInformation.objects.filter(ci_id=course)
    schedule = calculateSchedule(course_info)
    group = Group.objects.filter(g_course=course)
    if group:
        group = group[0]
    else:
        group = None
    return render(request, 'teacher/teacher_course_info.html', {'course': course, 'schedule': schedule, 'group': group})

def mygroup(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

    teacher = Teacher.objects.get(t_id=name)
    group = Group.objects.filter(g_teacher=teacher)

    sysPage = Paginator(group, 10)
    current = request.GET.get('page', None)
    if not current:
        current = 1
    else:
        current = int(current)

    if current > sysPage.num_pages:
        return render(request, 'student/student_result.html', {'status': 12})

    page = PageInfo(current, sysPage.num_pages)
    group = sysPage.page(current).object_list


    return render(request, 'teacher/teacher_mygroup.html', {'group':group, 'page': page})

def groupInfo(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

    course_id = request.POST.get('group_id', None)
    course = Course.objects.get(c_id=course_id)
    group = Group.objects.get(g_course=course)
    sTg = group.sTg_group.all()
    return render(request, 'teacher/teacher_group_info.html', {'group': group, 'sTg': sTg})

def groupCreate(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

    course_id = request.POST.get('group_course', None)
    course = Course.objects.get(c_id=course_id)
    group_name = request.POST.get('group_name', None)
    group = Group(g_name=group_name,
                  g_teacher=course.c_teacher,
                  g_total=course.c_total,
                  g_course=course)
    group.save()
    return render(request, 'teacher/teacher_result.html', {'status': 0})

def information(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

    information_list = Information.objects.filter(i_to=name)
    for information in information_list:
        if information.i_type == 1 or information.i_type == 7:
            student = Student.objects.get(s_id=information.i_from)
            information.i_from = student.s_name
        elif information.i_type == 2:
            information.i_from = '系统消息'

    sysPage = Paginator(information_list, 10)
    current = request.GET.get('page', None)
    if not current:
        current = 1
    else:
        current = int(current)

    if current > sysPage.num_pages:
        return render(request, 'student/student_result.html', {'status': 12})

    page = PageInfo(current, sysPage.num_pages)
    information_list = sysPage.page(current).object_list

    return render(request, 'teacher/teacher_information.html', {'information': information_list, 'page': page})

def infoDetail(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

    information_id = request.POST.get('information_id', None)
    information = Information.objects.get(i_id=information_id)
    info_from = ''
    info_to = ''

    if information.i_type == 1 or information.i_type == 7:
        student = Student.objects.get(s_id=information.i_from)
        info_from = student.s_name
    elif information.i_type == 2:
        info_from = '系统消息'

    teacher = Teacher.objects.get(t_id=name)
    info_to = teacher.t_name
    return render(request, 'teacher/teacher_information_detail.html', {'information': information, 'info_from': info_from, 'info_to': info_to})

def infoResponse(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

    resp = request.GET.get('value', None)
    information_id = request.GET.get('id', None)
    information = Information.objects.get(i_id=information_id)
    information.i_status = True
    student_id = information.i_from
    student = Student.objects.get(s_id=student_id)
    teacher = Teacher.objects.get(t_id=name)
    information_type = 2
    information_to = student_id
    information_time = datetime.now()
    if resp == '1':
        sTg = StudentToGroup(s_id=student,
                             g_id=information.i_group)
        sTg.save()
        group = Group.objects.get(g_name=information.i_group.g_name)
        group.g_number += 1
        group.save()
        information_title = '%s老师已经同意了你的请求。' % (teacher.t_name)
        information_message = '%s老师已经同意了你的请求，你已经加入%s讨论组。' % (teacher.t_name, information.i_group.g_name)
    elif resp == '2':
        information_title = '%s老师拒绝了你的请求。' % (teacher.t_name)
        information_message = '很遗憾，%s老师拒绝了你的请求。' % (teacher.t_name)

    newInfo = Information(i_type=information_type,
                          i_to=information_to,
                          i_time=information_time,
                          i_title=information_title,
                          i_message=information_message)

    newInfo.save()
    information.save()
    return render(request, 'teacher/teacher_result.html', {'status': 1})

def deleteStu(request):
    # 在老师把学生踢出讨论组的同时 信息要不要也删除？？
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id': 'teacher_id', 'pwd': 'teacher_pwd'})

    student_id = request.POST.get('student_id', None)
    student = Student.objects.get(s_id=student_id)
    course_id = request.POST.get('group_id', None)
    course = Course.objects.get(c_id=course_id)
    group = Group.objects.get(g_course=course)
    teacher = Teacher.objects.get(t_id=name)

    information_tea_type = 8
    information_tea_from = name
    information_tea_title = '你将%s踢出了%s讨论组' % (student.s_name, group.g_name)
    information_tea_message = '你将%s踢出了%s讨论组' % (student.s_name, group.g_name)
    information_tea_time = datetime.now()

    information_tea = Information(i_from=information_tea_from,
                                  i_type=information_tea_type,
                                  i_time=information_tea_time,
                                  i_message=information_tea_message,
                                  i_title=information_tea_title)

    information_stu_type = 2
    information_stu_to = student_id
    information_stu_title = '你被%s踢出了%s讨论组' % (teacher.t_name, group.g_name)
    information_stu_message = '你被%s踢出了%s讨论组' % (teacher.t_name, group.g_name)
    information_stu_time = datetime.now()

    information_stu = Information(i_to=information_stu_to,
                                  i_type=information_stu_type,
                                  i_title=information_stu_title,
                                  i_message=information_stu_message,
                                  i_time=information_stu_time)

    StudentToGroup.objects.get(s_id=student, g_id=group).delete()
    group.g_number -= 1
    group.save()
    information_stu.save()
    information_tea.save()
    return render(request, 'teacher/teacher_result.html', {'status': 2, 'group': group, 'student': student})

def broadcast(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id': 'teacher_id', 'pwd': 'teacher_pwd'})

    information_from = request.POST.get('information_from', None)
    information_to = request.POST.get('information_to', None)
    information_title = request.POST.get('information_title', None)
    information_message = request.POST.get('information_message', None)
    information_time = datetime.now()
    information_status = True
    group = Group.objects.get(id=information_to)
    information = Information(i_from=information_from,
                              i_to=information_to,
                              i_type=3,
                              i_time=information_time,
                              i_title=information_title,
                              i_message=information_message,
                              i_status=information_status,
                              i_group=group)
    information.save()
    sTg = StudentToGroup.objects.filter(g_id=group)
    for s in sTg:
        tempInfo = Information(i_from=s.g_id.id,
                               i_to=s.s_id.s_id,
                               i_type=5,
                               i_time=information_time,
                               i_title=information_title,
                               i_message=information_message,
                               i_group=group)
        tempInfo.save()
    return render(request, 'teacher/teacher_result.html', {'status': 3})

def sendmsg(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id': 'teacher_id', 'pwd': 'teacher_pwd'})

    s_id = request.GET.get('s', None)
    if s_id:
        student = Student.objects.get(s_id=s_id)
        return render(request, 'teacher/teacher_sendmsg.html', {'status': 1, 'student': student})
    else:
        return render(request, 'teacher/teacher_search.html')

# 老师发送消息只有两种情况，一种是群发，在broadcast函数中；另一种是私信发送或者回复，对象都是学生
def sendmsgSubmit(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id': 'teacher_id', 'pwd': 'teacher_pwd'})

    information_type = int(request.POST.get('information_type', None))
    information_to = request.POST.get('information_to', None)
    if information_type == 1:
        information_type = 4
    elif information_type == 2:
        information_type = 4
        student = Student.objects.get(Q(s_id=information_to) | Q(s_name=information_to))
        information_to = student.s_id
    information_title = request.POST.get('information_title', None)
    information_msg = request.POST.get('information_message', None)
    information_time = datetime.now()
    information_from = name
    information = Information(i_from=information_from,
                              i_to=information_to,
                              i_type=information_type,
                              i_title=information_title,
                              i_message=information_msg,
                              i_time=information_time)
    information.save()
    return render(request, 'teacher/teacher_result.html', {'status': 5})

def search(request):
    name = request.session.get('t_id')
    if not name:
        return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id': 'teacher_id', 'pwd': 'teacher_pwd'})

    student_id = request.POST.get('student_id', None)
    if not student_id:
        return render(request, 'teacher/teacher_search.html')
    else:
        student = Student.objects.filter(Q(s_id=student_id) | Q(s_name__contains=student_id))
        if not student:
            return render(request, 'teacher/teacher_search.html', {'status': 0})
        else:
            return render(request, 'teacher/teacher_search.html', {'status': 1, 'student': student})

def quit(request):
    try:
        del request.session['t_id']
    except KeyError:
        pass
    return render(request, 'teacher/teacher_login.html', {'url':'/teacher/login/', 'id':'teacher_id', 'pwd':'teacher_pwd'})

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