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

# Create your views here.
#Currently Broken.  Added StepOrder Model which breaks a lot of this.

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
    if projectimage and projectstep:
        if form.is_valid():
            print 'Projec'
            published_project = form.save(commit = False)
            published_project.project_link = self
            published_project.project_slug_id = self.project_id


            published_project.save()
            return HttpResponseRedirect('/project/%s' % published_project.project_slug_id)
    else:
        return HttpResponseRedirect('/project/edit/%s' % project.project_id)
