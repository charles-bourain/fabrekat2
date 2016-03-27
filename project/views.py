from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from project.models import Project, ProjectImage, Catagory
from projectsteps.models import PurchasedComponent, FabricatedComponent, ProjectFile, ProjectStep, StepOrder
from django.views.generic import CreateView, UpdateView, TemplateView
from project.forms import ProjectForm, ProjectImageForm, ReOrderStepForm, TagForm, ProjectEditForm
from project.forms import ProjectStepDescriptionForm, ProjectStepVideoForm, ProjectStepImageForm
from project.forms import   PurchasedComponentFormSet, FabricatedComponentFormSet, ProjectFileFormSet
from project.forms import FormSetHelper, PurchasedComponentFormsetHelper, FabricatedComponentFormsetHelper
from .mixins import LoginRequiredMixin
from publishedprojects.models import PublishedProject
from publishedprojects.views import publish_project
from follow import utils
from follow.models import Follow
import uuid
from projectpricer.utils import get_product
from projecttags.models import ProjectTag
from projecttags.views import tag_assign, tag_remove
from .utils import get_project_id, is_project_published, move_step_up, move_step_down, is_user_project_creator, adjust_order_for_deleted_step, delete_project
from django import forms
from designprofiles.models import WorkingStepOrder


#Assigns Project id to a project.  This will be uniquie and show in URL.


#Assigns components and files to a step

#LoginRequiredMixin checks if user is logged in
#This creates the first of the Project.  This is a fresh create


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'project/create.html'
    model = Project
    form_class = ProjectForm

    #Gets the forms.
    def get(self, request, *args, **kwargs):
            self.object = None
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            form.helper.form_action = reverse('prj_create')
            return self.render_to_response(
                self.get_context_data(
                form = form,
                )
            )

    #Begins the posting proccess.  Returns the valid/invalid forms.     
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)       
        if (form.is_valid()):       
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    #after valid check, saves the Project create form to the database
    def form_valid(self, form): 
        self.object = form.save(commit = False)
        self.object.project_creator = self.request.user
        self.object.project_id = get_project_id()
        self.object = form.save()

        return HttpResponseRedirect('/project/edit/%s' % self.object.project_id)


    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form = form,
            )
        )

class ProjectDetailView(TemplateView):
    template_name = 'project/published_project_view.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = get_object_or_404(Project, project_id = self.kwargs['project_id'])
        project_index = project.id
        creator_id = project.project_creator.id
        purchasedcomponent = []
        fabricatedcomponent = []
        projectfile = []        


        #Project Image List
        projectimage  = list(
            ProjectImage.objects.filter(
            project_image_for_project = project_index
            )
        )
        
        #Project Step Handling
        step_list = StepOrder.objects.filter(step_order_for_project = project).order_by('order')
        step_value_list = step_list.values_list('step', flat = True)
        if step_list: 

            purchasedcomponent =PurchasedComponent.objects.filter(
                    purchased_component_for_step__in = step_value_list,
                    )

            fabricatedcomponent =FabricatedComponent.objects.filter(
                    fabricated_component_for_step__in = step_value_list,
                    )
            fabricatedcomponent_from_project_list_id = fabricatedcomponent.values_list('fabricated_component_from_project_id', flat = True)
            fabricated_component_thumbnails = ProjectImage.objects.filter(project_image_for_project__in = fabricatedcomponent_from_project_list_id).first()

            projectfile  = list(
            ProjectFile.objects.filter(
                project_file_for_step__in = step_value_list,
                )
            )

        #Tag Handling
        tags = ProjectTag.objects.filter(tag_for_project = project_index)
        total_component_cost = 0
        for component in purchasedcomponent:
            total_component_cost += component.product.price
        try:
            catagories = Catagory.objects.get(project = project)
            context['catagory_list'] =catagories.catagory
            print type(context['catagory_list'])
            print context['catagory_list']
        except:
            context['catagory_list'] = ['No Catagories Assigned']

        context['project'] = project
        context['purchasedcomponent'] = purchasedcomponent
        context['fabricatedcomponent'] = fabricatedcomponent
        context['projectfile'] = projectfile
        context['projectstep'] = step_list
        context['projectimage'] = projectimage
        context['tags'] = tags
        context['total_component_cost']=total_component_cost

        return context


