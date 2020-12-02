from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Class(models.Model):

    user = models.ForeignKey(User, verbose_name="user", null=True, on_delete=models.SET_NULL)
    class_name = models.CharField(max_length=200, verbose_name="Aula", null=True)
    start_date = models.DateTimeField(null=True, verbose_name="Data de Início")
    end_date = models.DateTimeField(null=True, verbose_name="Data de Fim")

    def __str__(self):
        return '%s ---- %s' % (self.user, self.class_name)

class Registration(models.Model):

    user = models.ForeignKey(User, verbose_name="user", null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Class, verbose_name="course", null=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField(verbose_name='date joined', auto_now_add=True)

    def __str__(self):
        return '%s ---- %s' % (self.user, self.course)


class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
