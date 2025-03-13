
from django.contrib import admin
from django.urls import path,include
from hackathon import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('hackathon.urls'))
]
