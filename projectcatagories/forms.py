from django import forms
from .models import ProjectCatagory
from django.forms.models import inlineformset_factory
from django.forms import ImageField, CharField
import autocomplete_light


class ProjectCatagoryForm(forms.ModelForm):
	class Meta:
		model = ProjectCatagory
		fields = [
		'catagory',
		]