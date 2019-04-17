from django.contrib import admin
from .models import Profile, Education, Skills, Interests, UserConnections, Recruiter

myModels = [Profile, Education, Skills, Interests, UserConnections, Recruiter]  # iterable list
admin.site.register(myModels)
