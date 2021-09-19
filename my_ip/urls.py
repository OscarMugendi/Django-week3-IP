from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.home, name='home'),
    url(r'project/new/',views.new_project,name='new_project'),
    url(r'^profile/',views.profile,name='profile'),
    url(r'^profile/update',views.profile,name='update_profile'),
    url('search/',views.search_projects,name="search"),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)