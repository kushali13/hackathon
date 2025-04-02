from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')




@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',) 
