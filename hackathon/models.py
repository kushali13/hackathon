from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('learner', 'Learner'),
        ('instructor', 'Instructor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='learner')

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generate slug automatically
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generate slug automatically
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='media/courses/')
    video_url = models.URLField(blank=True, null=True)  # Stores video links (YouTube/Vimeo)
    level = models.CharField(max_length=50, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    language = models.CharField(max_length=50, choices=[('english', 'English'), ('spanish', 'Spanish'), ('french', 'French')])
    duration = models.CharField(max_length=50)  # Duration in hours/days/weeks
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    categories = models.ManyToManyField(Category, related_name="courses")  
    subcategories = models.ManyToManyField(Subcategory, related_name="courses")  # Many-to-Many for flexibility
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    content = models.TextField()
    prerequisites = models.TextField()
    course_outcomes = models.TextField()
    students_enrolled = models.ManyToManyField(CustomUser, related_name="enrolled_courses", blank=True)  

class LearnerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="learner_profile")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="media/learners/", blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    enrolled_courses = models.ManyToManyField('Course', related_name="learners", blank=True)  # Tracks enrolled courses  

    def __str__(self):
        return f"Learner: {self.user.username}"


class InstructorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="instructor_profile")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="media/instructors/", blank=True, null=True)
    experience = models.IntegerField(default=0)  
    skills = models.CharField(max_length=255, blank=True, null=True)  
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)  # Admin can verify instructors

    def __str__(self):
        return f"Instructor: {self.user.username} {'(Verified)' if self.is_verified else '(Pending)'}"


