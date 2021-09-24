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

from .models import Profile, Project
from .forms import ProfileForm, ProjectForm

import datetime as dt

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer, ProjectSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly

# Create your views here.


def home(request):
    projects = Project.all_projects()
    current_user = request.user

    print(projects)

    return render(request,"home.html",{"projects":projects})


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
def update_profile(request,id):
    current_user = request.user 
    title = 'Update Profile'
    try:

        requested_profile = Profile.objects.get(user_id = current_user.id)
        if request.method == 'POST':

            form = ProfileForm(request.POST,request.FILES)

            if form.is_valid():
                requested_profile.profile_pic = form.cleaned_data['profile_pic']
                requested_profile.bio = form.cleaned_data['bio']
                requested_profile.email = form.cleaned_data['email']
                requested_profile.contact = form.cleaned_data['contact']
                requested_profile.user_id= current_user
                requested_profile.image_id = current_image

                requested_profile.save_profile()

                return redirect(profile)
        else:
            
            form = ProfileForm()

    except:
        if request.method == 'POST':

            form = ProfileForm(request.POST,request.FILES)

            if form.is_valid():

                new_profile = Profile(profile_pic = form.cleaned_data['profile_pic'], bio = form.cleaned_data['bio'], email = form.cleaned_data['email'], contact = form.cleaned_data['contact'], user = current_user)
                new_profile.save_profile()

                return redirect(profile)

        else:

            form = ProfileForm()

    return render(request,'update_profile.html',{"title":title,"current_user":current_user,"form":form})


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


# @login_required(login_url='/accounts/login/')
# def add_review(request):
#     project = Project.objects.get()
#     current_user = request.user
#     if request.method == 'POST':

#         form = ReviewForm(request.POST)

#         if form.is_valid():
#             design = form.cleaned_data['design']
#             usability = form.cleaned_data['usability']
#             content = form.cleaned_data['content']
#             review = form.save(commit=False)
#             review.project = project
#             review.design = design
#             review.usability = usability
#             review.content = content
#             review.save()

#             return redirect('home')
#     else:

#         form = ReviewForm()

#         return render(request,'review.html',{"user":current_user,"form":form})

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