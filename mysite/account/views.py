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
            print(user)
            if user is not None:
                login(request, user)
                group = None
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name
                if group == "professor":
                    return redirect('dashboard_professor')
                elif group == "student":
                    return redirect('dashboard_student')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
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
    classes = Class.objects.all()
    registrations = Registration.objects.filter(user=request.user)
    print(request.user)
    print(registrations)
    context = {'classes': classes , "registrations" : registrations}

    return render(request, 'accounts/dashboard_student.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def add_class(request, pk):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        class_obj = Class.objects.get(id=pk)
        registration = Registration.objects.filter(course=class_obj)
        print(class_obj.class_name)
        print(class_obj.user)
        print(class_obj.start_date)
        print(class_obj.end_date)
        print(class_obj)
        print(form)
        if form.is_valid():
            if len(registration) == 0:
                form = form.save(commit=False)
                form.user = request.user
                form.course = class_obj
                print(form)
                form.save()
            else:
                print("Not possible to add")
            return redirect('dashboard_student')
    context = {}
    return render(request, 'accounts/dashboard_student.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def remove_class(request, pk):
    print(pk)
    registration = Registration.objects.get(id=pk)
    print(registration)
    if request.method == "POST":
        registration.delete()
        return redirect('dashboard_student')
    context = {'item': registration}
    print("Oi")
    return render(request, 'accounts/delete_student_class.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['professor'])
def create_class(request):
    form = ClassForm()
    if request.method == 'POST':
        form = ClassForm(request.POST)
        start_date = form.data['start_date']
        end_date = form.data['end_date']
        print(start_date)
        classes = Class.objects.filter(Q(user=request.user) & (Q(start_date__range=[start_date, end_date]) | Q(end_date__range=[start_date, end_date])) & (Q(start_date__lte=start_date) | Q(end_date__gte=end_date)))
        print(classes)
        if form.is_valid() and len(classes) == 0:
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('dashboard_professor')
        else:
            messages.info(request, 'This class time is already taken!')

    context = {'form': form}
    return render(request, 'accounts/create_class.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['professor'])
def update_class(request, pk):
    classObj = Class.objects.get(id=pk)
    classForm = ClassForm(instance=classObj)
    if request.method == 'POST':
        classForm = ClassForm(request.POST, instance=classObj)
        start_date = classForm.data['start_date']
        end_date = classForm.data['end_date']
        classes = Class.objects.filter(~Q(id=pk) & Q(user=request.user) & (Q(start_date__range=[start_date, end_date]) | Q(end_date__range=[start_date, end_date])) & (Q(start_date__lte=start_date) | Q(end_date__gte=end_date)))
        print(classes)
        if classForm.is_valid() and len(classes) == 0:
            classForm.save()
            return redirect('dashboard_professor')
        else:
            messages.info(request, 'This class time is already taken!')

    context = {'form':classForm}
    return render(request, 'accounts/create_class.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['professor'])
def delete_class(request, pk):
    order = Class.objects.get(id=pk)
    print(order)
    if request.method == "POST":
        order.delete()
        return redirect('dashboard_professor')

    context = {'item':order}
    return render(request, 'accounts/delete_professor_class.html', context)