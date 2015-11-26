import re

from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from designprofiles.models import DesignProfile
from project.models import Project
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test


class RequireLoginMiddleware(object):
    """
    Middleware component that wraps the login_required decorator around
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and
    define LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS in your
    settings.py. For example:
    ------
    LOGIN_REQUIRED_URLS = (
        r'/topsecret/(.*)$',
    )
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$',
        r'/topsecret/logout(.*)$',
    )
    ------
    LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must
    be a valid regex.

    LOGIN_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly
    define any exceptions (like login and logout URLs).
    """
    def __init__(self):
        self.required = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS)
        self.exceptions = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)
        self.ownership = tuple(re.compile(url) for url in settings.OWNERSHIP_REQUIRED_URLS)




    def process_view(self, request, view_func, view_args, view_kwargs):
        # No need to process URLs if user already logged in

        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path):
                return None

        # Requests matching a restricted URL pattern are returned
        # wrapped with the login_required decorator
        for url in self.required:
            if url.match(request.path):
                return login_required(view_func)(request, *view_args, **view_kwargs)

        for url in self.ownership:
            if url.match(request.path):
                if request.user.is_authenticated() and self.check_ownership(request, view_func):
                    print 'Ownship Check is GOOD'
                    return None
                else:
                    return HttpResponseRedirect('/') 


        # Explicitly return None for all non-matching requests
        return None

    def check_ownership(self, request, view_func):
        requesting_user = request.user
        print 'USERNAME =',requesting_user.username
        print 'PATH =',request.path
        path = request.path
        response = False
        print 'OWNERSHIP CHECK - - - - - - - '
        if str(requesting_user.username) in path:
            print str(requesting_user).upper()

        if 'myprofile' in path and str(requesting_user.username) in path:
            print 'This is a Profile View'
            try:
                DesignProfile.objects.get(user = requesting_user)
                response = True
            except:
                pass
        elif '/project/edit/'in path:
            print 'This is a Project Edit View'
            project_id_compiler = re.compile('(?<=(\/edit\/))(\w*)')
            try:
                project_regex_obj = project_id_compiler.search(path)
                project_id = project_regex_obj.group(0)
                print 'PROJECT ID =',project_id
                project = Project.objects.get(project_id = project_id)
                if project.project_creator == requesting_user:
                    response = True
            except:
                pass

        return response