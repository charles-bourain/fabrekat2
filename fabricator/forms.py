from django import forms
from project.models import Project, PurchasedComponent, ProjectImage, FabricatedComponent
from django.forms.models import inlineformset_factory
from django.forms import ImageField, CharField


class FabricatorForm(forms.ModelForm):
	
	class Meta:
		model = Project
		fields = [
			'fabricator_location',
			'fabricator_qualifications',
			'fabricator_tools',
			]