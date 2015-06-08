from django import forms
from .models import ProjectCatagory
from django.forms.models import inlineformset_factory
from django.forms import ImageField, CharField
from project.models import Project
import autocomplete_light


class CatagoryForm(forms.ModelForm):
	class Meta:
		model = ProjectCatagory
		fields = ('catagory',)


# CatagoryFormSet = inlineformset_factory(
# 	Project,	
# 	ProjectCatagory,
# 	form = CatagoryForm,
# 	extra = 1
# 	)