class StepView(TemplateView):
    template_name = 'project/project_templates/step.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        context = super(StepView, self).get_context_data(**kwargs)   
        project=get_object_or_404(Project, project_id=kwargs['project_id'])
        step_order = get_object_or_404(StepOrder, id = kwargs['step_id'], step_order_for_project=project)
        context['step'] = step_order
        context['purchasedcomponent'] =PurchasedComponent.objects.filter(purchased_component_for_step = step_order.step)
        context['fabricatedcomponent'] =FabricatedComponent.objects.filter(fabricated_component_for_step = step_order.step)
        context['projectfile']  = ProjectFile.objects.filter(project_file_for_step = step_order.step)     

        return context


class InWorkStepView(StepView):
    template_name = 'project/project_templates/step_in_work_step_wrapper.html'
    def get_context_data(self, *args,**kwargs):
        context = super(InWorkStepView, self).get_context_data(*args, **kwargs)
        project = get_object_or_404(PublishedProject, project_slug_id=kwargs['project_id'])
        working_step = WorkingStepOrder.objects.get(user = self.request.user, steporder=context['step'], project=project)
        context['single_step_load'] = True
        context['single_step_load_is_complete'] = working_step.complete
        context['published_project'] = project
        return context



class EditorStepView(StepView):
    template_name = 'project/editor_templates/editor_step_wrapper.html'


class PublishProjectDetailView(ProjectDetailView):
    template_name = 'project/published_project_view.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(PublishProjectDetailView, self).get_context_data(**kwargs)      
        unpub_project_index = context['project']
        project = PublishedProject.objects.get(project_link = unpub_project_index)
        saved_project_count = len(Follow.objects.get_follows(project))
        working_step_order = False
        try:
            working_step_order = WorkingStepOrder.objects.filter(project = project, user = self.request.user)
        except:
            pass


        if working_step_order and working_step_order[0].in_work:
            context['project_in_work_by_user'] = True
            context['working_step_order'] = working_step_order
            is_step_complete_dict={}
            for wso in working_step_order:
                is_step_complete_dict[wso.steporder] = wso.complete
            context['is_step_complete_dict'] = is_step_complete_dict
        else:
            context['project_in_work_by_user'] = False

        context['saved_project_count'] = saved_project_count
        context['published_project'] = project
        return context


