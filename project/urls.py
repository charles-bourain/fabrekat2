from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from project import views

urlpatterns=patterns('',
	url(r'^create/$', views.ProjectCreateView.as_view(), name='prj_create'),
 	url(r'^(?P<id>\d+)/$', views.project_detail, name='prj_detail'),
 	url(r'^saved_projects/$', views.my_saved_projects, name='my_saved_projects'),
 	url(r'^edit/(?P<id>\d+)/$', views.ProjectEditView.as_view(), name='prj_edit'),
)

if settings.DEBUG:
    #static files(images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))