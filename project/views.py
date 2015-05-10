from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .decorators import user_is_project_creator_permission
from django.core.urlresolvers import reverse
from project.models import Project, PurchasedComponent, ProjectImage, FabricatedComponent, ProjectFile, ProjectStep
from django.views.generic import CreateView, UpdateView
from project.forms import ProjectForm, PurchasedComponentFormSet, FabricatedComponentFormSet, ProjectFileFormSet
from project.forms import ProjectImageForm, ProjectImageFormSet, ProjectStepFormSet
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

#Assigns components and files to a step
def assign_items_to_step(projectstep_formset, fabricatedcomponent_formset, purchasedcomponent_formset):
	
	for step in projectstep_formset:
		print "Step:" + str(step)



#LoginRequiredMixin checks if user is logged in
class ProjectCreateView(LoginRequiredMixin, CreateView):
	template_name = 'project/create.html'
	model = Project
	form_class = ProjectForm

	def get(self, request, *args, **kwargs):
			self.object = None
			form_class = self.get_form_class()
			form = self.get_form(form_class)
			purchasedcomponent_formset = PurchasedComponentFormSet
			fabricatedcomponent_formset = FabricatedComponentFormSet
			projectimage_formset = ProjectImageFormSet
			projectfile_formset = ProjectFileFormSet
			projectstep_formset = ProjectStepFormSet
			return self.render_to_response(
				self.get_context_data(
				form = form,
				purchasedcomponent_formset = purchasedcomponent_formset,
				fabricatedcomponent_formset = fabricatedcomponent_formset,
				projectimage_formset = projectimage_formset,
				projectfile_formset = projectfile_formset,
				projectstep_formset = projectstep_formset,
				)
			)
	def post(self, request, *args, **kwargs):
		print 'Post Initiated....'
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		purchasedcomponent_formset = PurchasedComponentFormSet(self.request.POST,)	
		fabricatedcomponent_formset = FabricatedComponentFormSet(self.request.POST,)
		projectimage_formset = ProjectImageFormSet(self.request.POST, self.request.FILES,)
		projectfile_formset = ProjectFileFormSet(self.request.POST, self.request.FILES,)
		projectstep_formset = ProjectStepFormSet(self.request.POST, self.request.FILES,) 
		
		if (
			form.is_valid()
			and  purchasedcomponent_formset.is_valid()
			and  projectimage_formset.is_valid()
			and  fabricatedcomponent_formset.is_valid()
			and  projectfile_formset.is_valid()
			and projectstep_formset.is_valid()
			):		

			return self.form_valid(form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset,projectfile_formset, projectstep_formset)
		else:
			return self.form_invalid(form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset,projectfile_formset, projectstep_formset)

	def form_valid(self, form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset, projectfile_formset, projectstep_formset):
		print 'All Forms Are Valid'
		self.object = form.save(commit = False)
		self.object.project_creator = self.request.user
		self.object.project_id = get_project_id()
		self.object = form.save()
		

		purchasedcomponent_formset.instance = self.object
		purchasedcomponent_formset.save()

		fabricatedcomponent_formset.instance = self.object
		fabricatedcomponent_formset.instance.fabricated_component_name = self.object.project_name
		fabricatedcomponent_formset.save()

		projectimage_formset.instance = self.object	
		projectimage_formset.save()

		projectfile_formset.instance = self.object	
		projectfile_formset.save()

		projectstep_formset.instance = self.object
		projectstep_formset.save()

		return HttpResponseRedirect('/project/unpublished/%s' % self.object.project_id)


	def form_invalid(self, form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset, projectfile_formset, projectstep_formset):
		print 'FORMS WERE INVALID'
		return self.render_to_response(
			self.get_context_data(
				form = form,
				purchasedcomponent_formset = purchasedcomponent_formset,
				fabricatedcomponent_formset = fabricatedcomponent_formset,
				projectimage_formset = projectimage_formset,
				projectfile_formset = projectfile_formset,
				projectstep_formset = projectstep_formset,
			)
		)




