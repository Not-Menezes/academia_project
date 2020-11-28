from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User


class Class(models.Model):

    user = models.ForeignKey(User, verbose_name="user", null=True, on_delete=models.SET_NULL)
    class_name = models.CharField(max_length=200, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return '%s ---- %s' % (self.user, self.class_name)

class Registration(models.Model):

    user = models.ForeignKey(User, verbose_name="user", null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Class, verbose_name="course", null=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField(verbose_name='date joined', auto_now_add=True)

    def __str__(self):
        return '%s ---- %s' % (self.user, self.course)
