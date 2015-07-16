from django.shortcuts import render, redirect
from .models import PublishedProject
from .forms import PublishForm
from django.http import HttpResponseRedirect
from project.models import ProjectImage, Project
from projectsteps.models import ProjectStep, PurchasedComponent, FabricatedComponent, ProjectStep, ProjectFile, StepOrder
from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView
from project.mixins import LoginRequiredMixin
from follow import utils
from follow.models import Follow
import uuid
from publishedprojects.utils import verify_step_order

# Create your views here.
def publish_project(self, request):
    form = PublishForm(request.POST)
    project = self
    project_index = project.id

    projectimage  = list(
        ProjectImage.objects.filter(
        project_image_for_project = project_index
        )
    )

    projectstep  =StepOrder.objects.filter(
        step_order_for_project = project,
        ).order_by('order')

    step_list = projectstep.values_list('step', flat = True)
    
    purchasedcomponent =PurchasedComponent.objects.filter(
            purchased_component_for_step__in = step_list,
            )

#Need to add functionality to verify_step_order to ensure steps go from 1-len(ProjectSteps)
    if projectimage and projectstep and verify_step_order():
        if form.is_valid():
            published_project = form.save(commit = False)
            published_project.project_link = self
            published_project.project_slug_id = self.project_id


            published_project.save()
            return HttpResponseRedirect('/project/%s' % published_project.project_slug_id)
    else:
        print 'SHIT FAILED'
        return HttpResponseRedirect('/project/edit/%s' % project.project_id)

#published view.  This is what will be anyone accessing the sight.
def published_project_detail(request, project_id):
    
    project = get_object_or_404(Project, project_id=project_id)
    project_index = project.id
    purchasedcomponent = []
    fabricatedcomponent = []
    projectfile = []
    fabricated_component_thumbnails = []

    #Counts the amount of people who 'saved' this project using the Follow app
    saved_project_count = len(Follow.objects.get_follows(project))
    projectimage  = list(
    ProjectImage.objects.filter(
        project_image_for_project = project_index
        )
    )
    #Might be showing the user who is viewing the page...
    user = request.user
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

    #User Checking - If Creating User, Allow Publish and Create.  Passes a True Value to Template of user_is_creator if user is creator
    user_is_creator = False
    if request.user == project.project_creator:
        user_is_creator = True
        if request.POST:
            #Revise should ONLY be seen by the original create of the project.  Hitting Revise re-directs to a project edit page with all these values already in.
            #PUBLISHING the new revision should assign the project_id of the original project to this one, however preserve anything assigned to the old project_index.
            #This is done to preserve anyone using the Inspiration link to the project (inspiration uses project_index).
            if '_revise' in request.POST:
                #CREATE VIEW WITH INTIAL VALUES AS VALUES ALREADY IN THIS PROJECT
                return redirect('reviseproject', project_id = project_id)
    else:
        if request.POST:
            if '_inspire' in request.POST:
                #INPUT SELECTOR FOR TASK/COMPONENTS - INITIAL VALUES WILL BE SELECTED TASKS
                return HttpResponseRedirect('/project/create')
    context = {
        'project': project,
        'purchasedcomponent': purchasedcomponent,
        'fabricatedcomponent' : fabricatedcomponent,
        'projectimage':projectimage,
        'projectfile':projectfile,
        'fabricated_component_thumbnails':fabricated_component_thumbnails,
        'saved_project_count': saved_project_count,
        'projectstep': step_list,
        'user_is_creator': user_is_creator,
    }

    return render_to_response(
        'project/pub_detail.html',
        context,
        context_instance = RequestContext(request),
    )
