from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from project import views
from .models import Project
from .forms import ProjectForm

urlpatterns=patterns('',
	url(r'^myprofile/(?P<project_id>[\w-]+)/load_single_step/(?P<step_id>[\w-]+)/$', views.InWorkStepView.as_view(), name='load_single_step_in_work_view'),
    url(r'^create/$', views.ProjectCreateView.as_view(), name='prj_create'),
 	url(r'^edit/(?P<project_id>[\w-]+)$', views.EditProjectView.as_view(), name='prj_edit'),
 	url(r'^edit/(?P<project_id>[\w-]+)/addstep/$', views.create_blank_step, name='add_step'),
	url(r'^edit/(?P<project_id>[\w-]+)/addimage/$', views.ImageCreateView.as_view(), name='add_image'),	
    url(r'^edit/(?P<project_id>[\w-]+)/editstep/(?P<step_id>[\w-]+)/media_upload/$', views.StepMediaView.as_view(), name='media_upload_view'), 
	url(r'^edit/(?P<project_id>[\w-]+)/editstep/$', views.StepEditView.as_view(), name='load_edit_step'),
    url(r'^edit/(?P<project_id>[\w-]+)/editstep/(?P<step_id>[\w-]+)/save_step/$', views.StepEditView.as_view(), name='save_edit_step'),
    url(r'^edit/(?P<project_id>[\w-]+)/editstep/(?P<step_id>[\w-]+)/load_step/$', views.StepView.as_view(), name='load_step'),
	url(r'^edit/(?P<project_id>[\w-]+)/delete/$', views.delete_project, name='deleteproject'),
    url(r'^edit/(?P<project_id>[\w-]+)/update_step_order/$', views.update_step_order, name='update_step_order'),
    url(r'^edit/(?P<project_id>[\w-]+)/editstep/(?P<step_id>[\w-]+)/delete_step/$', views.delete_step, name='delete_step'), 
    url(r'^edit/(?P<project_id>[\w-]+)/editstep/(?P<step_id>[\w-]+)/delete_component/(?P<component_id>[\w-]+)$', views.delete_component, name='delete_component'), 
    url(r'^edit/(?P<project_id>[\w-]+)/editstep/(?P<step_id>[\w-]+)/delete_file/(?P<file_id>[\w-]+)$', views.delete_file, name='delete_file'),   
    url(r'^edit/(?P<project_id>[\w-]+)/editstep/(?P<step_id>[\w-]+)/editor_load_step/$', views.EditorStepView.as_view(), name='editor_load_step'),   		  
    # url(r'^revise/(?P<project_id>[\w-]+)/$', views.ReviseProjectView.as_view(), name='reviseproject'),	  	
	)


if settings.DEBUG:
    #static files(images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))