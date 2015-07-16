from project.models import Project
from projectsteps.models import ProjectStep

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


#function for moving the step order of the selected step with the previous step
def move_step_up(step_order_object, step):
	old_step = step_order_object.get(step = step.step)
	old_step_order = old_step.order
	new_step = step_order_object.get(order = old_step_order - 1)
	old_step.order = old_step_order-1
	old_step.save()
	new_step.order = old_step_order
	new_step.save()

#function for moving the step order of the selected stpe with the next step
def move_step_down(step_order_object, step):
	old_step = step_order_object.get(step = step.step)
	old_step_order = old_step.order
	new_step = step_order_object.get(order = old_step_order + 1)
	old_step.order = old_step_order+1
	old_step.save()
	new_step.order = old_step_order
	new_step.save()


def is_user_project_creator(user, request):
	project_id = self.kwargs['project_id']
	project_creator = Project.objects.get(project_id = project_id).project_creator
	if user != project_creator:
		return False


def adjust_order_for_deleted_step(project, step, step_list):
	deleted_step = step

	for step in step_list:
		if step.step == deleted_step:
			pass
		elif step.order < deleted_step.order:
			pass
		else:
			step.order = step.order-1	
			step.save()
	step.delete()