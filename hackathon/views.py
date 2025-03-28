from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from .models import Course
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'index.html')

def dashboard_redirect(request):
    if request.user.user_type == "student":
        return redirect("student_dashboard")
    elif request.user.user_type == "instructor":
        return redirect("instructor_dashboard")
    return redirect("home")


def login(request):
    return render(request, 'login.html')


def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def logout_view(request):
    logout(request)  
    return redirect('login')  
