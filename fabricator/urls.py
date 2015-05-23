from django.shortcuts import render

from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from fabricator import views 


urlpatterns=patterns('',
	url(r'^create_fabricator/$', views.FabricatorCreateView.as_view(), name='fab_create'),
	url(r'^(?P<name>[\w-]+)/$', views.fabricator_detail, name='fab_detail'),
	)