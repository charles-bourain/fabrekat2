from designprofiles.models import DesignProfile, WorkingStepOrder
from projectsteps.models import StepOrder, ProjectStep
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response


#Takes in requesting user, the project, 
def add_project_to_working_projects(user, project):
    designprofile = DesignProfile.objects.get_or_create(user = user, slug = user)[0]
    step_order = StepOrder.objects.filter(step_order_for_project = project.project_link)
    for so in step_order:
        working_step_order = WorkingStepOrder.objects.create(user = designprofile, project = project, steporder = so)


def remove_project_from_working_projects(user, project):
    designprofile = DesignProfile.objects.get(user = user, slug = user)
    working_step_order = WorkingStepOrder.objects.filter(user = designprofile, project = project)

    for step in working_step_order:
        step.delete()
    pass


@login_required
def complete_step_toggle(request, steporder):

    if request.user.id == steporder.user.id:
        if steporder.complete:
            steporder.complete = False
            steporder.save()
        else:
            steporder.complete = True
            steporder.save()


  