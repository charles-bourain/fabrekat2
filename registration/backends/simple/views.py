from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect

from registration import signals
from registration.views import RegistrationView as BaseRegistrationView
from registration.users import UserModel
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic import TemplateView
from registration.forms import LoginForm


class RegistrationView(BaseRegistrationView):
    """
    A registration backend which implements the simplest possible
    workflow: a user supplies a username, email address and password
    (the bare minimum for a useful account), and is immediately signed
    up and logged in).

    """
    success_url = 'registration_complete'

    def register(self, request, form):
        new_user = form.save()
        username_field = getattr(new_user, 'USERNAME_FIELD', 'username')
        new_user = authenticate(
            username=getattr(new_user, username_field), 
            password=form.cleaned_data['password1']
        )

        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.

        """
        return getattr(settings, 'REGISTRATION_OPEN', True)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = 'home'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(
            self.get_context_data(
            form = form,
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)        
        if (form.is_valid()):       
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect('/')

class LogoutView(TemplateView):
    template_name = 'logout.html'
    form_class = LoginForm
    success_url = 'home'

    def post(self, request, *args, **kwargs):
       logout(request)
       return HttpResponseRedirect('/')      







