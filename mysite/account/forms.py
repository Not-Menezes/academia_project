from functools import partial

from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import ModelForm, DateTimeField, DateField, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account, Class
from django import forms
from django.contrib.admin import widgets
DateInput = partial(forms.DateInput, {'class': 'form-control datetimepicker-input'})


class ClassForm(ModelForm):
	class Meta:
		model = Class
		exclude = ['user']

class CreateUserForm(UserCreationForm):
	function = forms.RadioSelect()
	class Meta:
		model = Account
		fields = ['username', 'email', 'password1', 'password2' , 'function']