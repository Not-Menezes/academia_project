from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ClassForm, RegistrationForm
from .models import Class, Registration
from .decorators import unauthenticated_user, student_only, professor_and_admin_only, allowed_users
import datetime

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                function = form.cleaned_data.get('function')
                user = form.save()
                username = form.cleaned_data.get('username')

                if function == "Professor":
                    group, created = Group.objects.get_or_create(name='professor')
                elif function == "Student":
                    group, created = Group.objects.get_or_create(name='student')

                user.groups.add(group)


                messages.success(request, 'Account was created for ' + username)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                group = None
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name
                elif request.user.is_superuser and not request.user.groups.exists():
                    group , created = Group.objects.get_or_create(name='professor')
                    request.user.groups.add(group)
                if group == "professor":
                    return redirect('dashboard_professor')
                elif group == "student":
                    return redirect('dashboard_student')
            else:
                messages.info(request, 'Login ou senha incorreto(s)!')

        context = {}
        return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
@professor_and_admin_only
@student_only
def home(request):
    return render(request, 'accounts/home.html')

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@professor_and_admin_only
def dashboard_professor(request):
    classes = Class.objects.filter(user=request.user)

    context = {'classes': classes}
    return render(request, 'accounts/dashboard_professor.html', context)

@login_required(login_url='login')
@student_only
def dashboard_student(request):
    classes = Class.objects.filter(user__groups__name='professor')
    registrations = Registration.objects.filter(user=request.user)
    context = {'classes': classes , "registrations" : registrations}

    return render(request, 'accounts/dashboard_student.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def add_class(request, pk):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        class_obj = Class.objects.get(id=pk)
        start_date = class_obj.start_date
        end_date = class_obj.end_date
        registration = Registration.objects.filter(Q(course=class_obj) | (~Q(course=class_obj) & (Q(course__start_date__range=[start_date, end_date]) | Q(course__end_date__range=[start_date, end_date])) & (Q(course__start_date__lte=start_date) | Q(course__end_date__gte=end_date))))
        if form.is_valid():
            if len(registration) == 0:
                form = form.save(commit=False)
                form.user = request.user
                form.course = class_obj
                form.save()
            else:
                messages.info(request, 'Choque de horário da aula "'+class_obj.class_name+'" de horário inicial '+str(start_date)+' e horário final '+ str(end_date)+' !')
            return redirect('dashboard_student')
    context = {}
    return render(request, 'accounts/dashboard_student.html', context)

def dates_valid(start_date, end_date):
    try:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
        return True , start_date, end_date
    except ValueError:
        return False , "" , ""

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def remove_class(request, pk):
    registration = Registration.objects.get(id=pk)
    if registration.user != request.user:
        return redirect('dashboard_student')
    if request.method == "POST":
        registration.delete()
        return redirect('dashboard_student')
    context = {'item': registration}
    return render(request, 'accounts/delete_student_class.html', context)

def validate_class_date(start_date, end_date, request):
    result, start_date , end_date = dates_valid(start_date, end_date)
    success = True
    if not result:
        messages.info(request, 'Formato de datas inválido! Por Favor, escreva no formato (YYYY-MM-DD HH:MM:SS)')
        success = False
        return result
    if start_date >= end_date:
        messages.info(request, 'Data de Início deve ser Menor que a Data Final!')
        success = False
    return success

@login_required(login_url='login')
@allowed_users(allowed_roles=['professor'])
def create_class(request):
    form = ClassForm()
    if request.method == 'POST':
        form = ClassForm(request.POST)
        start_date = form.data['start_date']
        end_date = form.data['end_date']
        if validate_class_date(start_date,end_date,request):
            classes = Class.objects.filter(Q(user=request.user) & (Q(start_date__range=[start_date, end_date]) | Q(end_date__range=[start_date, end_date])) & (Q(start_date__lte=start_date) | Q(end_date__gte=end_date)))
            if form.is_valid() and len(classes) == 0:
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect('dashboard_professor')
            else:
                messages.info(request, 'Esse horário de aula já está preenchido!')

    context = {'form': form}
    return render(request, 'accounts/create_class.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['professor'])
def update_class(request, pk):
    classObj = Class.objects.get(id=pk)
    if classObj.user != request.user:
        return redirect('dashboard_professor')
    classForm = ClassForm(instance=classObj)
    if request.method == 'POST':
        classForm = ClassForm(request.POST, instance=classObj)
        start_date = classForm.data['start_date']
        end_date = classForm.data['end_date']
        if validate_class_date(start_date, end_date, request):
            classes = Class.objects.filter(~Q(id=pk) & Q(user=request.user) & (Q(start_date__range=[start_date, end_date]) | Q(end_date__range=[start_date, end_date])) & (Q(start_date__lte=start_date) | Q(end_date__gte=end_date)))
            if classForm.is_valid() and len(classes) == 0:
                classForm.save()
                return redirect('dashboard_professor')
            else:
                messages.info(request, 'Voce já possui uma aula criada durante este horário!')

    context = {'form':classForm}
    return render(request, 'accounts/create_class.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['professor'])
def delete_class(request, pk):
    classObj = Class.objects.get(id=pk)
    if classObj.user != request.user:
        return redirect('dashboard_professor')
    if request.method == "POST":
        classObj.delete()
        return redirect('dashboard_professor')

    context = {'item':classObj}
    return render(request, 'accounts/delete_professor_class.html', context)