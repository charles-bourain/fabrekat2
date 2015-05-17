from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import user_is_project_creator_permission
from django.core.urlresolvers import reverse
from project.models import Project, PurchasedComponent, ProjectImage, FabricatedComponent, ProjectFile, ProjectStep
from django.views.generic import CreateView, UpdateView
from project.forms import ProjectForm, ProjectImageForm, ProjectStepForm, ReOrderStepForm
from project.forms import   PurchasedComponentFormSet, FabricatedComponentFormSet, ProjectFileFormSet
from account.mixins import LoginRequiredMixin
from publishedprojects.models import PublishedProject
from publishedprojects.views import publish_project
from follow import utils
from follow.models import Follow
import uuid



def get_project_id():
	project_id = str(uuid.uuid4())[:20].replace('-','').lower()
	
	try:
		id_exists = Project.objects.get(project_id = project_id)
		get_project_id()
	
	except:
		return project_id

def is_project_published(project_id):
	try:
		project = PublishedProject.objects.get(project_slug_id = project_id)
		return True

	except:
		return False




def is_user_project_creator(user, request):
	project_id = self.kwargs['project_id']
	project_creator = Project.objects.get(project_id = project_id).project_creator
	if user != project_creator:
		return False



#Assigns components and files to a step

#LoginRequiredMixin checks if user is logged in
class ProjectCreateView(LoginRequiredMixin, CreateView):
	template_name = 'project/create.html'
	model = Project
	form_class = ProjectForm

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

class StepCreateView(LoginRequiredMixin, CreateView):
	template_name = 'project/addstep.html'
	model = ProjectStep
	form_class = ProjectStepForm

	def get(self, request, *args, **kwargs):
		user_id = request.user.id
		project_id = self.kwargs['project_id']
		project = get_object_or_404(Project, project_id = project_id)
		project_index = project.id 
		creator_id = project.project_creator.id

		#Can Redo this as a decorator......
		if user_id != creator_id:
			return HttpResponseRedirect('/')
		elif is_project_published(project_id) == True:
			return HttpResponseRedirect('/')	
		else:
			self.object = None
			form_class = self.get_form_class()
			form = self.get_form(form_class)
			purchasedcomponent_formset = PurchasedComponentFormSet
			fabricatedcomponent_formset = FabricatedComponentFormSet
			projectfile_formset = ProjectFileFormSet
			return self.render_to_response(
				self.get_context_data(
				form = form,
				purchasedcomponent_formset = purchasedcomponent_formset,
				fabricatedcomponent_formset = fabricatedcomponent_formset,
				projectfile_formset = projectfile_formset,
				)
			)
	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		purchasedcomponent_formset = PurchasedComponentFormSet(self.request.POST,)	
		fabricatedcomponent_formset = FabricatedComponentFormSet(self.request.POST,)
		projectfile_formset = ProjectFileFormSet(self.request.POST, self.request.FILES,)
		
		if (
			form.is_valid()
			and  purchasedcomponent_formset.is_valid()
			and  fabricatedcomponent_formset.is_valid()
			and  projectfile_formset.is_valid()
			):		

			return self.form_valid(form, purchasedcomponent_formset, fabricatedcomponent_formset, projectfile_formset)
		else:
			return self.form_invalid(form, purchasedcomponent_formset, fabricatedcomponent_formset, projectfile_formset)


			#Item Assigning Project to the FK does not seem to be working.
	def form_valid(self, form, purchasedcomponent_formset, fabricatedcomponent_formset, projectfile_formset):
		self.object = form.save(commit = False)
		project_id = self.kwargs['project_id']
		project = Project.objects.get(project_id = project_id)
		self.object.step_for_project = project	
		if len(ProjectStep.objects.filter(step_for_project = project.id)) > 0:
			step_count_for_order = len(ProjectStep.objects.filter(step_for_project = project.id))
		else:
			step_count_for_order = 0
		self.object.step_order = step_count_for_order
		self.object = form.save()

		purchasedcomponent_formset.instance = self.object
		purchasedcomponent_formset.purchased_component_for_project = project
		purchasedcomponent_formset.save()

		fabricatedcomponent_formset.instance = self.object
		fabricatedcomponent_formset.fabricated_component_for_project = project
		fabricatedcomponent_formset.instance.fabricated_component_name = self.object.step_for_project.project_name
		fabricatedcomponent_formset.save()

		projectfile_formset.instance = self.object
		projectfile_formset.project_file_for_project_id = project.id
		projectfile_formset.save()


		return HttpResponseRedirect('/project/edit/%s' % project_id)


	def form_invalid(self, form, purchasedcomponent_formset, fabricatedcomponent_formset, projectfile_formset):
		return self.render_to_response(
			self.get_context_data(
				form = form,
				purchasedcomponent_formset = purchasedcomponent_formset,
				fabricatedcomponent_formset = fabricatedcomponent_formset,
				projectfile_formset = projectfile_formset,
			)
		)


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


