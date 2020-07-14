from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    context = {
        'users': User.objects.get_all_by_email()
    }
    return render(request, 'index.html', context)


def create(request):
    errors = User.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')

    new_user = User.objects.register(request.POST)
    request.session['user_id'] = new_user.id
    return redirect('/success')

def login(request):
    result = User.objects.authenticate(request.POST['email'], request.POST['password'])
    if result == False:
        messages.error(request, "Invalid Email/Password", extra_tags='log_in')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        messages.success(request, "You have successfully registered!", extra_tags='success')
        return redirect('/success')
    return redirect('/')


def success(request):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'success.html', context)

def logout(request):
    messages.success(request, "You have successfully logged out!", extra_tags='lo')
    request.session.clear()
    return redirect('/')




