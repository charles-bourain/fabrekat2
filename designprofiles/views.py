from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, TemplateView
from .models import DesignProfile
from django.contrib.auth.decorators import login_required
from .forms import DesignProfileForm
from project.mixins import LoginRequiredMixin
from publishedprojects.models import PublishedProject
from project.models import Project, ProjectImage
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import WorkingStepOrder
from publishedprojects.models import PublishedProject
from projectsteps.models import StepOrder
from designprofiles.utils import complete_step_toggle


from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

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


class DesignProfileDetailView(TemplateView):
    template_name = 'designprofiles/design_profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DesignProfileDetailView, self).get_context_data(**kwargs)


        #Getting Projects Created by The User that is being Viewed        
        user_slug = self.kwargs['slug']
        user = User.objects.get(username = user_slug)
        user_projects = Project.objects.filter(project_creator = user)
        user_projects_id = user_projects.values_list('id', flat = True)

        #Gets Profile Information

        user_profile = get_object_or_404(DesignProfile, user = user)
        context['user_profile'] = user_profile
        print user_profile.interest.all

        #Gets Projects Created by User and adds them to context dict
        user_published_projects = PublishedProject.objects.filter(project_link = user_projects_id).distinct('id')
        project_value_list = user_published_projects.values_list('project_link')

        context['projects'] = user_published_projects
        published_project_images = ProjectImage.objects.filter(project_image_for_project__in = project_value_list).distinct('project_image_for_project')
        context['published_project_images']=published_project_images

        tagged_projects = WorkingStepOrder.objects.filter(user = user_profile, in_work=False).distinct('project')

        #gets projects current user is working on
        in_work_steps = WorkingStepOrder.objects.filter(user = user_profile, in_work=True)
        in_work_projects_id = in_work_steps.distinct('project').values_list('project', flat=True)
        in_work_projects_published = PublishedProject.objects.filter(id__in = in_work_projects_id)
        in_work_projects = Project.objects.filter(id__in = in_work_projects_published.values_list('project_link',flat=True))
        in_work_step_order = in_work_steps.order_by('steporder__order')

        in_work_project_images_dict={}
        for piw in in_work_projects:
            for ppiw in in_work_projects_published:
                if ppiw.project_link == piw:
                    i = ProjectImage.objects.filter(project_image_for_project=piw).first()
                    in_work_project_images_dict[ppiw] = i.image.url
                    print 'IMAGE URL:, ',i.image.url
        context['in_work_project_images_dict'] = in_work_project_images_dict


        complete_project_dict={}
        for ppiw in in_work_projects_published:
            complete_step_count = 0
            total_step_count = 0
            for iws in in_work_steps:
                if iws.project == ppiw and iws.complete == True:
                    complete_step_count +=1
                    total_step_count += 1
                elif iws.project == ppiw and iws.complete == False:
                    total_step_count += 1
                else:
                    pass
            complete_project_dict[ppiw] = int(float(complete_step_count)/float(total_step_count)*100)
            print complete_project_dict[ppiw]




        context['in_work_projects'] = in_work_projects_published
        context['in_work_step_order'] = in_work_step_order
        context['project_percent_complete'] = complete_project_dict
        context['user_projects'] = user_projects

        return context


#View for the Designer to View their Own Profile
class MyProfileView(DesignProfileDetailView):
    template_name = 'designprofiles/my_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MyProfileView, self).get_context_data(*args, **kwargs)
        my_published_projects = context['projects']
        my_published_projects_id = my_published_projects.values_list('project_link_id', flat = True)

        project_drafts = context['user_projects'].exclude(id__in = my_published_projects_id)

        project_draft_images_dict = {}
        for pd in project_drafts:
            try:
                i = ProjectImage.objects.filter(project_image_for_project = pd).first()
                project_draft_images_dict[pd] = i.image.url
            except:
                project_draft_images_dict[pd]=None

        context['project_drafts'] = project_drafts
        context['project_draft_images_dict']= project_draft_images_dict



        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        for steporder in context['in_work_step_order']:
            step = steporder.steporder.step
            if 'complete_toggle_%s' % steporder.id in request.POST:
                complete_step_toggle(request, steporder)
                return HttpResponseRedirect(request.user)





def toggle_project_in_work(request, slug, project_id):
    user = get_object_or_404(DesignProfile, slug = slug)
    published_project = get_object_or_404(PublishedProject, project_slug_id = project_id)
    working_step_order = WorkingStepOrder.objects.filter(user = user, project = published_project) 
    
    for i in working_step_order:
        if i.in_work:
            i.in_work = False
            i.save()
        else:
            i.in_work=True
            i.save()
    return redirect('pub_detail', published_project.project_slug_id)

def toggle_step_complete(request, slug, project_id, step_id):
    print request.POST
    print 'ProjectID:', project_id
    print 'steporder_id', step_id
    user = get_object_or_404(DesignProfile, slug = slug)
    published_project = get_object_or_404(PublishedProject, project_slug_id = project_id)
    step_order = get_object_or_404(StepOrder, id = step_id)
    working_step_order = WorkingStepOrder.objects.get_or_create(user = user, project = published_project, steporder = step_order)[0]

    if working_step_order.complete:
        working_step_order.complete = False
    else:
        working_step_order.complete = True


    print '............'
    working_step_order.save()
    print 'IS THIS COMPLETE?', working_step_order.complete


    if request.is_ajax():
        return HttpResponse(working_step_order.complete)
    else:
        return redirect('pub_detail', published_project.project_slug_id)