@login_required
def unpublished_project_detail(request, project_id):
	user_id = request.user.id
	project = get_object_or_404(Project, project_id = project_id)
	project_index = project.id 
	creator_id = project.project_creator.id

	#Can Redo this as a decorator......
	if user_id != creator_id:
		return HttpResponseRedirect('/')
	elif is_project_published(project_id) == True:
		return HttpResponseRedirect('/')	
	else:
		# saved_project_count = len(Follow.objects.get_follows(project))
		projectimage  = list(
		ProjectImage.objects.filter(
			project_image_for_project = project_index
			)
		)
		#Might be showing the user who is viewing the page...

		projectstep  = list(
			ProjectStep.objects.filter(
				step_for_project = project_index,
			),
		)	
		#purchase component gathers the database objects for the purchased component for project id.
		#The view may need to store the API for amazon store.
		#May want to pass fabricated components as well(for thumbnails etc)

		#Controlling what shoes on the detailed page.  The id passed the id associated to the project shown.
		
		purchasedcomponent =PurchasedComponent.objects.filter(
				purchased_component_for_step__in = projectstep
				)

		fabricatedcomponent =FabricatedComponent.objects.filter(
				fabricated_component_for_step__in = projectstep
				)
		fabricatedcomponent_from_project_list_id = fabricatedcomponent.values_list('fabricated_component_from_project_id', flat = True)
		fabricated_component_thumbnails = ProjectImage.objects.filter(project_image_for_project__in = fabricatedcomponent_from_project_list_id).first()

		projectfile  = list(
		ProjectFile.objects.filter(
			project_file_for_step__in = projectstep
			)
		)

		#User Checking - If Creating User, Allow Publish and Create.  Passes a True Value to Template of user_is_creator if user is creator
		if request.user == project.project_creator:
			if request.POST:
				if '_edit' in request.POST:
					return HttpResponseRedirect('/project/edit/%s' % project.project_id)
				elif '_publish' in request.POST:
					publish_project(project, request)
					return HttpResponseRedirect('/project/%s' % project.project_id)
		else:
			HttpResponseRedirect('/')			
		context = {
			'project': project,
			'purchasedcomponent': purchasedcomponent,
			'fabricatedcomponent' : fabricatedcomponent,
			'projectimage':projectimage,
			'projectfile':projectfile,
			'fabricated_component_thumbnails':fabricated_component_thumbnails,
			'projectstep': projectstep,
		}

		return render_to_response(
			'project/unpub_detail.html',
			context,
			context_instance = RequestContext(request),
		)

