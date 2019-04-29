from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accomplishments = models.CharField(max_length=255, blank=True)
    skills = models.CharField(max_length=255, blank=True)
    experiences = models.CharField(max_length=255, blank=True)
    interests = models.CharField(max_length=255, blank=True)
    grad_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    friends = models.ManyToManyField("Profile", blank=True)  # to have a list of all the associated other user models

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return "/users/{}"

    def save(self, *args, **kwargs):  # to make the uploading faster
        super(Profile, self).save(*args, **kwargs)
        profile_img = Image.open(self.image.path)
        if profile_img.height > 300 or profile_img.width > 300:
            new_size = (300, 300)
            profile_img.thumbnail(new_size)
            profile_img.save(self.image.path)


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=255, blank=False)
    industry = models.CharField(max_length=255, blank=True)


class Education(models.Model):
    school = models.CharField(max_length=255, blank=False)
    degree = models.CharField(max_length=255, blank=True)
    study_field = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=1023, blank=True)
    grad_year = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.school, self.degree, self.grad_year}'

    def get_absolute_url(self):
        return reverse('profile')


class WorkExperience(models.Model):
    exp_title = models.CharField(max_length=255, blank=False)
    company = models.CharField(max_length=255, blank=True)
    start_year = models.DateField(blank=True, null=True)
    end_year = models.DateField(blank=True, null=True)
    description = models.TextField(max_length=1023, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.exp_title, self.company}'

    def get_absolute_url(self):
        return reverse('profile')


class Interests(models.Model):
    frameworks = models.CharField(max_length=255, blank=True)
    languages = models.CharField(max_length=255, blank=True)
    technologies = models.CharField(max_length=255, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.frameworks, self.languages, self.technologies}'

    def get_absolute_url(self):
        return reverse('profile')


class Skills(models.Model):
    skill = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.skill}'

    def get_absolute_url(self):
        return reverse('profile')


RELATIONSHIP_CONNECTED = 1
RELATIONSHIP_PENDING = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_CONNECTED, 'Connected'),
    (RELATIONSHIP_PENDING, 'Pending'),
)


class UserConnections(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    conn_status = models.IntegerField(choices=RELATIONSHIP_STATUSES, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)  # set only when created

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)