#View for Editing a Step for a project.
class StepEditView(LoginRequiredMixin, UpdateView):
    template_name = 'project/edit_step.html'
    model = ProjectStep

    def get_object(self,):
        try:
            obj = get_object_or_404(ProjectStep, id = self.request.GET.get('stepid'))
        except:
            obj = get_object_or_404(ProjectStep, id = self.kwargs['step_id'])
        return obj

    def get(self, request, *args, **kwargs):
        step_id = request.GET.get('stepid')
        user_id = request.user.id


        #project_id is what will show in the URL.  Unique to each project.
        # project_id = self.kwargs['project_id']
        edited_step = self.get_object()
        step_order = get_object_or_404(StepOrder, step = edited_step)
        project = step_order.step_order_for_project
        project_id = project.project_id
        # project index is what will track associated objects (Steps, Components, IMages etc..)
        project_index = project.id 
        creator_id = project.project_creator.id

        projectfile = ProjectFile.objects.filter(
            project_file_for_step = edited_step,
            )

        #Can Redo this as a decorator......
        if user_id != creator_id:
            return HttpResponseRedirect('/')
        elif is_project_published(project_id) == True:
            return HttpResponseRedirect('/')    
        else:
            self.object = self.get_object()
            description_form = ProjectStepDescriptionForm(instance = self.object)
            try:
                step_image_url = edited_step.project_step_image.url
            except:
                step_image_url = 0

            try:
                step_video_url = edited_step.project_step_video
            except:
                step_video_url = 0

            purchasedcomponent = PurchasedComponent.objects.filter(purchased_component_for_step = step_order.step) 
            purchasedcomponent_formset = PurchasedComponentFormSet(instance = self.object)
            fabricatedcomponent_formset = FabricatedComponentFormSet(instance = self.object)
            projectfile_formset = ProjectFileFormSet(instance = self.object)
            formset_helper = FormSetHelper
            purchased_component_formset_helper = PurchasedComponentFormsetHelper
            fabricated_component_formset_helper = FabricatedComponentFormsetHelper
            return self.render_to_response(
                self.get_context_data(
                projectfile = projectfile,    
                step = edited_step.id,
                step_order = step_order.order,
                step_image_url = step_image_url,
                step_video_url = step_video_url,
                project_id = project_id,
                description_form = description_form,
                purchasedcomponent = purchasedcomponent,
                purchasedcomponent_formset = purchasedcomponent_formset,
                fabricatedcomponent_formset = fabricatedcomponent_formset,
                projectfile_formset = projectfile_formset,
                formset_helper = formset_helper,
                purchasedcomponent_formset_helper =  purchased_component_formset_helper,
                fabricatedcomponent_formset_helper =  fabricated_component_formset_helper,
                )
            )

    def post(self, request, *args, **kwargs):
        print 'PROJECT EDIT POST'
        self.object = self.get_object()
        description_form = ProjectStepDescriptionForm(self.request.POST, instance=self.object)
        purchasedcomponent_formset = PurchasedComponentFormSet(self.request.POST, instance=self.object)  
        # fabricatedcomponent_formset = FabricatedComponentFormSet(self.request.POST, instance=self.object)
        projectfile_formset = ProjectFileFormSet(self.request.POST, self.request.FILES, instance=self.object)
        print description_form.is_valid(), purchasedcomponent_formset.is_valid(), projectfile_formset.is_valid()
        if (
            description_form.is_valid()
            and  purchasedcomponent_formset.is_valid()
            # and  fabricatedcomponent_formset.is_valid()
            and  projectfile_formset.is_valid()
            ):      
            return self.form_valid(description_form, purchasedcomponent_formset, projectfile_formset)
        else:
            return self.form_invalid(
                description_form, 
                purchasedcomponent_formset, 
                projectfile_formset,
                )


    def form_valid(self, description_form, purchasedcomponent_formset, projectfile_formset):
        print 'form valid'
        description_form.save()
        project_id = self.kwargs['project_id']
        project = Project.objects.get(project_id = project_id)
        purchaseform = purchasedcomponent_formset.save(commit = False)
        projectfileform = projectfile_formset.save(commit=False)
        for afile in projectfileform:
            afile.save()

        if purchaseform:
            product = get_product(   #ASSIGN ALL NEEDED VALUES
                self.request, 
                str(purchaseform[0].purchased_component_url_link), 
                str(purchaseform[0].purchased_component_name),
                )
            purchaseform[0].product = product
            purchaseform[0].save()
            
        self.object = self.get_object()
        
        self.object.step_for_project = project
        self.object = description_form.save()

        return HttpResponseRedirect('/project/edit/%s' % project_id)


    def form_invalid(self, form, purchasedcomponent_formset,  projectfile_formset):
        print 'FORM WAS INVALID'
        formset_helper = FormSetHelper
        purchased_component_formset_helper = PurchasedComponentFormsetHelper
        # fabricated_component_formset_helper = FabricatedComponentFormsetHelper

                
        return self.render_to_response(
            self.get_context_data(
                form = form,
                purchasedcomponent_formset = purchasedcomponent_formset,
                # fabricatedcomponent_formset = fabricatedcomponent_formset,
                projectfile_formset = projectfile_formset,
                formset_helper = formset_helper,
                purchasedcomponent_formset_helper =  purchased_component_formset_helper,
                # fabricatedcomponent_formset_helper =  fabricated_component_formset_helper,                
            )
        )

