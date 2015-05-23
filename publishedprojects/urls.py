from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
import views

urlpatterns=patterns('',
 	url(r'^project/(?P<project_id>[\w-]+)/$', views.published_project_detail, name='pub_detail'), 	
)
if settings.DEBUG:
    #static files(images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))