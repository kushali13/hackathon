from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin URLs
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="user_login"), 
    path("logout/", logout_view, name="logout"),
    path("courses/", courses, name="courses"),
    path("course/<int:course_id>/", course_detail, name="course_detail"),

    # Learner URLs
    path("learner/", learner, name="learner"),
    path('learner-profile/', learner_profile, name='learner_profile'),
    path('learner-profile/update/', update_learner_profile, name='update_learner_profile'),

    # Insructor URLs
    path("instructor/", instructor, name="instructor"),
    path('instructor-profile/', instructor_profile, name='instructor_profile'),
    path('instructor-profile/update/', update_instructor_profile, name='update_instructor_profile'),
    path('instructor/add-course/', add_course, name='add_course'), 
    path("instructor/course/edit/<int:course_id>/", edit_course, name="edit_course"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

