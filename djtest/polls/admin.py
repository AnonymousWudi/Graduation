from django.contrib import admin

# Register your models here.
from polls.models import Question, Manager, Academy, Major, Student, Teacher, Course, StudentToCourse, CourseInformation, \
    Group, StudentToGroup, Information, User, Chat, CourseGroup, Homework, StudentToHomework


class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Manager)
admin.site.register(Academy)
admin.site.register(Major)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(StudentToCourse)
admin.site.register(CourseInformation)
admin.site.register(Group)
admin.site.register(StudentToGroup)
admin.site.register(Information)
admin.site.register(User)
admin.site.register(Chat)
admin.site.register(CourseGroup)
admin.site.register(Homework)
admin.site.register(StudentToHomework)