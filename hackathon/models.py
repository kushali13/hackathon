from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import path

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='media/courses/')
    instructor = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_enrolled = models.BooleanField(default=False)
    enrollment_start_date = models.DateField()
    enrollment_end_date = models.DateField()
    enrollment_limit = models.PositiveIntegerField()
    enrolled_students = models.PositiveIntegerField(default=0)
    syllabus = models.TextField()
    prerequisites = models.TextField()
    course_materials = models.TextField()
    

    def __str__(self):
        return f"{self.title} taught by {self.instructor.username}"  

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('learner', 'Learner'),
        ('instructor', 'Instructor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='learner')

    # Fixing the clash issues
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  # Change related_name to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  # Change related_name to avoid conflict
        blank=True
    )


