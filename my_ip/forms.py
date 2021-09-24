from .models import Profile, Project
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, IntegerField, EmailField, CharField, Form, ImageField


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

        fields = ['title', 'project_image', 'description', 'live_link', 'github_link']


# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = ['design', 'usability', 'content']


class ProfileForm(forms.Form):

    profile_pic = forms.ImageField(required = False, label = 'Image Field') 
    bio = forms.CharField(label='Bio',max_length=300)
    email = forms.EmailField(label='Email')
    contact = forms.IntegerField(label='Contacts')