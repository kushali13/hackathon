from django.contrib import admin
from .models import CustomUser, LearnerProfile

admin.site.register(CustomUser)   # Ensure CustomUser is registered
admin.site.register(LearnerProfile)  # Register LearnerProfile model
