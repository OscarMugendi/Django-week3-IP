from .models import Profile, Project
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, IntegerField, EmailField, CharField, Form, ImageField


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

        fields = ['title', 'project_image', 'description', 'live_link', 'github_link']

    # title = forms.CharField(label='Title',max_length = 30)
    # project_image = forms.ImageField(label = 'Image Field') 
    # description = forms.CharField(label='Description',max_length=320)
    # live_link = forms.URLField(label='Live Link')
    # github_link = forms.URLField(label='Github Link')


# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = ['design', 'usability', 'content']


class ProfileForm(forms.Form):
    username = forms.CharField(label='Username',max_length = 30)
    profile_pic = forms.ImageField(label = 'Image Field') 
    bio = forms.CharField(label='Bio',max_length=300)
    email = forms.EmailField(label='Email')
    contact = forms.IntegerField(label='Contacts')