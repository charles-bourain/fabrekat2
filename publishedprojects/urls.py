from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from project import views

urlpatterns=patterns('',
 	url(r'^project/(?P<project_id>[\w-]+)/$', views.PublishProjectDetailView.as_view(), name='pub_detail'), 	
)
if settings.DEBUG:
    #static files(images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))