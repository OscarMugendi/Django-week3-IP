from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, IntegerField, EmailField, CharField, Form, ImageField


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['design', 'usability', 'content']


class ProfileForm(forms.Form):
    class Meta:
        model = Profile
        exclude = ('user', 'project')