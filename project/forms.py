from django import forms
from project.models import Project, PurchasedComponent, ProjectImage, FabricatedComponent, ProjectFile, ProjectStep
from django.forms.models import inlineformset_factory
from django.forms import ImageField, CharField
import autocomplete_light


#Use fields instead of exclude.


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = [
			'project_name',
			'project_description',
			'project_catagory',
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
		 	'step_order',
	 		]		 		

# ProjectStepFormSet = inlineformset_factory(
# 	Project,
# 	ProjectStep, 
# 	 form = ProjectStepForm, 
# 	 fields = (
# 	 	'project_step_description',
# 	 	'project_step_image',
# 	 	), 
# 	 extra = 1,
# 	)

class PurchasedComponentForm(forms.ModelForm):

	class Meta:
		model = PurchasedComponent
		fields = '__all__'
		exclude = [
		'purchased_component_for_project',
		'purchased_component_for_step',
		]

PurchasedComponentFormSet = inlineformset_factory(
	ProjectStep, 
	PurchasedComponent,   
	form = PurchasedComponentForm,
	fk_name = 'purchased_component_for_step',
	extra = 1, 
	can_delete = True,
	)


class FabricatedComponentForm(autocomplete_light.ModelForm):
	class Meta:
		model = FabricatedComponent
		autocomplete_fields = ('fabricated_component_from_project',)
		autocomplete_exclude = (
			'fabricated_component_for_project',
			'fabricated_component_for_step',
			)

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

# class PurchasedComponentForm(forms.ModelForm):

# 	class Meta:
# 		model = PurchasedComponent
# 		fields = '__all__'
# 		exclude = ['purchased_component_for_project']

# class FabricatedComponentForm(autocomplete_light.ModelForm):
# 	class Meta:
# 		model = FabricatedComponent
# 		autocomplete_fields = ('fabricated_component_from_project',)
# 		autocomplete_exclude = ('fabricated_component_for_project',)

# class ProjectFileForm(forms.ModelForm):

# 	class Meta:
# 		model = ProjectFile
# 		fields = '__all__'
# 		exclude = ['project_file_for_project']
# 		required = False
# ProjectFileFormSet = inlineformset_factory(Project, ProjectFile, form = ProjectFileForm, fields = ('project_file',), extra = 1, )

# PurchasedComponentFormSet = inlineformset_factory(
# 	Project, 
# 	PurchasedComponent,   
# 	form = PurchasedComponentForm,
# 	fk_name = 'purchased_component_for_project',
# 	extra = 1, 
# 	can_delete = True,
# 	)
# FabricatedComponentFormSet = inlineformset_factory(
# 	Project, 
# 	FabricatedComponent,
# 	form = FabricatedComponentForm,
# 	fk_name = 'fabricated_component_for_project',
# 	fields = ('fabricated_component_from_project','fabricated_component_quantity'),
# 	extra = 1, 
# 	can_delete = True,
# 	 )
