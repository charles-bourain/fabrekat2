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
 	url(r'^edit/(?P<project_id>[\w-]+)$', views.EditProjectView.as_view(), name='prj_edit'),
 	url(r'^edit/(?P<project_id>[\w-]+)/addstep/$', views.StepCreateView.as_view(), name='add_step'),
	url(r'^edit/(?P<project_id>[\w-]+)/addimage/$', views.ImageCreateView.as_view(), name='add_image'),	
	url(r'^edit/editstep/(?P<id>[\w-]+)/$', views.edit_step, name='edit_step'),
	url(r'^edit/(?P<project_id>[\w-]+)/delete/$', views.delete_project, name='deleteproject'),		  
    url(r'^revise/(?P<project_id>[\w-]+)/$', views.ReviseProjectView.as_view(), name='reviseproject'),	  	
	)


if settings.DEBUG:
    #static files(images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))