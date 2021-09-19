from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from pyuploadcare.dj.models import ImageField
from django.db.models import Avg, Max, Min
from django.core.validators import MaxValueValidator, MinValueValidator

import datetime as dt
import numpy as np

# Create your models here.

class Project(models.Model):
    title=models.CharField(max_length=30)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    image=models.ImageField(upload_to='images/projects/')
    description=models.TextField(max_length=320)
    live_link=models.URLField()
    github_link=models.URLField()

    date=models.DateField(auto_now=True)

    design=models.IntegerField(default=0)
    usability=models.IntegerField(default=0)
    content=models.IntegerField(default=0)

    class Meta:
        ordering=['-title']

    def __str__(self):
        self.title

    def average_design(self):
        design_ratings = list(map(lambda x: x.design_rating, self.reviews.all()))
        return np.mean(design_ratings)

    def average_usability(self):
        usability_ratings = list(map(lambda x: x.usability_rating, self.reviews.all()))
        return np.mean(usability_ratings)

    def average_content(self):
        content_ratings = list(map(lambda x: x.content_rating, self.reviews.all()))
        return np.mean(content_ratings)

    def save_project(self):
        self.save()

    @classmethod
    def search_projects(cls,search_term):
        search_results=cls.objects.filter(title__icontains=search_term)
        return search_results



class Profile(models.Model):

    class Meta:
        db_table = 'profile'

    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    bio = models.TextField(max_length=200, null=True, blank=True, default="bio")
    profile_pic = models.ImageField(upload_to='images/profiles/', null=True, blank=True, default= 0)

    project=models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    email = models.EmailField(default="email")
    contact=models.IntegerField(default=0)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)


    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()


    @classmethod
    def search_profiles(cls, search_term):
        profile_search_results = cls.objects.filter(user__username__icontains=search_term)
        return profile_search_results

    @property
    def image_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url

    def __str__(self):
        return self.user.username