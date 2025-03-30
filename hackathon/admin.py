from django.contrib import admin
from .models import Course , CustomUser

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor')  # Display course title in admin panel

admin.site.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type') 
    