import email
import imp
import profile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.views.decorators.csrf import csrf_protect
from .models import Profile

from core.models import Profile

@login_required(login_url='signin')
#@csrf_protect
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    return render(request, 'index.html', {'user_profile' : user_profile})

def signup(request):
    
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id_user)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')  
    
def signin(request):
    
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credential invalid')
            return redirect('signin')
        
    return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.FILES.get('image') == None:
        image = user_profile.profileimg
        bio = request.POST['bio']
        location = request.POST['location']
        
        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
    if request.FILES.get('image') != None:
        image = request.FILES.get('image')
        bio = request.FILES.get('bio')
        location = request.FILES.get('locatin')
        
        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        
    return redirect('settings')
        
    return render(request, 'settings.html', {'user_profile' : user_profile})


@login_required(login_url='signin')
def upload(request):
    return HttpResponse()