from django import forms
from .models import Fabricator
from django.forms.models import inlineformset_factory
from django.forms import ImageField, CharField


class FabricatorForm(forms.ModelForm):
	
	class Meta:
		model = Fabricator
		fields = [
			'fabricator_qualifications',
			'fabricator_type',
			'fabricator_location',
			]

