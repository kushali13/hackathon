from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin URLs
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="user_login"), 
    path("about/", about, name="about"),
    path("logout/", logout_view, name="logout"),
    path("courses/", courses, name="courses"),
    path("course/<int:course_id>/", course_detail, name="course_detail"),
    path('course/<int:course_id>/enroll/', enroll_course, name='enroll_course'),
    path("logout-redirect/", logout_and_redirect, name="logout_redirect"),  # Fixed this line



    # Learner URLs
    path("learner/", learner, name="learner"),
    path('learner/learner-profile/', learner_profile, name='learner_profile'),
    path('learner/learner-profile/update/', update_learner_profile, name='update_learner_profile'),
    path('learner/my-courses/', my_courses, name='learner_my_courses'),
    path("learner/course/<int:course_id>/", learner_course_detail, name="learner_course_detail"),
    path('learner/course/<int:course_id>/enroll/', enroll_course, name='learner_enroll_course'),


    # Insructor URLs
    path("instructor/", instructor, name="instructor"),

    path('instructor-profile/', instructor_profile, name='instructor_profile'),
    path('instructor-profile/update/', update_instructor_profile, name='update_instructor_profile'),
    path("update-profile-picture/", update_profile_picture, name="update_profile_picture"),

    path('instructor/add-course/', add_course, name='add_course'), 
    path("instructor/course/edit/<int:course_id>/", edit_course, name="edit_course"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

