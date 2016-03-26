from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from filebrowser.sites import site

urlpatterns = patterns('',
   (r'^admin/filebrowser/', include(site.urls)),
   (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),   
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^project/', include('project.urls')),
	url(r'^account/', include('registration.backends.simple.urls')),
	url(r'^', include('haystack.urls')),
	url(r'^', include('follow.urls')),
	# url(r'^', include('fabricator.urls')),
	url(r'^autocomplete/', include('autocomplete_light.urls')),
	url(r'^', include('publishedprojects.urls')),
    url(r'^profile/', include('designprofiles.urls')),

)


#Put these in so Server/media/image/ in the HTML for project detail will work
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
