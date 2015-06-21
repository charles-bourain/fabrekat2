from django import forms
from .models import ProjectCatagory
from django.forms.models import inlineformset_factory
from django.forms import ImageField, CharField, ModelChoiceField, ModelForm
from project.models import Project
import autocomplete_light