class StepMediaView(LoginRequiredMixin, UpdateView):
    template_name = 'project/media_upload_view.html'
    model=ProjectStep
    fields = ['project_step_video', 'project_step_image']

    def get_object(self, queryset=None):
        obj = get_object_or_404(ProjectStep, id = self.kwargs['step_id'])
        return obj

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        print self.object.id
        user_id = request.user.id
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, project_id = project_id)
        image_form = ProjectStepImageForm(instance = self.object)
        video_form = ProjectStepVideoForm(instance = self.object)
        if user_id != project.project_creator_id:
            return HttpResponseRedirect('/')
        elif is_project_published(project_id) == True:
            return HttpResponseRedirect('/')    
        else:
            self.object = None
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            return self.render_to_response(
                self.get_context_data(
                project_id = project_id,
                step_id = self.kwargs['step_id'],
                image_form = image_form,
                video_form = video_form,
                )
            )        
    def post(self, request, *args, **kwargs):
        print 'MEDIA VIEW IS POSTING'
        print request.POST
        print 'REQUEST FILES: ',request.FILES
        self.object = self.get_object()
        image_form = ProjectStepImageForm(request.POST, request.FILES, instance = self.object)
        video_form = ProjectStepVideoForm(request.POST, instance = self.object)         
        if (image_form.is_valid() and video_form.is_valid()):       

            return self.form_valid(image_form,video_form)
        else:
            return self.form_invalid(video_form,video_form)


            #Item Assigning Project to the FK does not seem to be working.
    def form_valid(self, image_form, video_form):
        print 'FORM WAS VALID'
        image_form.save()
        video_form.save()
        print image_form
        print video_form        

        project_id = self.kwargs['project_id']

        if self.request.is_ajax():
            return HttpResponse('success')
        else:
            return HttpResponseRedirect('/project/edit/%s' % project_id)


    def form_invalid(self, image_form, video_form):
        return self.render_to_response(
            self.get_context_data(
                form = form,
            )
        )     



#Allows upload and assigns an image to a Project via the project_index
class ImageCreateView(LoginRequiredMixin, CreateView):
    template_name = 'project/addimage.html'
    model = ProjectImage
    form_class = ProjectImageForm

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, project_id = project_id)
        #Can Redo this as a decorator......
        if user_id != project.project_creator_id:
            return HttpResponseRedirect('/')
        elif is_project_published(project_id) == True:
            return HttpResponseRedirect('/')    
        else:
            self.object = None
            form_class = self.get_form_class()
            print "FORM CLASS ==",form_class
            print self.get_form(form_class)
            form = self.get_form(form_class)
            return self.render_to_response(
                self.get_context_data(
                project_id = project_id,
                form = form,
                )
            )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        if (form.is_valid()):       

            return self.form_valid(form,)
        else:
            return self.form_invalid(form,)


            #Item Assigning Project to the FK does not seem to be working.
    def form_valid(self, form):
        project_id = self.kwargs['project_id']
        self.object = form.save(commit = False)
        project = Project.objects.get(project_id = project_id)
        self.object.project_image_for_project = project
        self.object = form.save()

        return HttpResponseRedirect('/project/edit/%s' % project_id)


    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form = form,
            )
        )       

#Edit project view is the main view for any unpublished projects.  Shows everything assigned to the project and POST buttons for edits.



