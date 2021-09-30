from django.conf.urls import url
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.home, name='home'),
    path('account/', include('django.contrib.auth.urls')),
    path('profile/<id>/', views.profile, name='profile'),
    path('profile/<id>/update/', views.update_profile, name='update_profile'),
    path('project/new/', views.new_project, name='new_project'),
    path('project/<title>/reviews/', views.single_project, name='single_project'),
    path('project/<title>/', views.single_project, name='project'),
    path('project/<id>/review/', views.add_review, name='review'),
    url('search/',views.search_projects,name="search"),
    url(r'^api/profiles/$', views.ProfileView.as_view(), name='api_profiles'),
    url(r'^api/projects/$', views.ProjectView.as_view(), name='api_projects')
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)