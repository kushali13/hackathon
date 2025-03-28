from django.contrib import admin
from django.urls import path
from hackathon import views
from hackathon.views import * 
from django.contrib.auth.views import LoginView  
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name='hackathon'),  
    path('logout/', logout_view, name='logout'), 
    path('login/', views.login, name='login'), 
    path("register/", views.register, name="register"),
    path("courses/", views.courses, name="courses"),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

