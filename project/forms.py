from django import forms
from project.models import Project, PurchasedComponent, ProjectImage, FabricatedComponent,ProjectFile
from django.forms.models import inlineformset_factory
from django.forms import ImageField, CharField


class ProjectForm(forms.ModelForm):
	
	class Meta:
		model = Project
		fields = '__all__'
		exclude = [ 
		'project_spotlight',
		]

class PurchasedComponentForm(forms.ModelForm):

	class Meta:
		model = PurchasedComponent
		fields = '__all__'
		exclude = ['purchased_component_for_project']

class FabricatedComponentForm(forms.ModelForm):
	fabricated_component_from_project = forms.ModelChoiceField(queryset = Project.objects.all(), to_field_name = 'project_name')
	print 'THis is working'
	class Meta:
		model = FabricatedComponent
		fields = '__all__'
		exclude = ['fabricated_component_for_project']	


class ProjectImageForm(forms.ModelForm):

	class Meta:
		model = ProjectImage
		fields = '__all__'
		exclude = ['project_image_for_project']
		required = True

class ProjectFileForm(forms.ModelForm):

	class Meta:
		model = ProjectFile
		fields = '__all__'
		exclude = ['project_file_for_project']
		required = False



PurchasedComponentFormSet = inlineformset_factory(
	Project, 
	PurchasedComponent,   
	form = PurchasedComponentForm,
	fk_name = 'purchased_component_for_project',
	extra = 1, 
	can_delete = True,
	)
FabricatedComponentFormSet = inlineformset_factory(
	Project, 
	FabricatedComponent,
	form = FabricatedComponentForm,
	fk_name = 'fabricated_component_for_project',
	fields = ('fabricated_component_from_project','fabricated_component_quantity'),
	extra = 1, 
	can_delete = True,
	 )

ProjectImageFormSet = inlineformset_factory(Project, ProjectImage, form = ProjectImageForm, fields = ('image',), extra = 1, )
ProjectFileFormSet = inlineformset_factory(Project, ProjectFile, form = ProjectFileForm, fields = ('project_file',), extra = 1, )