from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from designprofiles import views

urlpatterns=patterns('',
    url(r'^create/$', views.DesignProfileCreateView.as_view(), name='design_profile_create'),  
    url(r'^myprofile/(?P<slug>[\w-]+)$', views.MyProfileView.as_view(), name='my_profile'),    
    url(r'^(?P<slug>[\w-]+)$', views.DesignProfileDetailView.as_view(), name='design_profile_detail'),
    url(r'^myprofile/(?P<slug>[\w-]+)/set_project_in_work/(?P<project_id>[\w-]+)$', views.toggle_project_in_work, name='project_in_work'),
    url(r'^myprofile/(?P<slug>[\w-]+)/(?P<project_id>[\w-]+)/(?P<step_id>[\w-]+)/toggle_step$', views.toggle_step_complete, name='toggle_step_complete'),       
    )

