# coding=utf-8
import os
import pdb
from datetime import *

from django import forms
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext

from polls.classes import CourseInfo, GroupCheck, PageInfo, HomeworkCheck
from polls.models import Student, Course, StudentToCourse, CourseInformation, Group, StudentToGroup, Information, \
    Teacher, Academy, Major, Notice, User, Chat, CourseGroup, Homework, StudentToHomework

FILE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def register(request):
    academy = Academy.objects.all()
    major = Major.objects.all()
    return render(request, 'student/student_register.html', {'academy': academy, 'major': major})

def registerSubmit(request):
    student_id = request.POST.get('student_id', None)
    check_stu = Student.objects.filter(s_id=student_id)
    if check_stu:
        return render(request, 'base/result.html', {'status': 1})
    student_name = request.POST.get('student_name', None)
    student_pwd = request.POST.get('password', None)
    student_grade = request.POST.get('student_grade', None)
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
    return render(request, 'base/result.html', {'status': 3})

def login(request):
    name = request.session.get('s_id', None)
    if name:
        student = Student.objects.get(s_id=name)
        return render(request, 'student/student_index.html', {'student':student})

    student_id = request.POST.get('student_id', None)
    student_pwd = request.POST.get('student_pwd', None)
    student = Student.objects.filter(s_id=student_id,
                                     s_pwd=student_pwd)
    if student:
        request.session['s_id'] = student_id
        return render(request, 'student/student_index.html', {'student':student[0]})
    else:
        return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

