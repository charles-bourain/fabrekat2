from django import forms
from project.models import Project, ProjectImage, Catagory
from projectsteps.models import PurchasedComponent, FabricatedComponent, ProjectFile, ProjectStep, StepOrder
from django.forms.models import inlineformset_factory
from django.forms import ImageField, CharField
import autocomplete_light
from projecttags.models import ProjectTag


#Use fields instead of exclude.


class TagForm(forms.ModelForm):
	class Meta:
		model = ProjectTag
		fields = ['tag']


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = [
			'project_name',
			'project_description',
		]

class ProjectDeleteForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = [
			'project_name',
			'project_description',
		]


class ProjectStepForm(forms.ModelForm):

	class Meta:
		model = ProjectStep
		fields = [
		 	'project_step_description',
		 	'project_step_image',
	 		]	


class ReOrderStepForm(forms.ModelForm):
	
	class Meta:
		model = ProjectStep
		fields = [
	 		]	

class PurchasedComponentForm(forms.ModelForm):

	class Meta:
		model = PurchasedComponent
		fields = ['purchased_component_name', 'purchased_component_url_link', 'purchased_component_quantity']

PurchasedComponentFormSet = inlineformset_factory(
	ProjectStep, 
	PurchasedComponent,   
	form = PurchasedComponentForm,
	fk_name = 'purchased_component_for_step',
	extra = 1, 
	can_delete = True,
	)



class FabricatedComponentForm(forms.ModelForm):

	class Meta:
		model = FabricatedComponent


FabricatedComponentFormSet = inlineformset_factory(
	ProjectStep, 
	FabricatedComponent,
	form = FabricatedComponentForm,
	fk_name = 'fabricated_component_for_step',
	fields = (
		'fabricated_component_from_project',
		'fabricated_component_quantity',
		),
	extra = 1, 
	can_delete = True,
	 )

class ProjectImageForm(forms.ModelForm):

	class Meta:
		model = ProjectImage
		fields = ('image',)
		required = True

# ProjectImageFormSet = inlineformset_factory(Project, ProjectImage, form = ProjectImageForm, fields = ('image',), extra = 1, )

class ProjectFileForm(forms.ModelForm):

	class Meta:
		model = ProjectFile
		fields = '__all__'
		exclude = ['project_file_for_step']
		required = False

ProjectFileFormSet = inlineformset_factory(ProjectStep, ProjectFile, form = ProjectFileForm, fields = ('project_file',), extra = 1, )

class CatagoryForm(forms.ModelForm):
	class Meta:
		model = Catagory
		fields = ('catagory',)
	
	CATAGORY_CHOICE_LIST = [
	    ('LifeStyle','LifeStyle'),
	    ('Outdoors','Outdoors'),
	    ('Transporation','Transportation'),
	    ('Technology','Technology'),
	]

	catagory = forms.ChoiceField(choices = CATAGORY_CHOICE_LIST)


CatagoryFormSet = inlineformset_factory(Project, Catagory, form = CatagoryForm, extra = 1)