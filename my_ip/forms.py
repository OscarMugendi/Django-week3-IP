from .models import Profile, Project
from django import forms
from django.forms import ModelForm, Textarea, IntegerField


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user',]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [ 'usability', 'design', 'content']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user',]