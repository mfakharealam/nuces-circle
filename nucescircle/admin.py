from django.contrib import admin

from .models import Post, Job, JobApplications

admin.site.register(Post)
admin.site.register(Job)
admin.site.register(JobApplications)
