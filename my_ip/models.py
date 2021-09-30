from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, Max, Min
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import ImageField

import datetime as dt
import numpy as np

# Create your models here.

class Project(models.Model):

    title=models.CharField(max_length=30, null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="project", null=True)

    project_image=models.ImageField(upload_to='images/projects/', blank=True, default = 0, null=True)
    description=models.TextField(max_length=320, blank=True, null=True)
    live_link=models.URLField(blank=True, null=True)
    github_link=models.URLField(blank=True, null=True)

    date=models.DateField(auto_now=True, blank=True, null=True)


    def delete_project(self):
        self.delete()

    @classmethod
    def search_project(cls, search_term):
        project = Project.objects.filter(title__icontains=search_term)
        return project

    @classmethod
    def all_projects(cls):
        return cls.objects.all()

    @classmethod
    def get_project_by_id(cls, id):
        projects = cls.objects.get(pk=id)
        return projects

    def save_project(self):
        self.save()

    def __str__(self):
        return f'{self.title}'



class Profile(models.Model):

    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=True)

    bio = models.CharField(max_length=500, null=True, blank=True, default="bio")
    profile_pic = models.ImageField(upload_to='images/profiles/', blank=True, default = 0, null=True)

    project=models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, default="email", null=True)
    contact = models.IntegerField(blank=True, default=0, null=True)

    def __str__(self):
        return f'{self.user.username}'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        


class Rating(models.Model):

    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    design = models.IntegerField(choices=rating, default=0, blank=True)
    usability = models.IntegerField(choices=rating, blank=True)
    content = models.IntegerField(choices=rating, blank=True)
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rating', null=True)

    def save_rating(self):
        self.save()

    def __str__(self):
        return f'{self.project} Rating'

    @classmethod
    def get_ratings(cls,id):
        ratings = Rating.objects.filter(project_id=id).all()
        return ratings