def published_project_detail(request, project_id):
	
	project = get_object_or_404(Project, project_id=project_id)
	project_index = project.id
	purchasedcomponent = []
	fabricatedcomponent = []
	projectfile = []
	fabricated_component_thumbnails = []

	saved_project_count = len(Follow.objects.get_follows(project))
	projectimage  = list(
	ProjectImage.objects.filter(
		project_image_for_project = project_index
		)
	)
	#Might be showing the user who is viewing the page...
	user = request.user
	projectstep  = list(
		ProjectStep.objects.filter(
			step_for_project = project_index,
		),
	)	
	#purchase component gathers the database objects for the purchased component for project id.
	#The view may need to store the API for amazon store.
	#May want to pass fabricated components as well(for thumbnails etc)

	#Controlling what shoes on the detailed page.  The id passed the id associated to the project shown.
	
	step_list = []
	for step in projectstep:
		step_list.append(step.id)
	print step_list

	purchasedcomponent =PurchasedComponent.objects.filter(
			purchased_component_for_step__in = step_list,
			)

	fabricatedcomponent =FabricatedComponent.objects.filter(
			fabricated_component_for_step__in = step_list,
			)
	fabricatedcomponent_from_project_list_id = fabricatedcomponent.values_list('fabricated_component_from_project_id', flat = True)
	fabricated_component_thumbnails = ProjectImage.objects.filter(project_image_for_project__in = fabricatedcomponent_from_project_list_id).first()

	projectfile  = list(
	ProjectFile.objects.filter(
		project_file_for_step__in = step_list,
		)
	)

	#User Checking - If Creating User, Allow Publish and Create.  Passes a True Value to Template of user_is_creator if user is creator
	user_is_creator = False
	if request.user == project.project_creator:
		user_is_creator = True
		if request.POST:
			if '_revise' in request.POST:
				#CREATE VIEW WITH INTIAL VALUES AS VALUES ALREADY IN THIS PROJECT
				return HttpResponseRedirect('/project/create')
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
		'projectstep': projectstep,
		'user_is_creator': user_is_creator,
	}

	return render_to_response(
		'project/pub_detail.html',
		context,
		context_instance = RequestContext(request),
	)

@login_required
def my_saved_projects(request):

	my_saved_projects_id = Follow.objects.get_follows(Project).values('target_project_id')

	my_saved_projects =  Project.objects.filter(id__in = my_saved_projects_id)


	context = {
    'my_saved_projects': my_saved_projects,
    }

	return render_to_response(
        'project/saved_projects.html',
        context,
        context_instance = RequestContext(request),        
        )




@login_required
def my_projects(request):

	user = request.user
	user_projects =  Project.objects.filter(project_creator = user)
	my_published_projects = PublishedProject.objects.filter(id__in = user_projects)
	my_published_projects_id = my_published_projects.values_list('project_id', flat = True)
	my_unpublished_projects =  user_projects.exclude(id__in = my_published_projects_id)
	# my_unpublished_projects = Project.objects.filter(project_id__in = user_projects).exclude(project_id__in = my_published_projects)


	context = {
    'my_unpublished_projects': my_unpublished_projects,
    'my_published_projects': my_published_projects,
    }

	return render_to_response(
        'project/my_projects.html',
        context,
        context_instance = RequestContext(request),        
        )


@login_required
def edit_project(request, project_id):
	user_id = request.user.id
	project = get_object_or_404(Project, project_id = project_id)
	project_index = project.id 
	creator_id = project.project_creator.id
	purchasedcomponent = []
	fabricatedcomponent = []
	projectfile = []

	#Can Redo this as a decorator......
	if user_id != creator_id:
		return HttpResponseRedirect('/')
	elif is_project_published(project_id) == True:
		return HttpResponseRedirect('/')	
	else:
		form = ProjectForm(instance = project)

		projectimage  = list(
			ProjectImage.objects.filter(
			project_image_for_project = project_index
			)
		)

		projectstep  =ProjectStep.objects.filter(
			step_for_project = project_index,
			).order_by('step_order')
		

		step_list = []
		for step in projectstep:
			step_list.append(step.id)
		print step_list

		purchasedcomponent =PurchasedComponent.objects.filter(
				purchased_component_for_step__in = step_list,
				)

		fabricatedcomponent =FabricatedComponent.objects.filter(
				fabricated_component_for_step__in = step_list,
				)
		fabricatedcomponent_from_project_list_id = fabricatedcomponent.values_list('fabricated_component_from_project_id', flat = True)
		fabricated_component_thumbnails = ProjectImage.objects.filter(project_image_for_project__in = fabricatedcomponent_from_project_list_id).first()

		projectfile  = list(
		ProjectFile.objects.filter(
			project_file_for_step__in = step_list,
			)
		)

		if request.POST:
			if '_addstep' in request.POST:
				return HttpResponseRedirect('/project/edit/%s/addstep/' % project.project_id)
			elif '_publish' in request.POST:
				publish_project(project, request)
				return HttpResponseRedirect('/project/unpublished/%s' % project.project_id)
			elif '_save' in request.POST:
				form = ProjectForm(request.POST, instance = project)
				form.save()
			elif '_delete' in request.POST:
				return HttpResponseRedirect('/project/unpublished/%s' % project.project_id)	
			elif '_addimage' in request.POST:
				return HttpResponseRedirect('/project/edit/%s/addimage/' % project.project_id)	
			elif '_reorder_steps' in request.POST:
				return HttpResponseRedirect('/project/edit/%s/ordersteps/' % project.project_id)				
			# for step in projectstep:
			# 	edit_step_tag = '_editstep_%s' % step.id
			# 	edit_step_redirect = HttpResposeRedirect('/project/edit/%s/editstep/%s ' % project, step.id)
			# elif edit_step_tag in request.POST:
			# 	return edit_step_redirect





		context = {
			'form' : form,
			'purchasedcomponent':purchasedcomponent,
			'fabricatedcomponent':fabricatedcomponent,				
			'projectfile': projectfile,
			'projectstep':projectstep,
			'projectimage':projectimage,
		}	


		return render_to_response(
			'project/edit.html',
			context,
			context_instance = RequestContext(request),
			)



