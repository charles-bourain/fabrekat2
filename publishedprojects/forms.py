from django import forms
from .models import PublishedProject

class PublishForm(forms.ModelForm):
	
    class Meta:
        model = PublishedProject
        exclude = ['project_slug_id','project_link']


