from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from project.models import Project, PurchasedComponent, ProjectImage, FabricatedComponent, ProjectFile, ProjectStep
from django.views.generic import CreateView, UpdateView
from project.forms import ProjectForm, ProjectImageForm, ProjectStepForm, ReOrderStepForm, CatagoryForm
from project.forms import   PurchasedComponentFormSet, FabricatedComponentFormSet, ProjectFileFormSet
from account.mixins import LoginRequiredMixin
from publishedprojects.models import PublishedProject
from publishedprojects.views import publish_project
from follow import utils
from follow.models import Follow
import uuid
from projectpricer.utils import get_product_info
from projectcatagories.models import ProjectCatagory
from projectcatagories.views import catagory_assign, catagory_remove
from .utils import get_project_id, is_project_published, get_order, move_step_up, move_step_down, is_user_project_creator
from django import forms
import autocomplete_light


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

#View for Creating a Step for a project.
class StepCreateView(LoginRequiredMixin, CreateView):
	template_name = 'project/addstep.html'
	model = ProjectStep
	form_class = ProjectStepForm

	def get(self, request, *args, **kwargs):
		user_id = request.user.id
		#project_id is what will show in the URL.  Unique to each project.
		project_id = self.kwargs['project_id']
		project = get_object_or_404(Project, project_id = project_id)
		#project index is what will track associated objects (Steps, Components, IMages etc..)
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


	def form_valid(self, form, purchasedcomponent_formset, fabricatedcomponent_formset, projectfile_formset):
		self.object = form.save(commit = False)
		project_id = self.kwargs['project_id']
		project = Project.objects.get(project_id = project_id)
		self.object.step_for_project = project	
		# if len(ProjectStep.objects.filter(step_for_project = project.id)) > 0:
		# 	step_count_for_order = len(ProjectStep.objects.filter(step_for_project = project.id))
		# else:
		# 	step_count_for_order = 0
		self.object.step_order = get_order(project)
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

#any projects saved by user using the follows app will appear in this view.
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



#List Projects created by user.  Splits between working projects and published projects
@login_required
def my_projects(request):

	user = request.user
	user_projects =  Project.objects.filter(project_creator = user)
	my_published_projects = PublishedProject.objects.filter(project_link__in = user_projects)
	my_published_projects_id = my_published_projects.values_list('project_link_id', flat = True)
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

