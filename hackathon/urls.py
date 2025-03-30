from django.urls import path
from .views import home, register, user_login, learner, instructor, courses, logout_view,learner_profile,update_learner_profile,instructor_profile,update_instructor_profile , add_course

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="user_login"),  
    path("learner/", learner, name="learner"),
    path("instructor/", instructor, name="instructor"),
    path("courses/", courses, name="courses"),
    path("logout/", logout_view, name="logout"),
    path('learner-profile/', learner_profile, name='learner_profile'),
    path('learner-profile/update/', update_learner_profile, name='update_learner_profile'),
    path('instructor-profile/', instructor_profile, name='instructor_profile'),
    path('instructor-profile/update/', update_instructor_profile, name='update_instructor_profile'),
    path('instructor/add-course/', add_course, name='add_course'), 
]
