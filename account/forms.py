from functools import partial

from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import ModelForm, DateTimeField, DateField, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Class , Registration
from django import forms
from django.contrib.admin import widgets
DateInput = partial(forms.DateInput, {'class': 'form-control datetimepicker-input'})


class RegistrationForm(ModelForm):
	class Meta:
		model = Registration
		exclude = ['user', 'course']

class ClassForm(ModelForm):
	class Meta:
		model = Class
		exclude = ['user']

class CreateUserForm(UserCreationForm):
	function = forms.CharField(
	max_length=20,
		widget=forms.RadioSelect(choices=[
			('Student', 'Student'),
			('Professor', 'Professor')
		])
	)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		fields.append('function')