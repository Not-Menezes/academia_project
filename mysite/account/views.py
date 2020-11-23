from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ClassForm
from .models import Account, Class


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
            if user is not None and user.function == "Professor":
                login(request, user)
                return redirect('dashboard_professor')
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
def dashboard_professor(request):
    classes = Class.objects.filter(user=request.user)

    context = {'classes': classes}
    return render(request, 'accounts/class.html', context)


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