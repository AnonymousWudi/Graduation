# coding=utf-8
import sys
from datetime import *
from django import forms

reload(sys)
sys.setdefaultencoding('utf8')
from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Manager(models.Model):
    m_name = models.CharField(max_length=20, primary_key=True, blank=False, null=False, unique=True)
    m_pwd = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return "%s" % (self.m_name,)

class Academy(models.Model):
    a_id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    a_name = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return "%s %s" % (self.a_id, self.a_name)

class Major(models.Model):
    m_id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    m_name = models.CharField(max_length=30, blank=False, null=False)
    m_academy = models.ForeignKey(Academy, related_name='major_academy')

    def __str__(self):
        return "%s %s" % (self.m_academy.a_name, self.m_name)

class Student(models.Model):
    s_id = models.CharField(max_length=10, primary_key=True, blank=False, null=False, unique=True)
    s_name = models.CharField(max_length=10, blank=False, null=False)
    s_pwd = models.CharField(max_length=20, blank=False, null=False)
    s_mail = models.CharField(max_length=30)
    s_class = models.IntegerField(blank=False, null=False)
    s_grade = models.IntegerField(blank=False, null=False)
    s_major = models.ForeignKey(Major, related_name='student_major')
    s_academy = models.ForeignKey(Academy, related_name='student_academy')

    def __str__(self):
        return "%s %s" % (self.s_id, self.s_name)

class Teacher(models.Model):
    t_id = models.CharField(max_length=20, primary_key=True, blank=False, null=False, unique=True)
    t_name = models.CharField(max_length=20, blank=False, null=False)
    t_pwd = models.CharField(max_length=20, blank=False, null=False)
    t_academy = models.ForeignKey(Academy, related_name='teacher_academy')
    t_mail = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return "%s %s" % (self.t_id, self.t_name)

class Course(models.Model):
    c_id = models.CharField(max_length=20, primary_key=True, blank=False, null=False, unique=True)
    c_name = models.CharField(max_length=40, blank=False, null=False, unique=True)
    c_teacher = models.ForeignKey(Teacher, related_name='course_teacher')
    c_academy = models.ForeignKey(Academy, related_name='course_academy')
    c_major = models.ForeignKey(Major, related_name='course_major', default=None)
    c_total = models.IntegerField(blank=False, null=False, default=100)
    c_number = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return "%s %s" % (self.c_id, self.c_name)

class StudentToCourse(models.Model):
    c_id = models.ForeignKey(Course, related_name='get_course')
    s_id = models.ForeignKey(Student, related_name='get_student')

    def __str__(self):
        return "%s %s" % (self.s_id.s_name, self.c_id.c_name)

    class Meta:
        unique_together = ('c_id', 's_id')

class CourseInformation(models.Model):
    ci_id = models.ForeignKey(Course, related_name='course_info')
    # 课时数
    ci_period = models.IntegerField(blank=False, null=False)
    # 上课时间(0-34)
    ci_time = models.IntegerField(blank=False, null=False)
    # 上课地点
    ci_classroom = models.CharField(max_length=30, blank=False, null=False)
    # 上课节数
    ci_module = models.IntegerField(blank=False, null=False)
    # 单双周
    ci_type = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return "%s %s" % (self.ci_id.c_id, self.ci_id.c_name)

    class Meta:
        unique_together = ('ci_id', 'ci_time')

class Group(models.Model):
    g_name = models.CharField(max_length=30, null=False, blank=False, default='')
    g_teacher = models.ForeignKey(Teacher, related_name='group_teacher')
    g_course = models.ForeignKey(Course, related_name='group_course')
    g_total = models.IntegerField(blank=False, null=False, default=0)
    g_number = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return "%s %s" % (self.g_teacher.t_name, self.g_course.c_name)

    class Meta:
        unique_together = ('g_teacher', 'g_course')

class StudentToGroup(models.Model):
    s_id = models.ForeignKey(Student, related_name='sTg_student')
    g_id = models.ForeignKey(Group, related_name='sTg_group')

    def __str__(self):
        return "%s %s" % (self.s_id.s_name, self.g_id.g_course.c_name)

    class Meta:
        unique_together = ('s_id', 'g_id')

class Information(models.Model):
    i_id = models.AutoField(primary_key=True)
    # type 表示发送消息的类型，1表示请求加入讨论组，2是系统消息(系统->学生)，3是老师->讨论组，4是老师->学生，5是讨论组->学生，6是学生->学生，7是学生->老师, 8是系统消息(老师->系统)
    i_type = models.IntegerField(blank=False, null=False, default=2)
    i_from = models.CharField(max_length=30, blank=False, null=False, default='0')
    i_to = models.CharField(max_length=30, blank=False, null=False, default='0')
    i_title = models.CharField(max_length=30, blank=False, null=False, default='system')
    i_message = models.TextField(blank=True, null=False)
    # 附件功能暂未实现
    i_time = models.DateTimeField('date send')
    i_status = models.BooleanField(default=False)
    i_group = models.ForeignKey(Group, null=True, blank=True, default=None)

    def __str__(self):
        return "%s %s %s %s" % (self.i_id, self.i_from, self.i_to, self.i_time)

    class Meta:
        unique_together = ('i_from', 'i_to', 'i_time')

