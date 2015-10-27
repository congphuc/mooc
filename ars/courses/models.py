from django.db import models
from django.core.exceptions import MultipleObjectsReturned

from ars.core.models import Timestampable, Describable
from ars.teachers.models import Teacher


class Course(Timestampable, Describable):
    teachers = models.ManyToManyField(Teacher,
                            through='TeacherCourse', related_name='courses')

    class Meta:
        db_table = 'course'

    def __str__(self):
        return self.name

    @property
    def creator(self):
        try:
            teacher = Teacher.objects.filter(
                                    courses=self
                                    ).filter(
                                    courses__teachercourse__is_creator=True
                                    ).get()
        except MultipleObjectsReturned as err:
            print(err.strerror)
            teacher = self.teachers[0]
        
        return teacher


class TeacherCourse(models.Model):
    teacher = models.ForeignKey(Teacher)
    course = models.ForeignKey(Course)
    is_creator = models.BooleanField(default=False)

    class Meta:
        db_table = 'teacher_course'