@login_required
def edit_step(request, id):
	user_id = request.user.id
	edited_step = get_object_or_404(ProjectStep, id=id)

	#Can Redo this as a decorator......
	# if user_id != creator_id:
	# 	return HttpResponseRedirect('/')
	# elif is_project_published(project_id) == True:
	# 	return HttpResponseRedirect('/')	
	# else:
	form = ProjectStepForm(instance = edited_step)
	fabricatedcomponent_form = FabricatedComponentFormSet(instance = edited_step)
	purchasedcomponent_form = PurchasedComponentFormSet(instance = edited_step)
	projectfile_form = ProjectFileFormSet(instance = edited_step)

	if request.POST:
		if '_save' in request.POST:
			form = ProjectStepForm(request.POST,request.FILES,instance = edited_step)
			fabricatedcomponent_form = FabricatedComponentFormSet(request.POST, instance = edited_step)
			purchasedcomponent_form = PurchasedComponentFormSet(request.POST,request.FILES, instance = edited_step)
			projectfile_form = ProjectFileFormSet(request.POST, request.FILES, instance = edited_step)
			if form.is_valid() and fabricatedcomponent_form.is_valid() and purchasedcomponent_form.is_valid() and projectfile_form.is_valid():			
				print'FORM IS VALID'
				form.save()
				fabricatedcomponent_form.save()
				purchasedcomponent_form.save()
				projectfile_form.save()
				return HttpResponseRedirect('/project/edit/%s' % edited_step.step_for_project.project_id)					
			else:
				print'FORM IS NOT VALID'


	context = {
		'form' : form,
		'fabricatedcomponent_form':fabricatedcomponent_form,
		'purchasedcomponent_form':purchasedcomponent_form,
		'projectfile_form':projectfile_form,
	}	


	return render_to_response(
		'project/editstep.html',
		context,
		context_instance = RequestContext(request),
		)


@login_required
def reorder_steps(request, project_id):
	user_id = request.user.id
	edited_project = get_object_or_404(Project, project_id=project_id)
	project_index = edited_project.id 
	steps_for_reorder = ProjectStep.objects.filter(
			step_for_project = project_index,
			).order_by('step_order')	



	form = ReOrderStepForm(instance = edited_project)

	projectstep  =ProjectStep.objects.filter(
		step_for_project = project_index,
		).order_by('step_order')	

	if request.POST:
		if '_save' in request.POST:
			form = ReOrderForm(request.POST,request.FILES,instance = edited_step)
			if form.is_valid():			
				print'FORM IS VALID'
				form.save()
				return HttpResponseRedirect('/project/edit/%s' % edited_step.step_for_project.project_id)					
			else:
				print'FORM IS NOT VALID'


	context = {
		'form' : form,
		'projectstep': projectstep,
	}	


	return render_to_response(
		'project/ordersteps.html',
		context,
		context_instance = RequestContext(request),
		)	