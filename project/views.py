from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from project.models import Project, PurchasedComponent, ProjectImage, FabricatedComponent
from django.views.generic import CreateView, UpdateView
from project.forms import ProjectForm, PurchasedComponentForm, PurchasedComponentFormSet, FabricatedComponentFormSet
from project.forms import ProjectImageForm, ProjectImageFormSet
from account.mixins import LoginRequiredMixin
from follow import utils
from follow.models import Follow 

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
			return self.render_to_response(
				self.get_context_data(
				form = form,
				purchasedcomponent_formset = purchasedcomponent_formset,
				fabricatedcomponent_formset = fabricatedcomponent_formset,
				projectimage_formset = projectimage_formset,
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

		print 'is_Valid Check on Forms....'
		print 'Purchased Component:  %r , %r' % (purchasedcomponent_formset.is_valid(), purchasedcomponent_formset.errors)
		print 'Image:  %r , %r' % (projectimage_formset.is_valid(), projectimage_formset.errors)
		print 'Fabricated Comp: %r , %r' % (fabricatedcomponent_formset.is_valid(), fabricatedcomponent_formset.errors)	
		
		if (
			form.is_valid()
			and  purchasedcomponent_formset.is_valid()
			and  projectimage_formset.is_valid()
			and  fabricatedcomponent_formset.is_valid()
			):		

			return self.form_valid(form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset)
		else:
			return self.form_invalid(form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset)

	def form_valid(self, form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset):
		print 'All Forms Are Valid'
		self.object = form.save(commit = False)
		self.object.project_creator = self.request.user
		self.object = form.save()
		purchasedcomponent_formset.instance = self.object
		purchasedcomponent_formset.save()

		fabricatedcomponent_formset.instance = self.object
		fabricatedcomponent_formset.instance.fabricated_component_name = self.object.project_name
		fabricatedcomponent_formset.save()

		projectimage_formset.instance = self.object	
		projectimage_formset.save()


		return HttpResponseRedirect('/project/%d' % self.object.id)

	def form_invalid(self, form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset):
		print 'FORMS WERE INVALID'
		return self.render_to_response(
			self.get_context_data(
				form = form,
				purchasedcomponent_formset = purchasedcomponent_formset,
				fabricatedcomponent_formset = fabricatedcomponent_formset,
				projectimage_formset = projectimage_formset,
			)
		)

def project_detail(request, id):
	
	project = get_object_or_404(Project, id=id)

	#Might be showing the user who is viewing the page...
	user = request.user

	#purchase component gathers the database objects for the purchased component for project id.
	#The view may need to store the API for amazon store.
	#May want to pass fabricated components as well(for thumbnails etc)

	#Controlling what shoes on the detailed page.  The id passed the id associated to the project shown.
	purchasedcomponent = list(
		PurchasedComponent.objects.all().filter(
			purchased_component_for_project = id
			)
	)

	fabricatedcomponent =FabricatedComponent.objects.filter(
			fabricated_component_for_project = id)

	fabricatedcomponent_from_project_list_id = fabricatedcomponent.values_list('fabricated_component_from_project_id', flat = True)
		
	print 'FabricatedComponent_from_project_list = %r' % fabricatedcomponent_from_project_list_id

	fabricated_component_thumbnails = ProjectImage.objects.filter(project_image_for_project__in = fabricatedcomponent_from_project_list_id).first()

	print 'Thumbnailed Projects = %r' % fabricated_component_thumbnails


	#print 'Thumbnail Project Number: %r' % thumbnail_fabricatedcomponent
	#Choses the first applied image to be the thumbnail.  We may want a Javascript rotation later.
	#Gathering the Images in the Album

	projectimage  = list(
		ProjectImage.objects.filter(
			project_image_for_project = id
		)
	)


	context = {
		'project': project,
		'purchasedcomponent': purchasedcomponent,
		'fabricatedcomponent' : fabricatedcomponent,
		'projectimage':projectimage,
		'fabricated_component_thumbnails':fabricated_component_thumbnails,
	}

	return render_to_response(
		'project/detail.html',
		context,
		context_instance = RequestContext(request)
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


#Needs Work -- Is Broken
class ProjectEditView(LoginRequiredMixin, UpdateView):
	template_name = 'project/edit.html'
	model = Project
	form_class = ProjectForm
	

	def get(self, request, *args, **kwargs):
			self.object = None
			form_class = self.get_form_class()
			form = self.get_form(form_class)
			purchasedcomponent_formset = PurchasedComponentFormSet
			fabricatedcomponent_formset = FabricatedComponentFormSet
			projectimage_formset = ProjectImageFormSet
			return self.render_to_response(
				self.get_context_data(
				form = form,
				purchasedcomponent_formset = purchasedcomponent_formset,
				fabricatedcomponent_formset = fabricatedcomponent_formset,
				projectimage_formset = projectimage_formset,
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

		print 'is_Valid Check on Forms....'
		print 'Purchased Component:  %r , %r' % (purchasedcomponent_formset.is_valid(), purchasedcomponent_formset.errors)
		print 'Image:  %r , %r' % (projectimage_formset.is_valid(), projectimage_formset.errors)
		print 'Fabricated Comp: %r , %r' % (fabricatedcomponent_formset.is_valid(), fabricatedcomponent_formset.errors)	
		
		if (
			form.is_valid()
			and  purchasedcomponent_formset.is_valid()
			and  projectimage_formset.is_valid()
			and  fabricatedcomponent_formset.is_valid()
			):		

			return self.form_valid(form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset)
		else:
			return self.form_invalid(form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset)

	def form_valid(self, form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset):
		print 'All Forms Are Valid'
		self.object = form.save(commit = False)
		self.object.project_creator = self.request.user
		self.object = form.save()
		purchasedcomponent_formset.instance = self.object
		purchasedcomponent_formset.save()

		fabricatedcomponent_formset.instance = self.object
		fabricatedcomponent_formset.instance.fabricated_component_name = self.object.project_name
		fabricatedcomponent_formset.save()

		projectimage_formset.instance = self.object	
		projectimage_formset.save()


		return HttpResponseRedirect('/project/%d' % self.object.id)

	def form_invalid(self, form, purchasedcomponent_formset, projectimage_formset, fabricatedcomponent_formset):
		print 'FORMS WERE INVALID'
		return self.render_to_response(
			self.get_context_data(
				form = form,
				purchasedcomponent_formset = purchasedcomponent_formset,
				fabricatedcomponent_formset = fabricatedcomponent_formset,
				projectimage_formset = projectimage_formset,
			)
		)