from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from designprofiles import views

urlpatterns=patterns('',
    url(r'^create/$', views.DesignProfileCreateView.as_view(), name='design_profile_create'),  
    url(r'^edit/(?P<slug>[\w-]+)$', views.DesignProfileEditView.as_view(), name='design_profile_edit'),    
    url(r'^(?P<slug>[\w-]+)$', views.DesignProfileDetailView.as_view(), name='design_profile_detail'),      
    )

