from django.contrib import admin
from django.urls import path
from hackathon import views
from hackathon.views import logout_view  
from django.contrib.auth.views import LoginView  

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name='hackathon'),  
    path('logout/', logout_view, name='logout'), 
    path('login/', LoginView.as_view(), name='login'), 
]
