from django.test import TestCase
from . models import Profile, Project


class ProfileTestClass(TestCase):
    
    def setUp(self):
        self.profile = Profile(id = 1)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile)) 



class ProjectTestClass(TestCase):

    def setUp(self):
        self.project = Project(id = 1) 

    def test_instance(self):
        self.assertTrue(isinstance(self.project, Project)) 