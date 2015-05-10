from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from project import views
from .models import Project
from .forms import ProjectForm

urlpatterns=patterns('',
	url(r'^create/$', views.ProjectCreateView.as_view(), name='prj_create'),
 	url(r'^my_projects/$', views.my_projects, name='my_projects'),	
  	url(r'^saved_projects/$', views.my_saved_projects, name='my_saved_projects'),	
 	url(r'^unpublished/(?P<project_id>[\w-]+)/$', views.unpublished_project_detail, name='unpub_detail'),
 	url(r'^(?P<project_id>[\w-]+)/$', views.published_project_detail, name='pub_detail'), 	
 	url(r'^edit/(?P<project_id>[\w-]+)$', views.edit_project, name='prj_edit'),
	)


if settings.DEBUG:
    #static files(images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))