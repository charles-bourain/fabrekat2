from django import forms
from project.models import Project, ProjectImage, Catagory
from projectsteps.models import PurchasedComponent, FabricatedComponent, ProjectFile, ProjectStep, StepOrder
from django.forms.models import inlineformset_factory
from django.forms import ImageField, CharField
from projecttags.models import ProjectTag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, Fieldset
from crispy_forms.bootstrap import InlineCheckboxes, PrependedText


#Use fields instead of exclude.


class TagForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(TagForm, self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		# form_id value is the 'id = blah blah' in the HTML.  Good for CSS/java id
		self.helper.form_method = 'post'
		self.helper.form_name = '_addtag'
		self.helper.layout = Layout(
			PrependedText('tag', '#', placeholder = 'Add a Tag to your Project'),
			Submit('_addtag','Submit'),
			)

	class Meta:
		model = ProjectTag
		fields = ['tag']

class ProjectForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProjectForm, self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		# form_id value is the 'id = blah blah' in the HTML.  Good for CSS/java id
		self.helper.form_method = 'post'
		self.helper.form_id = 'createPopup'
		self.helper.add_input(Submit('submit','Submit'))

	class Meta:
		model = Project
		fields = [
			'project_name',
		]

class ProjectEditForm(forms.ModelForm):
	project_catagory = forms.ModelMultipleChoiceField(queryset = Catagory.objects.all())

	def __init__(self, *args, **kwargs):
		super(ProjectEditForm, self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_name = '_save'
		self.helper.add_input(Submit('_save','Save Project'))



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

# ----- Forms Contained within Step Create View -----
class ProjectStepDescriptionForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProjectStepDescriptionForm, self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.helper.layout = Layout(
			'project_step_description',
			)		


	class Meta:
		model = ProjectStep
		fields = [
		 	'project_step_description',
	 		]


class ProjectStepImageForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProjectStepImageForm, self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
	


	class Meta:
		model = ProjectStep
		fields = [
		 	'project_step_image',
	 		]	

class ProjectStepVideoForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProjectStepVideoForm, self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.helper.layout = Layout(
			PrependedText('project_step_video', 'URL:', placeholder = 'https://www.youtube.com/'),
			)		


	class Meta:
		model = ProjectStep
		fields = [
		 	'project_step_video',
	 		]	 	 		 		

class PurchasedComponentForm(forms.ModelForm):

	class Meta:
		model = PurchasedComponent
		fields = ['purchased_component_url_link', 'purchased_component_quantity']


PurchasedComponentFormSet = inlineformset_factory(
	ProjectStep, 
	PurchasedComponent,   
	form = PurchasedComponentForm,
	fk_name = 'purchased_component_for_step',
	extra = 0, 
	can_delete = False,
	)	

class PurchasedComponentFormsetHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super(PurchasedComponentFormsetHelper, self).__init__(*args,**kwargs)
		self.form_tag = False
		self.template = 'project/step_edit_component_table.html'



class FabricatedComponentForm(forms.ModelForm):

	class Meta:
		model = FabricatedComponent
		fields = ['fabricated_component_from_project', 'fabricated_component_quantity']




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
	can_delete = False,
	 )

class FabricatedComponentFormsetHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super(FabricatedComponentFormsetHelper, self).__init__(*args,**kwargs)
		self.form_tag = False
		self.template = 'bootstrap/table_inline_formset.html'
		self.layout= Layout(
			)

class ProjectFileForm(forms.ModelForm):

	class Meta:
		model = ProjectFile
		exclude = ['project_file_for_step']
		required = False

ProjectFileFormSet = inlineformset_factory(
	ProjectStep, 
	ProjectFile, 
	form = ProjectFileForm, 
	fk_name = 'project_file_for_step',
	fields = ('project_file',), 
	can_delete=True, 
	extra=1, 
	)

# ----- End of Project Step Create Forms -----

class ReOrderStepForm(forms.ModelForm):
	
	class Meta:
		model = ProjectStep
		fields = [
	 		]	

class ProjectImageForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProjectImageForm, self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class = 'createPopup'
		self.helper.add_input(Submit('submit','Submit'))
		self.helper.form_tag = False

	class Meta:
		model = ProjectImage
		fields = ('image',)
		required = True


class CatagoryForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(CatagoryForm, self).__init__(*args,**kwargs)
		self.helper = FormHelper()
		# form_id value is the 'id = blah blah' in the HTML.  Good for CSS/java id
		self.helper.form_method = 'post'
		self.helper.layout = Layout(

			)

	class Meta:
		model = Catagory
		fields = ['catagory']




class FormSetHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super(FormSetHelper, self).__init__(*args,**kwargs)
		self.form_tag = False