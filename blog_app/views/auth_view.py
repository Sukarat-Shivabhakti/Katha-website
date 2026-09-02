from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def register_method(request):
    if request.method == "POST":
        # .get('name', '') prevents errors if the field is missing
        # .strip() removes accidental blank spaces at the start or end
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        errors = {}

        # 1. Check for missing data or duplicates
        if not username:
            errors['username'] = "Username is required."
        elif User.objects.filter(username=username).exists():
            errors['username'] = "This username is already taken."
        
        if not email:
            errors['email'] = "Email address is required."
        elif User.objects.filter(email=email).exists():
            errors['email'] = "This email is already registered."

        # -> NEW: Password length validation added here <-
        if not password:
            errors['password'] = "Password is required."
        elif len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        
        if not confirm_password:
            errors['confirm_password'] = "Please confirm your password."
        elif password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."
        
        # 2. Stop here and show the form again if there are errors
        if errors:
            return render(request, 'auth/register.html', {'error': errors, 'prev': request.POST})
        
        # 3. If no mistakes, create the user
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
            
    return render(request, 'auth/register.html')


def login_method(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        errors = {}

        # 1. Check if boxes are empty or username is fake
        if not username:
            errors['username'] = "Username is required."
        elif not User.objects.filter(username=username).exists():
            errors['username'] = "We couldn't find an account with that username."

        if not password:
            errors['password'] = "Password is required."
        
        # 2. Stop and show errors if any exist
        if errors:
            return render(request, 'auth/login.html', {'error': errors, 'data': request.POST})
        
        # 3. Try to authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  
            messages.success(request, "Welcome back!")
            return redirect('index')
        else:
            # Username existed, but the password was wrong
            messages.error(request, 'Incorrect password. Please try again.')
            return redirect('login')
                
    return render(request, 'auth/login.html')


def logout_method(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')