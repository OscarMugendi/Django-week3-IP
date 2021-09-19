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