#Edit project view is the main view for any unpublished projects.  Shows everything assigned to the project and POST buttons for edits.
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
		catagory_form = CatagoryForm

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

		purchasedcomponent =PurchasedComponent.objects.filter(
				purchased_component_for_step__in = step_list,
				)

		for component in purchasedcomponent:
			component.purchased_component_price = get_product_info(component)[0] #Returns [Price integer, Currency string,]

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

		catagories = ProjectCatagory.objects.filter(catagory_for_project = project_index)

		for cat in catagories:
			if ('_remove_catagory_%s'% cat.id) in request.POST:
				catagory_remove(project, cat)	
				return HttpResponseRedirect('/project/edit/%s' % project.project_id)		
		if request.POST:
			if '_addstep' in request.POST:
				return HttpResponseRedirect('/project/edit/%s/addstep/' % project.project_id)
			
			if '_addcatagory' in request.POST:
				print 'Checking Catagory:::::',CatagoryForm(request.POST)
				catagory_assign(project, CatagoryForm(request.POST))	
				return HttpResponseRedirect('/project/edit/%s' % project.project_id)					
			
			elif '_publish' in request.POST:
				publish_project(project, request)	
			
			elif '_save' in request.POST:
				form = ProjectForm(request.POST, instance = project)
			
			elif '_delete_project' in request.POST:
				return HttpResponseRedirect('/project/edit/%s/delete/' % project.project_id)	
			
			elif '_addimage' in request.POST:
				return HttpResponseRedirect('/project/edit/%s/addimage/' % project.project_id)	
			# elif '_reorder_steps' in request.POST:
			# 	return HttpResponseRedirect('/project/edit/%s/ordersteps/' % project.project_id)

		for step in projectstep:
			if ('_deletestep_%s'% step.id) in request.POST:
				return HttpResponseRedirect('deletestep/%s' % step.id)
			if ('_move_%s_step_up'% step.id) in request.POST:
				if step.step_order == 1:
					return HttpResponseRedirect('/project/edit/%s' % project.project_id)
				else:
					move_step_up(project, step)
					return HttpResponseRedirect('/project/edit/%s' % project.project_id)
			if ('_move_%s_step_down'% step.id) in request.POST:
				if step.step_order == (len(projectstep)):
					return HttpResponseRedirect('/project/edit/%s' % project.project_id)
				else:
					move_step_down(project, step)
					return HttpResponseRedirect('/project/edit/%s' % project.project_id)			



		context = {
			'form' : form,
			'purchasedcomponent':purchasedcomponent,
			'fabricatedcomponent':fabricatedcomponent,				
			'projectfile': projectfile,
			'projectstep':projectstep,
			'projectimage':projectimage,
			'catagory_form': catagory_form,
			'catagories':catagories,
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

#Need to check what is deleted using this.  Need to make sure its EVERYTHING.  This Delete is only for unpublished projects.
@login_required
def delete_project(request, project_id):
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

		projectimage  =	ProjectImage.objects.filter(
			project_image_for_project = project_index
			)

		projectstep  =ProjectStep.objects.filter(
			step_for_project = project_index,
			).order_by('step_order')
		step_list = []
		for step in projectstep:
			step_list.append(step.id)

		purchasedcomponent =PurchasedComponent.objects.filter(
				purchased_component_for_step__in = step_list,
				)


		fabricatedcomponent =FabricatedComponent.objects.filter(
				fabricated_component_for_step__in = step_list,
				)


		fabricatedcomponent_from_project_list_id = fabricatedcomponent.values_list('fabricated_component_from_project_id', flat = True)
		fabricated_component_thumbnails = ProjectImage.objects.filter(project_image_for_project__in = fabricatedcomponent_from_project_list_id).first()

		projectfile  =ProjectFile.objects.filter(
			project_file_for_step__in = step_list,
			)

		if request.POST:
			if '_delete_project_confirm' in request.POST:
				purchasedcomponent.delete()
				fabricatedcomponent.delete()
				projectfile.delete()
				projectimage.delete()
				projectstep.delete()
				project.delete()
				return HttpResponseRedirect('/')	
			elif '_backto_project' in request.POST:
				return HttpResponseRedirect('/project/edit/%s' % project.project_id)			



		context = {
			'project':project,
			'purchasedcomponent':purchasedcomponent,
			'fabricatedcomponent':fabricatedcomponent,				
			'projectfile': projectfile,
			'projectstep':projectstep,
			'projectimage':projectimage,
		}	


		return render_to_response(
			'project/delete.html',
			context,
			context_instance = RequestContext(request),
			)

#Deletes a step, and should delete all associated objects (other then the associated project)
@login_required
def delete_step(request, id):
	user_id = request.user.id
	delete_step = get_object_or_404(ProjectStep, id=id)
	associated_project = Project.objects.get(id = delete_step.step_for_project.id)
	if user_id != associated_project.project_creator_id:
		return HttpResponseRedirect('/')	
	else:
	
		purchasedcomponent =PurchasedComponent.objects.filter(
				purchased_component_for_step = delete_step,
				)


		fabricatedcomponent =FabricatedComponent.objects.filter(
				fabricated_component_for_step = delete_step,
				)
		
		projectfile  =ProjectFile.objects.filter(
			project_file_for_step = delete_step,
			)

		if request.POST:
			if '_delete_step_confirm' in request.POST:
				purchasedcomponent.delete()
				fabricatedcomponent.delete()
				projectfile.delete()
				delete_step.delete()
				return HttpResponseRedirect('/project/edit/%s' % associated_project.project_id)		
			elif '_backto_project' in request.POST:
				return HttpResponseRedirect('/project/edit/%s' % associated_project.project_id)	



		context = {
			'projectstep' : delete_step,
			'fabricatedcomponent':fabricatedcomponent,
			'purchasedcomponent':purchasedcomponent,
			'projectfile':projectfile,
		}	


		return render_to_response(
			'project/deletestep.html',
			context,
			context_instance = RequestContext(request),
			)