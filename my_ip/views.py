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

from .models import *
from .forms import *

import datetime as dt

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer, ProjectSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly

# Create your views here.


def home(request):
    projects = Project.all_projects()
    #ratings = Rating.get_ratings(id)

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
def profile(request, id):
    user = request.user
    user_id = user.id

    projects = Project.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    userf = User.objects.get(pk=user_id)

    if userf:
        print('User found!')
        profile = Profile.objects.get(user=userf)

    else:

        print('User not found!')

    return render (request, 'profile.html', {'projects':projects, 'profile':profile, 'user':user,})


@login_required(login_url='/accounts/login/')
def update_profile(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            form.save()

            return redirect('profile', user.id)
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'update_profile.html', {'form': form})
    

def single_project(request, title):
    project = Project.objects.get(title=title)

    current_user = request.user

    return render (request, 'project.html', {'project':project})


@login_required(login_url='/accounts/login/')
def search_projects(request):

    if 'title' in request.GET and request.GET["title"]:
        search_term = request.GET.get("title")
        searched_project = Project.search_project(search_term)
        message = search_term

        return render(request,'search.html',{"message":message, "searched_project":searched_project})

    else:

        message = "Invalid search parameters!"
        return render(request,'search.html', {"message":message})


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
                new_project.user_id= current_user
                new_project.image_id = current_image

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


@login_required(login_url='/accounts/login/')
def project(request, post):
    project = Project.objects.get(title=project)
    ratings = Rating.objects.filter(user=request.user, project=project).first()
    rating_status = None

    if rating is None:
        rating_status = False

    else:
        rating_status = True

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.project = project
            rating.save()
            project_ratings = Rating.objects.filter(project=project)

            design_ratings = [d.design for d in project_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in project_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in project_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3

            rating.design_average = round(design_average, 2)
            rating.usability_average = round(usability_average, 2)
            rating.content_average = round(content_average, 2)
            rating.score = round(score, 2)
            rating.save()

            return HttpResponseRedirect(request.path_info)

            print(score)

    return render(request, 'project.html',{'project': project,'ReviewForm': form,'rating_status': rating_status})


@login_required(login_url='/accounts/login/')
def add_review(request, id):
    project = Project.objects.get(id=id)
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

        return render(request,'review.html',{'project': project, "user":current_user,"form":form})



class ProfileView(APIView):

    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)

        return Response(serializers.data)


    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)

        if serializers.is_valid():
            serializers.save()

            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectView(APIView):

    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)

        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)

        if serializers.is_valid():
            serializers.save()

            return Response(serializers.data, status=status.HTTP_201_CREATED)
            
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)