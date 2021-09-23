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
    #print(projects)

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
        user = User.objects.get(username=username)

    except:

        raise Http404()

    return render(request, 'profile.html', {"user":user,"profile":profile})


@login_required(login_url='/accounts/login/')
def update_profile(request,username):
    current_user = request.user 
    title = 'Update Profile'
    try:

        requested_profile = Profile.objects.get(user_id = current_user.id)
        if request.method == 'POST':

            form = ProfileForm(request.POST,request.FILES)

            if form.is_valid():
                requested_profile.username = form.cleaned_data['username']
                requested_profile.profile_pic = form.cleaned_data['profile_photo']
                requested_profile.bio = form.cleaned_data['bio']
                requested_profile.email = form.cleaned_data['email']
                requested_profile.contact = form.cleaned_data['contact']

                requested_profile.save_profile()

                return redirect(profile)
        else:
            
            form = ProfileForm()

    except:
        if request.method == 'POST':

            form = ProfileForm(request.POST,request.FILES)

            if form.is_valid():

                new_profile = Profile(username = form.cleaned_data['username'], profile_pic= form.cleaned_data['profile_pic'], bio = form.cleaned_data['bio'], email = form.cleaned_data['email'], contact = form.cleaned_data['contact'], user = current_user)
                new_profile.save_profile()

                return redirect(profile)

        else:

            form = ProfileForm()

    return render(request,'update_profile.html',{"title":title,"current_user":current_user,"form":form})


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


@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user 
    title = 'New Project'
    try:

        new_project = Project.objects.get(project_id = project.id)
        
        if request.method == 'POST':

            form = ProjectForm(request.POST,request.FILES)

            if form.is_valid():
                new_project.title = form.cleaned_data['title']
                new_project.project_image = form.cleaned_data['project_image']
                new_project.description = form.cleaned_data['description']
                new_project.live_link = form.cleaned_data['live_link']
                new_project.github_link = form.cleaned_data['github_link']

                new_project.save_project()

                return redirect(home)
        else:
            
            form = ProjectForm()

    except:
        if request.method == 'POST':

            form = ProjectForm(request.POST,request.FILES)

            if form.is_valid():

                ex_new_project = Project(title = form.cleaned_data['title'], project_image= form.cleaned_data['project_image'], description = form.cleaned_data['description'], live_link = form.cleaned_data['live_link'], github_link = form.cleaned_data['github_link'], user = current_user)
                ex_new_project.save_project()

                return redirect(home)

        else:

            form = ProjectForm()

    return render(request,'new_project.html',{"title":title,"current_user":current_user,"form":form})