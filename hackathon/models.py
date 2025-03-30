from django.contrib.auth.models import AbstractUser
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='media/courses/')

    def __str__(self):
        return self.title

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

class LearnerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) 
    email = models.EmailField(unique=True, blank=True, null=True)
    courses = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
