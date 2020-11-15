from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account
from django import forms


class CreateUserForm(UserCreationForm):
	function = forms.RadioSelect()
	class Meta:
		model = Account
		fields = ['username', 'email', 'password1', 'password2' , 'function']