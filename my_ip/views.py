import os
import json

from decouple import config, Csv
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.templatetags.static import static
from django.http  import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http  import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.defaulttags import register
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .email import send_welcome_email

from .models import Profile, Project
from .forms import ProfileForm, ReviewForm, ProjectForm

import datetime as dt

# Create your views here.

def home(request):

    if request.GET.get('search_term'):
        projects = Project.search_project(request.GET.get('search_term'))

    else:

        projects = Project.objects.all()

    return render(request,'home.html', {'projects':projects})


def my_projects(request,id):
    
    try:
        project = Project.objects.get(pk = id)

    except DoesNotExist:

        raise Http404()

    current_user = request.user
    reviews = Review.objects.all()

    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():
            
            design_rating = form.cleaned_data['design']
            content_rating = form.cleaned_data['content']
            usability_rating = form.cleaned_data['usability']

            review = Review()
            review.project = project
            review.user = current_user

            review.design_rating = design_rating
            review.content_rating = content_rating
            review.usability_rating = usability_rating

            review.save()

    else:
        form = ReviewForm()

    return render(request, 'image.html', {"project": project, 'form':form, 'reviews':reviews})



@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user

    if request.method == 'POST':

        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():

            project = form.save(commit=False)
            project.user = current_user
            project.save()

        return redirect('home')

    else:

        form = ProjectForm()

    return render(request, 'new_project.html', {"form": form})



@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user = request.user

    if request.method == 'POST':

        form = ProfileForm(request.POST, request.FILES, instance=current_user.profile)

        print(form.is_valid())

        if form.is_valid():

            image = form.save(commit=False)
            image.user = current_user
            image.save()

        return redirect('home')

    else:

        form = ProfileForm()

    return render(request, 'update_profile.html', {"form": form})



def search_projects(request):
    
    if 'project' in request.GET and request.GET["project"]:

        search_term = request.GET.get("project")
        searched_projects = Project.search_projects(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message": message, "projects": searched_projects})

    else:
        message = "Invalid search parameters!"
        
        return render(request, 'search.html', {"message": message})
