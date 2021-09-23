from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, Max, Min
from django.core.validators import MaxValueValidator, MinValueValidator

import datetime as dt
import numpy as np

# Create your models here.

class Project(models.Model):

    class Meta:
        db_table = 'project'


    title=models.CharField(max_length=30)
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="project")

    project_image=models.ImageField(upload_to='images/projects/', blank=True)
    description=models.TextField(max_length=320, blank=True)
    live_link=models.URLField(blank=True)
    github_link=models.URLField(blank=True)

    date=models.DateField(auto_now=True, blank=True)

    class Meta:
        ordering=['-title']


    def delete_project(self):
        self.delete()

    @classmethod
    def search_project(cls, title):
        return cls.objects.filter(title__icontains=title).all()

    @classmethod
    def all_projects(cls):
        return cls.objects.all()

    def save_project(self):
        self.save()

    def __str__(self):
        return self.title



class Profile(models.Model):
    class Meta:
        db_table = 'profile'

    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    #username = models.CharField(max_length=30, blank=True, default='user')

    bio = models.CharField(max_length=500, null=True, blank=True, default="bio")
    profile_pic = models.ImageField(upload_to='images/profiles/', blank=True, default = 0)

    project=models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, default="email")
    contact = models.IntegerField(blank=True, default=0)


    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

        post_save.connect(create_user_profile, sender=User)


    def save_profile(self):
        self.save()


    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()


    def __str__(self):
        return self.user.username
        


# class Rating(models.Model):
#     class Meta:
#         db_table = 'rating'


#     rating = (
#         (1, '1'),
#         (2, '2'),
#         (3, '3'),
#         (4, '4'),
#         (5, '5'),
#         (6, '6'),
#         (7, '7'),
#         (8, '8'),
#         (9, '9'),
#         (10, '10'),
#     )

#     design = models.IntegerField(choices=rating, default=0, blank=True)
#     usability = models.IntegerField(choices=rating, blank=True)
#     content = models.IntegerField(choices=rating, blank=True)
#     score = models.FloatField(default=0, blank=True)
#     design_average = models.FloatField(default=0, blank=True)
#     usability_average = models.FloatField(default=0, blank=True)
#     content_average = models.FloatField(default=0, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user')
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rating', null=True)

#     def save_rating(self):
#         self.save()

#     @classmethod
#     def get_ratings(cls, id):
#         ratings = Rating.objects.filter(project_id=id).all()
#         return ratings

#     def __str__(self):
#         return f'{self.project} Rating'