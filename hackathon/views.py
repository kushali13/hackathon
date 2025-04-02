from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json

User = get_user_model()  # Get the custom user model


def home(request):
    featured_courses = Course.objects.filter(is_featured=True)[:3]  # Fetch only 3 featured courses
    print("Featured Courses:", featured_courses)  # Debugging
    return render(request, 'index.html', {'featured_courses': featured_courses})


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

def courses(request):
    courses = Course.objects.all()
    return render(request, "courses.html", {"courses": courses})



def logout_view(request):
    auth_logout(request)  
    return redirect("home")



# INSTRUCTOR VIEWS
@login_required
def instructor(request):
    instructor_courses = Course.objects.filter(instructor=request.user)
    total_enrolled_students = sum(course.students_enrolled.all().count() for course in instructor_courses)  
    active_courses = instructor_courses.filter(is_active=True).count()

    context = {
        "instructor_courses": instructor_courses,
        "total_enrolled_students": total_enrolled_students,
        "active_courses": active_courses,
    }
    return render(request, "instructor/instructor.html", context)

@login_required
def add_course(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.FILES.get("image")
        video_url = request.FILES.get("video")
        level = request.POST["level"]
        language = request.POST["language"]
        duration = request.POST["duration"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        price = request.POST["price"]
        content = request.POST.get("content", "")
        prerequisites = request.POST.get("prerequisites", "")
        course_outcomes = request.POST.get("course_outcomes", "")
        is_active = request.POST.get("is_active", "off") == "on"
        is_featured = request.POST.get("is_featured", "off") == "on"
        
        instructor = request.user  # Assuming logged-in user is the instructor

        # Create course object
        course = Course.objects.create(
            title=title,
            description=description,
            image=image,
            video=video_url,
            level=level,
            language=language,
            duration=duration,
            instructor=instructor,
            start_date=start_date,
            end_date=end_date,
            price=price,
            content=content,
            prerequisites=prerequisites,
            course_outcomes=course_outcomes,
            is_active=is_active,
            is_featured=is_featured
        )

        # Handling Many-to-Many relationships
        category_ids = request.POST.getlist("categories")
        subcategory_ids = request.POST.getlist("subcategories")

        course.categories.set(Category.objects.filter(id__in=category_ids))
        course.subcategories.set(Subcategory.objects.filter(id__in=subcategory_ids))

        messages.success(request, "✅ Course added successfully!")
        return redirect("/instructor")

    # Passing categories and subcategories for the form dropdowns
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    
    return render(request, "instructor/add_course.html", {
        "categories": categories,
        "subcategories": subcategories
    })

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)

    if request.method == "POST":
        course.title = request.POST["title"]
        course.description = request.POST["description"]
        course.start_date = request.POST["start_date"]
        course.end_date = request.POST["end_date"]
        course.price = request.POST["price"]
        course.syllabus = request.POST["syllabus"]
        course.prerequisites = request.POST["prerequisites"]
        course.is_active = request.POST["is_active"] == "True"

        if "image" in request.FILES:
            course.image = request.FILES["image"]

        if "video" in request.FILES:
            course.video = request.FILES["video"]

        course.save()
        return redirect("/instructor")

    return render(request, "instructor/edit_course.html", {"course": course})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "course_detail.html", {"course": course})



@login_required
def instructor_profile(request):
    instructor_profile, created = InstructorProfile.objects.get_or_create(user=request.user)
    return render(request, 'instructor/instructor_profile.html', {'instructor_profile': instructor_profile})

@login_required
def update_instructor_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user  # Get the logged-in user
        instructor_profile, created = InstructorProfile.objects.get_or_create(user=user)

        # Update user details
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.save()  # Save user model

        # Update instructor profile details
        instructor_profile.bio = data.get("bio", instructor_profile.bio)
        instructor_profile.experience = data.get("experience", instructor_profile.experience)
        instructor_profile.skills = data.get("skills", instructor_profile.skills)
        instructor_profile.linkedin = data.get("linkedin", instructor_profile.linkedin)
        instructor_profile.github = data.get("github", instructor_profile.github)
        instructor_profile.website = data.get("website", instructor_profile.website)
        instructor_profile.save()  # Save profile model

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False})

# LEARNER VIEWS
@login_required
def learner(request):
    courses = Course.objects.all()
    return render(request, 'learner/learner.html ',{'courses': courses})

@login_required
def learner_profile(request):
    learner_profile = LearnerProfile.objects.get_or_create(user=request.user)
    return render(request, 'learner/learner_profile.html', {'learner_profile': learner_profile})

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


