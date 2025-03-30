from django.urls import path
from .views import home, register, user_login, learner, instructor, courses, logout_view

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="user_login"),  # Changed from 'login' to 'user_login'
    path("learner/", learner, name="learner"),
    path("instructor/", instructor, name="instructor"),
    path("courses/", courses, name="courses"),
    path("logout/", logout_view, name="logout"),
]