@login_required
def unpublished_project_detail(request, project_id):

	project = get_object_or_404(Project, project_id = project_id)
	project_index = project.id
	# saved_project_count = len(Follow.objects.get_follows(project))
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
	
	for step in projectstep:
		purchasedcomponent =PurchasedComponent.objects.filter(
				purchased_component_for_step = step.id
				)

		fabricatedcomponent =FabricatedComponent.objects.filter(
				fabricated_component_for_step = step.id
				)
		fabricatedcomponent_from_project_list_id = fabricatedcomponent.values_list('fabricated_component_from_project_id', flat = True)
		fabricated_component_thumbnails = ProjectImage.objects.filter(project_image_for_project__in = fabricatedcomponent_from_project_list_id).first()

		projectfile  = list(
		ProjectFile.objects.filter(
			project_file_for_step = step.id
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
		# 'saved_project_count': saved_project_count,
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
	
	for step in projectstep:
		purchasedcomponent =PurchasedComponent.objects.filter(
				purchased_component_for_step = step.id
				)

		fabricatedcomponent =FabricatedComponent.objects.filter(
				fabricated_component_for_step = step.id
				)
		fabricatedcomponent_from_project_list_id = fabricatedcomponent.values_list('fabricated_component_from_project_id', flat = True)
		fabricated_component_thumbnails = ProjectImage.objects.filter(project_image_for_project__in = fabricatedcomponent_from_project_list_id).first()

		projectfile  = list(
		ProjectFile.objects.filter(
			project_file_for_step = step.id
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
	my_unpublished_projects = Project.objects.filter(id__in = user_projects).exclude(id__in = my_published_projects)


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
	if user_id != creator_id:
		return HttpResponseRedirect('/' % project.id)
	else:
		form = ProjectForm(instance = project)
		purchasedcomponent_formset = PurchasedComponentFormSet(instance = project)
		fabricatedcomponent_formset = FabricatedComponentFormSet(instance = project)
		projectimage_formset = ProjectImageFormSet(instance = project)
		projectfile_formset = ProjectFileFormSet(instance = project)
		projectstep_formset = ProjectStepFormSet(instance = project)

		for component in purchasedcomponent_formset.forms:
			if component in purchasedcomponent_formset:
				purchasedcomponent_formset.initial = component
		
		for component in fabricatedcomponent_formset.forms:
			if component not in purchasedcomponent_formset:
				fabricatedcomponent_formset.initial = component

		print projectimage_formset.forms
		for image in projectimage_formset.forms:
			if image not in projectimage_formset:
				projectimage_formset.initial = image
		# Currently only getting the LAST item in each set

		# for item in projectstep_formset.forms:
		# 	if 'project_step_description' not in item.initial:
		# 		form.initial['project_step_description'] = projectstep_formset.forms.project_step_description

		context = {
			'form' : form,
			'purchasedcomponent_formset':purchasedcomponent_formset,
			'projectimage_formset':projectimage_formset,
			'projectfile_formset': projectfile_formset,
			'projectstep_formset':projectstep_formset,
		}		

		return render_to_response(
			'project/create.html',
			context,
			context_instance = RequestContext(request),
			)
	
	if request.POST:
		post(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		print 'Post Initiated....'
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		purchasedcomponent_formset = PurchasedComponentFormSet(self.request.POST,)	
		fabricatedcomponent_formset = FabricatedComponentFormSet(self.request.POST,)
		projectimage_formset = ProjectImageFormSet(self.request.POST, self.request.FILES,)
		projectfile_formset = ProjectFileFormSet(self.request.POST, self.request.FILES,)
		projectstep_formset = ProjectStepFormSet(self.request.POST, self.request.FILES,) 
		
		if (
			form.is_valid()
			and  purchasedcomponent_formset.is_valid()
			and  projectimage_formset.is_valid()
			and  fabricatedcomponent_formset.is_valid()
			and  projectfile_formset.is_valid()
			and projectstep_formset.is_valid()
			):		

			return self.form_valid(form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset,projectfile_formset, projectstep_formset)
		else:
			return self.form_invalid(form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset,projectfile_formset, projectstep_formset)

	def form_valid(self, form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset, projectfile_formset, projectstep_formset):
		print 'All Forms Are Valid'
		self.object = form.save(commit = False)
		self.object.project_creator = self.request.user
		self.object.project_id = get_project_id()
		self.object = form.save()
		

		purchasedcomponent_formset.instance = self.object
		purchasedcomponent_formset.save()

		fabricatedcomponent_formset.instance = self.object
		fabricatedcomponent_formset.instance.fabricated_component_name = self.object.project_name
		fabricatedcomponent_formset.save()

		projectimage_formset.instance = self.object	
		projectimage_formset.save()

		projectfile_formset.instance = self.object	
		projectfile_formset.save()

		projectstep_formset.instance = self.object
		projectstep_formset.save()

		return HttpResponseRedirect('/project/unpublished/%s' % self.object.project_id)


	def form_invalid(self, form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset, projectfile_formset, projectstep_formset):
		print 'FORMS WERE INVALID'
		return self.render_to_response(
			self.get_context_data(
				form = form,
				purchasedcomponent_formset = purchasedcomponent_formset,
				fabricatedcomponent_formset = fabricatedcomponent_formset,
				projectimage_formset = projectimage_formset,
				projectfile_formset = projectfile_formset,
				projectstep_formset = projectstep_formset,
			)
		)	