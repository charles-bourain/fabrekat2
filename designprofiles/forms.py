from django import forms
from django.forms.models import inlineformset_factory
from django.forms import ImageField, CharField

from .models import DesignProfile, WorkingStepOrder



class DesignProfileForm(forms.ModelForm):
    class Meta:
        model = DesignProfile
        fields = [
            'location',
            ]