class EditProjectView(UpdateView, LoginRequiredMixin, ProjectDetailView):
    template_name = 'project/edit_view.html'
    model=Project
    form_class=ProjectEditForm

    def get_object(self, queryset=None):
        obj = Project.objects.get(project_id=self.kwargs['project_id'])
        return obj

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context=super(EditProjectView,self).get_context_data(**kwargs)  
        self.object=self.get_object()
        context['form']=ProjectEditForm(instance=self.object)
        context['tag_form']=TagForm(instance=self.object)
        context['formset_helper'] = FormSetHelper

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        step_list = context['projectstep']
        self.object = self.get_object()
        project = self.object 
        if '_save' in request.POST:
            print "_save....."
            print request.POST
            form = ProjectEditForm(request.POST, instance = self.object)
            if form.is_valid():
                self.form_valid(form)
                return HttpResponseRedirect('/project/edit/%s' % project.project_id)
            else:
                self.form_invalid(form)
        elif '_addtag' in request.POST:
            tag_assign(self.object,TagForm(request.POST))
            return HttpResponseRedirect('/project/edit/%s' % project.project_id)
                            
            
        elif '_publish' in request.POST:
            publish_project(project, request)
            return HttpResponseRedirect('/project/%s' % project.project_id)   
            
        elif '_delete_project' in request.POST:
            delete_project(
                context['project'], 
                context['projectstep'], 
                context['tags'], 
                context['purchasedcomponent'], 
                context['fabricatedcomponent'], 
                context['projectimage'], 
                context['projectfile'],
                )  
            return HttpResponseRedirect('/')  
            
        elif '_addimage' in request.POST:
            return HttpResponseRedirect('/project/edit/%s/addimage/' % project.project_id)  
            # elif '_reorder_steps' in request.POST:
            #   return HttpResponseRedirect('/project/edit/%s/ordersteps/' % project.project_id)   


        for tag in context['tags']:
            if ('_remove_tag_%s' % tag.id) in request.POST:
                tag_remove(project,tag)    
        for step in step_list:
            if ('_deletestep_%s'% step.id) in request.POST:
                adjust_order_for_deleted_step(step, step_list)
                return HttpResponseRedirect('/project/edit/%s' % project.project_id)

            if ('_move_%s_step_up'% step.id) in request.POST:
                if step.order == 1:
                    return HttpResponseRedirect('/project/edit/%s' % project.project_id)
                else:
                    move_step_up(step_list, step)
                    return HttpResponseRedirect('/project/edit/%s' % project.project_id)
            if ('_move_%s_step_down'% step.id) in request.POST:
                if step.order == (len(step_list)):
                    return HttpResponseRedirect('/project/edit/%s' % project.project_id)
                else:
                    move_step_down(step_list, step)
                    return HttpResponseRedirect('/project/edit/%s' % project.project_id)   
        try:      
            if form.is_valid(): 
                print 'ALL FORMS ARE VALID'      
                return self.form_valid(form)
            else:
                print 'FORMS WERE INVALID'
                print "ERRORS:", form.errors
                return self.form_invalid(form)
        except:
            return HttpResponseRedirect('/project/edit/%s' % project.project_id)


    def form_valid(self, form):
        form.save()

        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )  

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )

def update_step_order(request, project_id):
    #Posts a Querydict from jQuery function that includes the new step order decided from user.  
    #the list index is the desired order, the values in the list is the old values.
    project = Project.objects.get(project_id = project_id)
    
    if request.method == "POST":
        try:
            new_order = request.POST.getlist('stepdata[]')
        except:
            pass
        step_order_objects = StepOrder.objects.filter(step_order_for_project = project).order_by('order')
        for steporder in step_order_objects:
            for no in new_order:
                if steporder.order == int(no):
                    steporder.order = new_order.index(no)+1
                    steporder.save()
                    break
    return HttpResponseRedirect(reverse('prj_edit', args=[project_id])) 

def delete_step(request, project_id, step_id):
    step=get_object_or_404(ProjectStep, id=step_id)
    step_order=get_object_or_404(StepOrder, step=step)
    project=get_object_or_404(Project, project_id=project_id)
    step_order_list = StepOrder.objects.filter(step_order_for_project = project).order_by('order')
    print step


    adjust_order_for_deleted_step(step_order, step_order_list)
    return HttpResponseRedirect('/project/edit/%s' % project.project_id)