class Notice(models.Model):
    n_id = models.AutoField(primary_key=True)
    n_type = models.IntegerField(blank=False, null=False, default=0)
    n_from = models.CharField(max_length=30, blank=False, null=False, default='0')
    n_to = models.CharField(max_length=30, blank=False, null=False, default='0')
    n_title = models.CharField(max_length=30, blank=False, null=False, default='system')
    n_message = models.TextField(blank=True, null=False)
    n_time = models.DateTimeField('data send')
    n_status = models.BooleanField(default=False)
    n_course = models.ForeignKey(Course, null=True, blank=True, default=None)

    def __str__(self):
        return "%s %s %s %s" % (self.n_id, self.n_from, self.n_to, self.n_time)

    class Meta:
        unique_together = ('n_id', 'n_time')

class User(models.Model):
    username = models.CharField(max_length = 30)
    headImg = models.FileField(upload_to = './polls/media/upload/')
    uploadperson = models.CharField(max_length=20, blank=False, null=False, default='0')
    course = models.ForeignKey(Course, related_name='file_course', blank=True, null=True)
    time = models.DateTimeField('date upload', default=datetime.now())
    # type=0 表示是学生上传 type=1表示是老师上传
    type = models.IntegerField(blank=False, null=False, default=0)

    def __unicode__(self):
        return self.username

class Chat(models.Model):
    ch_course = models.ForeignKey(Course, related_name='chat_course')
    ch_time = models.DateTimeField('date chat')
    ch_person = models.CharField(max_length=30, null=False, blank=False)
    ch_message = models.TextField(max_length=140, null=False, blank=False)
    # 1代表老师 0代表学生
    ch_type = models.CharField(max_length=10, null=False, blank=False)

    def __unicode__(self):
        return "%s %s %s" % (self.ch_time, self.ch_person, self.ch_message)

class CourseGroup(models.Model):
    cg_course = models.ForeignKey(Course)
    # 0代表是学生创建的讨论组 1代表是老师创建的讨论组 2表示是学生回复 3表示是老师回复
    cg_type = models.IntegerField(null=False, blank=False, default=0)
    cg_author = models.CharField(max_length=10, null=False, blank=False, default='0')
    cg_title = models.CharField(max_length=50, null=False, blank=False, default='讨论区')
    cg_time = models.DateTimeField('group_datetime')
    cg_message = models.TextField(blank=True, null=True, default=None)
    cg_replynumber = models.IntegerField(null=True, blank=False, default=0)
    cg_file = models.ForeignKey(User, null=True, blank=True, default=None)
    cg_repycg = models.CharField(max_length=50, null=True, blank=True, default='')

    def __unicode__(self):
        return self.cg_title

class Homework(models.Model):
    hw_title = models.CharField(max_length=30, blank=False, null=False, default='作业')
    hw_message = models.TextField(blank=True, null=True, default=None)
    hw_course = models.ForeignKey(Course, blank=True, null=True, related_name='homework_course', default=None)
    hw_teacher = models.ForeignKey(Teacher, blank=True, null=True, related_name='homework_teacher')
    hw_file = models.ForeignKey(User, blank=True, null=True, related_name='homework_file')
    hw_starttime = models.DateTimeField(blank=False, null=False)
    hw_deadline = models.DateTimeField(blank=False, null=False)
    hw_score = models.IntegerField(blank=False, null=False, default=100)
    # status=1表示该作业在进行中 status=0表示该作业已经结束
    hw_status = models.IntegerField(blank=False, name=False, default=1)

    def __unicode__(self):
        return self.hw_title

class StudentToHomework(models.Model):
    sTh_time = models.DateTimeField(blank=False, null=False)
    sTh_file = models.ForeignKey(User, blank=True, null=True, related_name='sth_file')
    sTh_student = models.ForeignKey(Student, blank=True, null=True, related_name='sth_student')
    # status=1 表示尚未提交作业 status=0 表示已经提交作业 可以再次提交 再次提交时 文件刷新
    sTh_status = models.IntegerField(null=False, blank=False, default=1)
    sTh_homework = models.ForeignKey(Homework, blank=True, null=True, related_name='sth_homework')

    def __unicode__(self):
        return "%s %s" % (self.sTh_student.s_name, self.sTh_homework.hw_title)