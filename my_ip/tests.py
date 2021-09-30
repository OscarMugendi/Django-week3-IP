from django.test import TestCase
from . models import *


class ProfileTestClass(TestCase):

    def setUp(self):
        self.profile = Profile(id = 1)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile)) 


class ProjectTestClass(TestCase):

    def setUp(self):
        self.Projo = Project.objects.create(title='Projo')

    def test_instance(self):
        self.Projo.save()
        self.assertTrue(isinstance(self.Projo, Project))

    def test_all_projects(self):
        self.Projo.save()
        projects = Project.all_projects()
        self.assertTrue(len(projects) > 0)


class RatingTestClass(TestCase):
    
    def setUp(self):
        self.Projo2 = Project.objects.create(title='Projo2')
        self.Projo2.save()
        self.Rate = Rating.objects.create(design='6', usability='8', content ='4')

    def test_instance(self):
        self.Rate.save()
        self.assertTrue(isinstance(self.Rate, Rating))