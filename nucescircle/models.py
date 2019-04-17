from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('circle-home')


JOB_CHOICES = (
    ('it', 'IT'),
    ('mg', 'Management'),
    ('fin', 'Finance'),
    ('art', 'Arts')
)


class Job(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=32, blank=True)
    job_desc = models.TextField(blank=True)
    job_location = models.CharField(max_length=32, blank=True)
    job_field = models.CharField(max_length=6, blank=True)
    job_tags = models.CharField(max_length=255, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('circle-recruit')


JOB_APP_ACCEPTED = 1
JOB_APP_PENDING = 2
JOB_APP_STATUSES = (
    (JOB_APP_ACCEPTED, 'Accepted'),
    (JOB_APP_PENDING, 'Pending'),
)


class JobApplications(models.Model):
    applicant = models.ForeignKey(User, related_name='applicant', on_delete=models.CASCADE)
    job_applied_for = models.ForeignKey(Job, related_name='job_applied_for', on_delete=models.CASCADE)  # has the hirer
    job_app_status = models.IntegerField(choices=JOB_APP_STATUSES, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.applicant.username, self.job_applied_for.job_title)
