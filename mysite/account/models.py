from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Usuáro deve possuir um email!")
        if not username:
            raise ValueError("Usuário deve possuir um login")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email        = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username     = models.CharField(max_length=30, unique=True)
    date_joined  = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    function     = models.CharField(
        choices=(
            ('Student','Student'),
            ('Professor','Professor'),
        ),
        max_length=20,
        verbose_name='Function',
        default='Student'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Class(models.Model):

    user = models.ForeignKey(Account, verbose_name="user", null=True, on_delete=models.SET_NULL)
    class_name = models.CharField(max_length=200, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return '%s ---- %s' % (self.user, self.class_name)

class Registration(models.Model):

    user = models.ForeignKey(Account, verbose_name="user", null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Class, verbose_name="course", null=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField(verbose_name='date joined', auto_now_add=True)

    def __str__(self):
        return '%s ---- %s' % (self.user, self.course)
