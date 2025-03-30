from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, CustomUser,LearnerProfile,InstructorProfile
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json

User = get_user_model()  # Get the custom user model

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        user_type = request.POST.get("user_type", "learner")  # Default to 'learner'

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.user_type = user_type  # Ensure CustomUser has this field
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("user_login")  # Redirect to login page

    return render(request, "register.html")


def home(request):
    return render(request, "index.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Use auth_login to avoid conflicts
            
            # Redirect based on user type
            if user.user_type == "learner":
                return redirect("learner")  
            elif user.user_type == "instructor":
                return redirect("instructor")  
            else:
                return redirect("home")  

        else:
            messages.error(request, "Invalid username or password.")
            return redirect("user_login")

    return render(request, "login.html")


@login_required
def learner(request):
    return render(request, "learner.html")


@login_required
def instructor(request):
    return render(request, "instructor.html")


def courses(request):
    courses = Course.objects.all()
    return render(request, "courses.html", {"courses": courses})


def logout_view(request):
    auth_logout(request)  # Use auth_logout to avoid conflicts
    return redirect("user_login")

@login_required
def learner_profile(request):
    learner_profile, created = LearnerProfile.objects.get_or_create(user=request.user)
    return render(request, 'learner_profile.html', {'learner_profile': learner_profile})

@login_required
def update_learner_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        learner_profile, created = LearnerProfile.objects.get_or_create(user=request.user)
        
        learner_profile.courses = data.get("courses", learner_profile.courses)
        learner_profile.age = data.get("age", learner_profile.age)
        learner_profile.state = data.get("state", learner_profile.state)
        learner_profile.city = data.get("city", learner_profile.city)
        
        learner_profile.save()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False})


@login_required
def instructor_profile(request):
    instructor_profile, created = InstructorProfile.objects.get_or_create(user=request.user)
    return render(request, 'instructor_profile.html', {'instructor_profile': instructor_profile})

@login_required
def update_instructor_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        instructor_profile, created = InstructorProfile.objects.get_or_create(user=request.user)
        
        instructor_profile.courses = data.get("courses", instructor_profile.courses)
        instructor_profile.age = data.get("age", instructor_profile.age)
        instructor_profile.state = data.get("state", instructor_profile.state)
        instructor_profile.city = data.get("city", instructor_profile.city)
        
        instructor_profile.save()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False})