from django.contrib import admin
from .models import Profile, Education, Skills, Interests, UserConnections

myModels = [Profile, Education, Skills, Interests, UserConnections]  # iterable list
admin.site.register(myModels)
