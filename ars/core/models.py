from django.db import models
from django.conf import settings


class Timestampable(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Describable(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, default='')

    class Meta:
        abstract = True


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True, related_name='profile')
    avatar = models.ImageField(upload_to='avatars')
    modified_date = models.DateTimeField(auto_now=True)

    @property
    def is_teacher(self):
        if hasattr(self, 'teacher'):
            return True
        return False

    @property
    def info(self):
        if self.student:
            return self.student
        elif self.teacher:
            return self.teacher
        return None
