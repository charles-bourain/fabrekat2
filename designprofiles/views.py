from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, TemplateView
from .models import DesignProfile
from django.contrib.auth.decorators import login_required
from .forms import DesignProfileForm
from project.mixins import LoginRequiredMixin
from publishedprojects.models import PublishedProject
from project.models import Project
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import WorkingStepOrder
from publishedprojects.models import PublishedProject
from projectsteps.models import StepOrder
from designprofiles.utils import complete_step_toggle


# Create your views here.

class DesignProfileCreateView(LoginRequiredMixin, CreateView):
    model = DesignProfile
    template_name = 'designprofiles/design_profile_create.html'
    success_url = 'design_profile_detail'
    form_class = DesignProfileForm
    
    def get(self, request, *args, **kwargs):
        try:
            user_id = User.objects.get(username = self.request.user).id
            print user_id
            user_profile = DesignProfile.objects.get(user = user_id)
            print user_profile
            return redirect('design_profile_detail', slug = self.request.user)

        except:
            self.object = None
            form_class = self.get_form_class()
            return self.render_to_response(
                self.get_context_data(
                form = form_class,
                    )
                )
    def post(self, request, *args, **kwargs):
        print 'Post Initiated....'
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        print 'is_Valid Check on Forms....'
        if (
            form.is_valid()
            ):      

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.slug = self.request.user
        self.object = form.save()

        return HttpResponseRedirect('design_profile_detail', slug = self.object.user)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form = form,
            )
        )



class DesignProfileEditView(LoginRequiredMixin, UpdateView):
    model = DesignProfile


class DesignProfileDetailView(TemplateView):
    template_name = 'designprofiles/design_profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DesignProfileDetailView, self).get_context_data(**kwargs)

        #Getting Users Created by The User that is being Viewed        
        user_slug = self.kwargs['slug']
        user = User.objects.get(username = user_slug)
        user_projects = Project.objects.filter(project_creator = user)
        user_projects_id = user_projects.values_list('id', flat = True)

        #Gets Projects Created by User and adds them to context dict
        user_published_projects = PublishedProject.objects.filter(project_link = user_projects_id)
        context['projects'] = user_published_projects


        user_profile = DesignProfile.objects.get(user = user)
        context['user_profile'] = user_profile

        #gets projects current user is working on
        in_work_steps = WorkingStepOrder.objects.filter(user = user_profile)
        in_work_projects = in_work_steps.distinct('project')
        in_work_step_order = in_work_steps.order_by('steporder__order')


        # project_percent_complete={}
        # step_total=0
        # step_complete=0
        # for project in in_work_projects:
        #     for step in in_work_steps:
        #         if step.project == project.project:
        #             step_total=step_total+1
        #             if step.complete==True:
        #                 step_complete=step_complete+1
        #     project_percent_complete[project.project]=step_complete/step_total*100

        #     print project_percent_complete





        # context['project_percent_complete']=project_percent_complete



        context['in_work_projects'] = in_work_projects
        context['in_work_step_order'] = in_work_step_order

        return context


#View for the Designer to View their Own Profile
class MyDesignProfileView(DesignProfileDetailView, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        for steporder in context['in_work_step_order']:
            step = steporder.steporder.step
            if 'complete_toggle_%s' % steporder.id in request.POST:
                complete_step_toggle(request, steporder)
                return HttpResponseRedirect(request.user)


from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)