def index(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

    student = Student.objects.get(s_id=name)
    return render(request, 'student/student_index.html', {'student':student})

def course(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

    course = Course.objects.all()
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

    return render(request, 'student/student_course.html', {'course':course, 'page': page})

def courseInfo(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

    course_id = request.POST.get('course_id', None)
    course = Course.objects.get(c_id=course_id)
    student_id = request.session.get('s_id', None)
    student = Student.objects.get(s_id=student_id)
    check_select = StudentToCourse.objects.filter(s_id=student,
                                                  c_id=course)
    select = 0
    if check_select:
        select = 1

    course_info = CourseInformation.objects.filter(ci_id=course)
    schedule = calculateSchedule(course_info)
    return render(request, 'student/student_course_info.html', {'course':course, 'select':select, 'schedule':schedule})

def mycourse(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

    student_id = request.session.get('s_id')
    student = Student.objects.get(s_id=student_id)
    course = StudentToCourse.objects.filter(s_id=student)

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

    return render(request, 'student/student_mycourse.html', {'course':course, 'page': page})

def addcourse(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

    student_id = request.session.get('s_id', None)
    student = Student.objects.get(s_id=student_id)
    course_id = request.POST.get('course_id', None)
    course = Course.objects.get(c_id=course_id)
    if course.c_total <= course.c_number:
        return render(request, 'student/student_result.html', {'status': 8})
    check_sTc = StudentToCourse.objects.filter(s_id=student,
                                               c_id=course)
    if check_sTc:
        return render(request, 'student/student_result.html', {'status':1})

    sTc = StudentToCourse(s_id=student,
                          c_id=course)
    sTc.save()
    course.c_number += 1
    course.save()

    return render(request, 'student/student_result.html', {'status':0})

def removecourse(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    student_id = request.session.get('s_id', None)
    student = Student.objects.get(s_id=student_id)
    course_id = request.POST.get('course_id', None)
    course = Course.objects.get(c_id=course_id)
    check_sTc = StudentToCourse.objects.filter(s_id=student,
                                               c_id=course)
    if not check_sTc:
        return render(request, 'student/student_result.html', {'status': 2})

    group = Group.objects.filter(g_course=course)
    if group:
        sTg = StudentToGroup.objects.filter(g_id=group[0], s_id=student)
        if sTg:
            return render(request, 'student/student_result.html', {'status': 6})

    StudentToCourse.objects.get(s_id=student, c_id=course).delete()
    course.c_number -= 1
    course.save()
    return render(request, 'student/student_result.html', {'status': 0})

def couSearch(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    course_info = request.POST.get('course_id', None)
    course = Course.objects.filter(Q(c_id__contains=course_info) | Q(c_name__contains=course_info))
    if not course:
        return render(request, 'student/student_course.html', {'status': 1})

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

    return render(request, 'student/student_course.html', {'status': 0, 'course':course, 'page': page})

def group(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

    group = Group.objects.all().order_by('g_course__c_id')
    student = Student.objects.get(s_id=name)
    sTg = StudentToGroup.objects.filter(s_id=student).order_by('g_id__g_course__c_id')
    result = calculateGroup(group, sTg)

    sysPage = Paginator(result, 10)
    current = request.GET.get('page', None)
    if not current:
        current = 1
    else:
        current = int(current)

    if current > sysPage.num_pages:
        return render(request, 'student/student_result.html', {'status': 12})

    page = PageInfo(current, sysPage.num_pages)
    result = sysPage.page(current).object_list

    return render(request, 'student/student_group.html', {'group':result, 'page': page})

def mygroup(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

    student = Student.objects.get(s_id=name)
    sTg = StudentToGroup.objects.filter(s_id=student).order_by('g_id__g_course__c_id')

    sysPage = Paginator(sTg, 10)
    current = request.GET.get('page', None)
    if not current:
        current = 1
    else:
        current = int(current)

    if current > sysPage.num_pages:
        return render(request, 'student/student_result.html', {'status': 12})

    page = PageInfo(current, sysPage.num_pages)
    sTg = sysPage.page(current).object_list

    return render(request, 'student/student_mygroup.html', {'group':sTg, 'page': page})

def groupInfo(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

    course_id = request.POST.get('group_id', None)
    course = Course.objects.get(c_id=course_id)
    group = Group.objects.get(g_course=course)
    sTg = group.sTg_group.all()
    return render(request, 'student/student_group_info.html', {'group':group, 'sTg':sTg, 'me': name})

# 对于重复的申请进行刷新时间操作，该功能已实现
def groupadd(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    information_type = 1
    course_id = request.POST.get('group_id', None)
    course = Course.objects.get(c_id=course_id)
    student = Student.objects.get(s_id=name)

    check_sTc = StudentToCourse.objects.filter(s_id=student, c_id=course)
    if not check_sTc:
        return render(request, 'student/student_result.html', {'status': 7})

    information_to = course.c_teacher.t_id
    information_from = name
    information_title = '老师，我想加入您的讨论组'
    information_message = '%s老师您好，我是%s。我想加入您%s课程的讨论组，希望您同意。' % (course.c_teacher.t_name, student.s_name, course.c_name)
    information_time = datetime.now()
    information_group = Group.objects.get(g_course=course)

    check_info = Information.objects.filter(i_type=information_type,
                                            i_from=information_from,
                                            i_to=information_to,
                                            i_title=information_title,
                                            i_message=information_message)
    if check_info:
        if check_info[0].i_status == False:
            check_info[0].i_time = datetime.now()
        check_info[0].save()
        return render(request, 'student/student_result.html', {'status': 9})

    else:
        information = Information(i_type=information_type,
                                  i_from=information_from,
                                  i_to=information_to,
                                  i_title=information_title,
                                  i_message=information_message,
                                  i_time=information_time,
                                  i_group=information_group)
        information.save()
        return render(request, 'student/student_result.html', {'status': 9})

def groupquit(request):
    # 退出讨论组的时候会把所有的消息全部清空,该功能暂未实现

    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    student = Student.objects.get(s_id=name)
    course_id = request.POST.get('group_id', None)
    course = Course.objects.get(c_id=course_id)
    group = Group.objects.get(g_course=course)
    group_check = StudentToGroup.objects.filter(g_id=group)
    if not group_check:
        return render(request, 'student/student_result.html', {'status': 4})

    StudentToGroup.objects.get(s_id=student, g_id=group).delete()
    group.g_number -= 1
    group.save()
    return render(request, 'student/student_result.html', {'status': 0})

def information(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    information_list = Information.objects.filter(i_to=name)
    sysPage = Paginator(information_list, 10)

    current = request.GET.get('page', None)
    if not current:
        current = 1
    else:
        current = int(current)

    if current > sysPage.num_pages:
        return render(request, 'student/student_result.html', {'status': 12})

    page = PageInfo(current, sysPage.num_pages)

    student = Student.objects.get(s_id=name)
    for information in information_list:
        if information.i_type == 2:
            information.i_from = '系统消息'
        elif information.i_type == 5:
            information.i_from = '%s' % (information.i_group.g_name)
        elif information.i_type == 4:
            teacher = Teacher.objects.get(t_id=information.i_from)
            information.i_from = teacher.t_name
        elif information.i_type == 6:
            student = Student.objects.get(s_id=information.i_from)
            information.i_from = student.s_name

        information.i_to = student.s_name

    information_list = sysPage.page(current).object_list

    return render(request, 'student/student_information.html', {'information': information_list, 'page': page})

def infoDetail(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    information_id = request.POST.get('information_id', None)
    information = Information.objects.get(i_id=information_id)
    information.i_status = True
    information.save()
    info_from = ''

    if information.i_type == 2:
        info_from = '系统消息'
    elif information.i_type == 5:
        info_from = '%s' % (information.i_group.g_name)
    elif information.i_type == 4:
        teacher = Teacher.objects.get(t_id=information.i_from)
        info_from = teacher.t_name
    elif information.i_type == 6:
        student = Student.objects.get(s_id=information.i_from)
        info_from = student.s_name

    student = Student.objects.get(s_id=name)
    info_to = student.s_name

    return render(request, 'student/student_information_detail.html', {'information': information, 'info_from': info_from, 'info_to': info_to})

def myself(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    student = Student.objects.get(s_id=name)
    return render(request, 'student/student_myself.html', {'student': student})

def sendmsg(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    t_id = request.GET.get('t', None)
    s_id = request.GET.get('s', None)
    if t_id:
        teacher = Teacher.objects.get(t_id=t_id)
        return render(request, 'student/student_sendmsg.html', {'status': 1, 'teacher': teacher})
    elif s_id:
        student = Student.objects.get(s_id=s_id)
        return render(request, 'student/student_sendmsg.html', {'status': 2, 'student': student})
    else:
        return render(request, 'student/student_sendmsg.html', {'status': 3})

# 此函数逻辑有问题 无法判断同名学生 也就是说如果用户输入的是名字 而且是重名的名字 那就暂时无法处理
def sendmsgSubmit(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    information_type = int(request.POST.get('information_type', None))
    information_to = request.POST.get('information_to', None)
    information_title = request.POST.get('information_title', None)
    information_msg = request.POST.get('information_message', None)
    information_from = name
    if information_type == 1:
        information_type = 7
    elif information_type == 2:
        information_type = 6
    elif information_type == 0:
        student = Student.objects.filter(Q(s_id=information_to) | Q(s_name=information_to))
        teacher = Teacher.objects.filter(Q(t_id=information_to) | Q(t_name=information_to))
        if student:
            information_type = 7
            information_to = student[0].s_id
        elif teacher:
            information_type = 6
            information_to = teacher[0].t_id
        else:
            return render(request, 'student/student_result.html', {'status': 10})
    information_time = datetime.now()
    information = Information(i_type=information_type,
                              i_from=information_from,
                              i_to=information_to,
                              i_title=information_title,
                              i_message=information_msg,
                              i_time=information_time)
    information.save()
    return render(request, 'student/student_result.html', {'status': 11})

def schedule(request):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    student = Student.objects.get(s_id=name)
    sTc = student.get_student.all()
    course = []
    for s in sTc:
        course_info = CourseInformation.objects.filter(ci_id=s.c_id)
        course.extend(course_info)

    course = bbsort(course)
    schedule = calculateSchedule(course)
    return render(request, 'student/student_schedule.html', {'schedule': schedule})

def courseIndex(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    course = Course.objects.get(c_id=course_id)
    return render(request, 'student/student_course_index.html', {'course': course})

# 日程需要展示本周的上课情况，所以课程信息最好按照日期来存储比较好，这一点需要改进
def courseSchedule(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    courses = CourseInformation.objects.filter(ci_id=Course.objects.get(c_id=course_id))
    schedule = calculateSchedule(courses)
    course = Course.objects.get(c_id=course_id)
    return render(request, 'student/student_course_schedule.html', {'schedule': schedule, 'course': course})

# 通知中只会显示关于该课程并且接收通知的人是登录用户的
def courseNotice(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', 'pwd': 'student_pwd'})

    course = Course.objects.get(c_id=course_id)
    notice = Notice.objects.filter(n_course=course, n_to=name)
    return render(request, 'student/student_course_notice.html', {'notice': notice, 'course': course})

# 分页，查找功能需要添加
def courseNamelist(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', \
                                                              'pwd': 'student_pwd'})

    course = Course.objects.get(c_id=course_id)
    sTc = StudentToCourse.objects.filter(c_id=course)
    return render(request, 'student/student_course_namelist.html', {'sTc': sTc, 'course': course})

# 跳转到上传文件页面 暂未与文件下载功能相关联
'''
def courseResource(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', \
                                                              'pwd': 'student_pwd'})

    course = Course.objects.get(c_id=course_id)
    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            headImg = uf.cleaned_data['headImg']
            handle_uploaded_file(headImg, course)
            #写入数据库
            user = User()
            user.username = username
            user.headImg = headImg
            user.save()
            return HttpResponse('upload ok!')
    else:
        uf = UserForm()
    ur = User.objects.filter(course=course).order_by('id')
    return render(request, 'student/student_course_resource.html',{'uf':uf, 'ur': ur, 'course': course}, context_instance=RequestContext(request))
'''

def courseDownload(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', \
                                                              'pwd': 'student_pwd'})

    def file_iterator(fn, buf_size=262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    file_name = FILE_ROOT.replace('\\','/') + '/polls/media/upload/' + request.GET.get('fname', None)
    response = StreamingHttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)

    return response

def courseChat(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', \
                                                              'pwd': 'student_pwd'})

    course = Course.objects.get(c_id=course_id)
    student = Student.objects.get(s_id=name)

    message = request.POST.get('chat_message', None)
    if message:
        ch_time = datetime.now()
        ch_person = name
        ch_type = 0
        ch_course = course
        ch_message = message
        chat = Chat(ch_person=ch_person,
                    ch_type=ch_type,
                    ch_course=ch_course,
                    ch_message=ch_message,
                    ch_time=ch_time)
        chat.save()

    chat = course.chat_course.all()
    for c in chat:
        if c.ch_type == '1':
            c.ch_person = Teacher.objects.get(t_id=c.ch_person)
        elif c.ch_type == '0':
            c.ch_person = Student.objects.get(s_id=c.ch_person)
        else:
            c.ch_person = None

    return render(request, 'student/student_course_chat.html', {'student': student, 'course': course, 'chat': chat})

# *上传附件的相应操作可以查看这一方法
def courseGroups(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', \
                                                              'pwd': 'student_pwd'})

    course = Course.objects.get(c_id=course_id)
    cg = CourseGroup.objects.filter(cg_course=course)
    student = Student.objects.get(s_id=name)
    for g in cg:
        if g.cg_type == 0:
            student = Student.objects.get(s_id=g.cg_author)
            g.cg_author = student
        elif g.cg_type == 1:
            teacher = Teacher.objects.get(t_id=g.cg_author)
            g.cg_author = teacher

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            cg_title = form.cleaned_data['cg_title']
            cg_message = form.cleaned_data['cg_message']
            cg_file = form.cleaned_data['cg_file']
            temp_cg = CourseGroup()
            temp_cg.cg_author = name
            temp_cg.cg_type = 0
            temp_cg.cg_title = cg_title
            temp_cg.cg_message = cg_message
            temp_cg.cg_time = datetime.now()
            temp_cg.cg_course = course
            if cg_file:
                # 该操作是上传文件至服务器
                handle_uploaded_file(cg_file, course)
                # 该操作是将相关信息写入数据库
                user = User()
                user.course = course
                user.headImg = cg_file
                user.username = cg_file.name
                user.uploadperson = name
                user.type = 0
                user.time = datetime.now()
                user.save()
                temp_cg.cg_file = user
            temp_cg.save()
        redirectURL = '/polls/student/%s/group' % course.c_id
        return HttpResponseRedirect(redirectURL)
    return render(request, 'student/student_course_group.html', {'courseGroup': cg, 'course': course, \
                                                                 'student': student})

def courseSendmsg(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', \
                                                              'pwd': 'student_pwd'})

    course = Course.objects.get(c_id=course_id)
    student = Student.objects.get(s_id=name)
    return render(request, 'student/student_course_sendmsg.html', {'course': course, 'student': student})

def courseMsgsubmit(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', \
                                                              'pwd': 'student_pwd'})

    course = Course.objects.get(c_id=course_id)
    info = Information()
    info.i_type = 7
    info.i_from = name
    info.i_to = course.c_teacher.t_id
    info.i_time = datetime.now()
    info.i_title = request.POST.get('msg_title', None)
    info.i_message = request.POST.get('msg_message', None)
    info.save()
    return  render(request, 'student/student_result.html', {'status': 11})

def courseHomework(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', \
                                                              'pwd': 'student_pwd'})

    course = Course.objects.get(c_id=course_id)
    student = Student.objects.get(s_id=name)
    homework = Homework.objects.filter(hw_course=course).order_by('id')
    myhw = StudentToHomework.objects.filter(sTh_student=student).order_by('sTh_homework__id')
    homework = calculateHomework(homework, myhw)

    return render(request, 'student/student_course_homework.html', {'course': course, 'student': student, 'homework': homework})

def courseHwDetail(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', \
                                                              'pwd': 'student_pwd'})

    course = Course.objects.get(c_id=course_id)
    hw_id = int(request.GET.get('hw_id', None))
    homework = Homework.objects.get(id=hw_id)
    myhw = homework.sth_homework.all()
    if not myhw:
        myhw = None
    else:
        myhw = myhw[0]
    return render(request, 'student/student_course_hwdetail.html', {'course': course, 'homework': homework, 'myhw': myhw})

def courseCgDetail(request, course_id):
    name = request.session.get('s_id', None)
    if not name:
        return render(request, 'student/student_login.html', {'url': '/student/login/', 'id': 'student_id', \
                                                              'pwd': 'student_pwd'})

    cg_id = request.GET.get('gid', None)
    if not cg_id:
        return HttpResponse('Error')
    course = Course.objects.get(c_id=course_id)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            cg_title = form.cleaned_data['cg_title']
            cg_message = form.cleaned_data['cg_message']
            cg_file = form.cleaned_data['cg_file']
            cg_replycg = cg_id
            temp_cg = CourseGroup()
            temp_cg.cg_author = name
            temp_cg.cg_type = 2
            temp_cg.cg_title = cg_title
            temp_cg.cg_message = cg_message
            temp_cg.cg_time = datetime.now()
            temp_cg.cg_course = course
            temp_cg.cg_repycg = cg_replycg
            temp_cg.cg_replynumber += 1
            if cg_file:
                # 该操作是上传文件至服务器
                handle_uploaded_file(cg_file, course)
                # 该操作是将相关信息写入数据库
                user = User()
                user.course = course
                user.headImg = cg_file
                user.username = cg_file.name
                user.uploadperson = name
                user.type = 0
                user.time = datetime.now()
                user.save()
                temp_cg.cg_file = user
            temp_cg.save()
        else:
            return HttpResponse('form invalid')

    try:
        cg = CourseGroup.objects.get(id=cg_id)
    except CourseGroup.DoesNotExist:
        return HttpResponse('Error')
    if cg.cg_type == 0:
        cg.cg_author = Student.objects.get(s_id=cg.cg_author)
    elif cg.cg_type == 1:
        cg.cg_author = Teacher.objects.get(t_id=cg.cg_author)
    cgrp = CourseGroup.objects.filter(cg_repycg=cg.id)
    for rp in cgrp:
        if rp.cg_type == 0:
            rp.cg_author = Student.objects.get(s_id=rp.cg_author)
        elif rp.cg_type == 1:
            rp.cg_author = Teacher.objects.get(t_id=rp.cg_author)

    return render(request, 'student/student_course_cgdetail.html', {'cg': cg, 'course': course, 'cgrp': cgrp})

def quit(request):
    try:
        del request.session['s_id']
    except KeyError:
        pass
    return render(request, 'student/student_login.html', {'url':'/student/login/', 'id':'student_id', 'pwd':'student_pwd'})

# 这个函数有问题 需要解决 创建一个result list用于返回值
def calculateHomework(homework, mywork):
    result = []

    if not homework:
        return None
    if not mywork:
        for h in homework:
            result_hw = HomeworkCheck(1, h)
            result.extend([result_hw])
    else:
        i = 0
        for h in homework:
            if mywork[i].sth_homework == h:
                result_hw = HomeworkCheck(0, h)
            else:
                result_hw = HomeworkCheck(1, h)
            if i < len(mywork) - 1:
                i += 1
            result.extend([result_hw])
    return result

def calculateSchedule(course_info):
    result = []
    j = 0

    if not course_info:
        for i in range(1, 41):
            if i % 8 == 1:
                tempCourse = CourseInfo(1, None, '第%d、%d节课' % ((i / 8)*2 + 1, (i / 8)*2 + 2))
            elif i % 8 == 0:
                tempCourse = CourseInfo(3, None, '')
            else:
                tempCourse = CourseInfo(5, None, '')
            result.extend([tempCourse])
        return result

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

def bbsort(course):
    if len(course) == 1:
        return course
    elif len(course) == 0:
        return None
    else:
        for i in range(0, len(course)):
            for j in range(0, len(course)):
                if course[j].ci_time > course[i].ci_time:
                    course[j], course[i] = course[i], course[j]
    return course

class UserForm(forms.Form):
    username = forms.CharField(max_length=50)
    headImg = forms.FileField()

def handle_uploaded_file(f, course):
    filepath = 'polls/media/upload/%s/%s' % (course.c_id, f.name)
    destination = open(filepath, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

class UploadFileForm(forms.Form):
    cg_title = forms.CharField(max_length=50)
    cg_file = forms.FileField(required=False)
    cg_message = forms.CharField(max_length=140, widget=forms.Textarea, required=False)