import os
import json

from decouple import config, Csv
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.templatetags.static import static
from django.http  import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http  import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.defaulttags import register
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate
from .email import send_welcome_email

from .models import Profile, Project, Rating
from .forms import ProfileForm, ReviewForm, ProjectForm

import datetime as dt

# Create your views here.


def home(request):
    projects = Project.all_projects()
    #ratings = Project.ratings.get_ratings()
    profile = Profile.get_profile()
    print(projects)

    current_user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']

            rating = form.save(commit=False)

            rating.project = project
            rating.design = design
            rating.usability = usability
            rating.content = content

            rating.save()

        return redirect('home')

    else:
        form = ReviewForm()

    return render(request,"home.html",{"projects":projects,"form": form,"profile":profile})


@login_required(login_url='/accounts/login/')
def profile(request, username):
    try:
        user = Profile.objects.get(username=username)

    except:

        raise Http404()

    return render(request, 'profile.html', {"user":user,"profile":profile})


@login_required(login_url='/accounts/login/')
def update_profile(request, username):
    user = User.objects.get(username=username)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, request.user.profile)
        
        if form.is_valid():
            form.save()

            return redirect('profile', user.username)

    else:
        form = ProfileForm(request.user.profile)

    return render(request, 'update_profile.html', {'form': form})


@login_required(login_url='/accounts/login/')
def project(request, post):
    project = Project.objects.get(title=project)
    ratings = Rating.objects.filter(user=request.user, project=project).first()
    rating_status = None

    if ratings is None:
        rating_status = False

    else:
        rating_status = True

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project = project
            rate.save()
            project_ratings = Rating.objects.filter(project=project)

            design_ratings = [d.design for d in project_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in project_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in project_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3

            print(score)

            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()

            return HttpResponseRedirect(request.path_info)

    else:
        form = ReviewForm()

    return render(request, 'project.html',{'project': project,'ReviewForm': form,'rating_status': rating_status})


def search_projects(request):

    if request.method == 'GET':

        title = request.GET.get("title")
        results = Project.objects.filter(title__icontains=title).all()

        print(results)

        message = f'title'

        return render(request, 'search.html',{'results': results,'message': message})

    else:

        message = "Invalid Parameters!"

    return render(request, 'search.html', {'message': message})
