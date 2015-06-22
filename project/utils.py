from .models import Project, ProjectStep
from publishedprojects.models import PublishedProject
import uuid


def get_project_id():
	project_id = str(uuid.uuid4())[:20].replace('-','').lower()
	
	try:
		id_exists = Project.objects.get(project_id = project_id)
		get_project_id()
	
	except:
		return project_id

#Checks if URL is published
def is_project_published(project_id):
	try:
		project = PublishedProject.objects.get(project_slug_id = project_id)
		return True

	except:
		return False


#This is for Step ordering.  This function assigns the newly created step to the next avialable step order
def get_order(project):
	order = 1
	while ProjectStep.objects.filter(step_for_project = project.id).filter(step_order = order):		
		order += 1
		print order
	return order

#function for moving the step order of the selected step with the previous step
def move_step_up(project, step):
	step_before_this_step = ProjectStep.objects.filter(step_for_project = project.id).get(step_order =(step.step_order-1))
	old_step = step.step_order
	new_step = step_before_this_step.step_order
	step.step_order = new_step
	step.save()
	step_before_this_step.step_order = old_step
	step_before_this_step.save()	

#function for moving the step order of the selected stpe with the next step
def move_step_down(project, step):
	step_after_this_step = ProjectStep.objects.filter(step_for_project = project.id).get(step_order =(step.step_order+1))
	print step_after_this_step
	old_step = step.step_order
	new_step = step_after_this_step.step_order
	step.step_order = new_step
	step.save()
	step_after_this_step.step_order = old_step
	step_after_this_step.save()


def is_user_project_creator(user, request):
	project_id = self.kwargs['project_id']
	project_creator = Project.objects.get(project_id = project_id).project_creator
	if user != project_creator:
		return False


def adjust_order_for_deleted_step(project, step):
	project_steps = ProjectStep.objects.filter(step_for_project = project.id)
	deleted_step = project_steps.get(step_order =(step.step_order))

	for step in project_steps:
		if step == deleted_step:
			pass
		elif step.step_order < deleted_step.step_order:
			pass
		else:
			step.step_order = step.step_order-1
			step.save()