def delete_component(request, project_id, step_id, component_id):
    print 'DELTING COMPONENT.....'
    component = get_object_or_404(PurchasedComponent, id=component_id)
    component.delete()
    print 'Is Ajax? ', request.is_ajax()
    if request.is_ajax():
        return HttpResponse('Success')

def delete_file(request, project_id, step_id, file_id):
    print 'DELTING steop file'
    deleted_file = get_object_or_404(ProjectFile, id=file_id)
    step = get_object_or_404(ProjectStep, id=step_id)
    deleted_file.delete()
    print 'Is Ajax? ', request.is_ajax()
    if request.is_ajax():
        return HttpResponse('Success') 
    else:
        HttpResponseRedirect('/project/edit/%s' % project.project_id)       




# @login_required
# def edit_step(request, id):
#     user_id = request.user.id
#     edited_step = get_object_or_404(ProjectStep, id=id)
#     project_id = request['project_id']
#     project = request[]

#     #Can Redo this as a decorator......
#     # if user_id != creator_id:
#     #   return HttpResponseRedirect('/')
#     # elif is_project_published(project_id) == True:
#     #   return HttpResponseRedirect('/')    
#     # else:
#     form = ProjectStepForm(instance = edited_step)
#     fabricatedcomponent_form = FabricatedComponentFormSet(instance = edited_step)
#     purchasedcomponent_form = PurchasedComponentFormSet(instance = edited_step)
#     projectfile_form = ProjectFileFormSet(instance = edited_step)
#     step_order = get_object_or_404(StepOrder, step_order_for_project = )

#     class StepOrder(models.Model):
#    step_order_for_project = models.ForeignKey(Project, null = True, blank = True)
#    step = models.ForeignKey(ProjectStep)
#    order = models.PositiveIntegerField(default = 0)

#    def __unicode__(self):
#     return unicode('Project Order for: ' + self.step_order_for_project.project_name)

#     if request.POST:
#         if '_save' in request.POST:
#             form = ProjectStepForm(request.POST,request.FILES,instance = edited_step)
#             fabricatedcomponent_form = FabricatedComponentFormSet(request.POST, instance = edited_step)
#             purchasedcomponent_form = PurchasedComponentFormSet(request.POST,request.FILES, instance = edited_step)
#             projectfile_form = ProjectFileFormSet(request.POST, request.FILES, instance = edited_step)
#             if form.is_valid() and fabricatedcomponent_form.is_valid() and purchasedcomponent_form.is_valid() and projectfile_form.is_valid():          
#                 form.save()
#                 fabricatedcomponent_form.save()
#                 purchasedcomponent_form.save()
#                 projectfile_form.save()
#                 return HttpResponseRedirect('/project/edit/%s' % edited_step.step_for_project.project_id)                   


#     context = {
#         'form' : form,
#         'fabricatedcomponent_form':fabricatedcomponent_form,
#         'purchasedcomponent_form':purchasedcomponent_form,
#         'projectfile_form':projectfile_form,
#     }       


#     return render_to_response(
#         'project/editstep.html',
#         context,
#         context_instance = RequestContext(request),
#         )

@login_required
def create_blank_step(request, project_id):
    project=get_object_or_404(Project, project_id = project_id)
    step_count = len(StepOrder.objects.filter(step_order_for_project=project))
    project_creator = project.project_creator
    requesting_user=request.user
    blank_step = ProjectStep.objects.create(project_step_description = ' ')
    print 'Blank Step has been created: ', blank_step
    blank_step.save()
    blank_step_order = StepOrder.objects.create(step_order_for_project = project, step=blank_step, order=(step_count+1))
    print 'Creating A Step for', project.project_name
    print 'Step Count for Project is Currently at: ', step_count
    print 'Saving the New Blank Step'
    blank_step_order.save()
    if project_creator==requesting_user:
        redirect('haystack_search')
    return HttpResponseRedirect('/project/edit/%s' % project_id)  


