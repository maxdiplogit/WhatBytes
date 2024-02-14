from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.validators import validate_email


# Models
from .models import CustomUser


# Create your views here.
def user_is_authenticated(user):
    return user.is_authenticated


def index(request):
    return render(request, 'home.html')


def register_user(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the user already exists
        usernameAndEmailSame = CustomUser.objects.filter(username=username, email=email)
        if (usernameAndEmailSame.exists()):
            messages.error(request, "User already exists, instead try logging in!")
            return redirect('login')
        
        # Check if the username is already taken
        usernameExists = CustomUser.objects.filter(username=username)
        if (usernameExists.exists()):
            messages.error(request, "Username already taken!")
            return redirect('register')
        
        # Check if the email is already taken
        emailTaken = CustomUser.objects.filter(email=email)
        if (emailTaken.exists()):
            messages.error(request, "Email already in use, instead try logging in!")
            return redirect('login')
        
        # Check if password and confirmPassword are same
        if (password != confirm_password):
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        
        # Create new user
        newUser = CustomUser.objects.create_user(username=username, email=email)
        newUser.set_password(password)
        newUser.save()

        login(request, newUser)
        messages.info(request, "Account created and logged in successfully!")

        return redirect('index')

    return render(request, 'register.html')


def login_user(request):
    if (request.method == 'POST'):
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        isEmail = False
        try:
            validate_email(username_or_email)
            isEmail = True
        except:
            isEmail = False
        
        if (isEmail):
            if not CustomUser.objects.filter(email=username_or_email).exists():
                messages.error(request, "Invalid Email!")
                return redirect('login')
            
            findUser = CustomUser.objects.filter(email=username_or_email)
            if (findUser.exists()):
                user = authenticate(request, username=findUser[0].username, password=password)
                
                if user is None:
                    messages.error(request, "Invalid Password!")
                    return redirect('login')
                else:
                    login(request, user)
                    messages.info(request, "Logged in successfully!")
                    return redirect('index')
        else:
            if not CustomUser.objects.filter(username=username_or_email).exists():
                messages.error(request, "Invalid Username!")
                return redirect('login')
            
            user = authenticate(request, username=username_or_email, password=password)

            if user is None:
                messages.error(request, "Invalid Password!")
                return redirect('login')
            else:
                login(request, user)
                messages.info(request, "Logged in successfully!")
                return redirect('index')

    return render(request, 'login.html')


@user_passes_test(user_is_authenticated, login_url='login')
def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'user_profile.html')


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "Logged out Successfully!")
    return redirect('login')