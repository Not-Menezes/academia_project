from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ClassForm, RegistrationForm
from .models import Account, Class, Registration


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

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
                if user.function == "Professor":
                    return redirect('dashboard_professor')
                elif user.function == "Student":
                    return redirect('dashboard_student')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        if request.user.function == "Professor":
            return redirect('dashboard_professor')
        elif request.user.function == "Student":
            return redirect('dashboard_student')
    return render(request, 'accounts/home.html')

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def dashboard_professor(request):
    if request.user.is_authenticated:
        if request.user.function == "Student":
            return redirect('dashboard_student')
    classes = Class.objects.filter(user=request.user)

    context = {'classes': classes}
    return render(request, 'accounts/dashboard_professor.html', context)

@login_required(login_url='login')
def dashboard_student(request):
    if request.user.is_authenticated:
        if request.user.function == "Professor":
            return redirect('dashboard_professor')
    classes = Class.objects.all()
    registrations = Registration.objects.filter(user=request.user)
    print(request.user)
    print(registrations)
    context = {'classes': classes , "registrations" : registrations}

    return render(request, 'accounts/dashboard_student.html', context)

@login_required(login_url='login')
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
def remove_class(request, pk):
    classes = Class.objects.all()
    registrations = Registration.objects.filter(user=request.user)

    context = {'classes': classes , "registrations" : registrations}

    return render(request, 'accounts/dashboard_student.html', context)


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
def delete_class(request, pk):
    order = Class.objects.get(id=pk)
    print(order)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)