import pdb

class CourseInfo:
    type = 0
    course = None
    status = ''

    def __init__(self, type, course, status):
        self.type = type
        self.course = course
        self.status = status

    def __str__(self):
        return "%s %s" % (self.type, self.course)

    def get_type(self):
        return self.type

    def get_course(self):
        return self.course

class GroupCheck:
    type = 0
    group = None
    student = None

    def __init__(self, type, group):
        self.type = type
        self.group = group

    def __str__(self):
        return "%s %s" % (self.type, self.group)

    def get_type(self):
        return self.type

    def get_group(self):
        return self.group

    def set_student(self, student):
        self.student = None
        self.student = student

class PageInfo:
    type = -1
    current = -1
    total = -1
    previouspage = -1
    nextpage = -1
    fivepage = []

    def __init__(self, current_page, total_page):
        self.current = current_page
        self.total = total_page
        self.fivepage = []

        if self.total == 1:
            self.type = 0
        elif self.total <= 5:
            if self.current == 1:
                self.type = 1
                self.nextpage = 2
            elif self.current == self.total:
                self.type = 2
                self.previouspage = self.total - 1
            else:
                self.type = 3
                self.previouspage = self.current - 1
                self.nextpage = self.current + 1
            for i in range(0, self.total):
                self.fivepage.append(i+1)
        else:
            if self.current == 1:
                self.type = 4
                self.nextpage = 2
                for i in range(0, 5):
                    self.fivepage.append(i + 1)
            elif self.current <= 3:
                self.type = 5
                self.nextpage = self.current + 1
                self.previouspage = self.current - 1
                for i in range(0, 5):
                    self.fivepage.append(i + 1)
            elif self.current == self.total:
                self.type = 6
                self.previouspage = self.total - 1
                for i in range(self.total - 5, self.total):
                    self.fivepage.append(i + 1)
            elif self.current >= self.total - 2:
                self.type = 7
                self.nextpage = self.current + 1
                self.previouspage = self.current - 1
                for i in range(self.total - 5, self.total):
                    self.fivepage.append(i + 1)
            else:
                self.type = 8
                self.nextpage = self.current + 1
                self.previouspage = self.current - 1
                for i in range(self.current - 2, self.current + 3):
                    self.fivepage.append(i)

    def get_prev(self):
        return self.previouspage

    def get_next(self):
        return self.nextpage

    def get_fivepage(self):
        return self.fivepage

    def get_type(self):
        return self.type

    def get_current(self):
        return self.current

    def get_total(self):
        return self.total

class HomeworkCheck:
    type = 1
    homework = None

    def __init__(self, type, homework):
        self.type = type
        self.homework = homework

    def get_homework(self):
        return self.homework

    def get_type(self):
        return self.type