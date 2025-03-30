from django.contrib import admin
from .models import CustomUser, LearnerProfile, Course, InstructorProfile  # Ensure Course is imported

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type')

@admin.register(LearnerProfile)
class LearnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'courses', 'age', 'state', 'city')

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'courses', 'age', 'state', 'city')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Removed 'instructor' since it's not in your Course model
