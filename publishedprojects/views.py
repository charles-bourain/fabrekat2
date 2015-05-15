from django.shortcuts import render
from .models import PublishedProject
from .forms import PublishForm
from django.http import HttpResponseRedirect

# Create your views here.
def publish_project(self, request):
	form = PublishForm(request.POST)
	if form.is_valid():
		published_project = form.save(commit = False)
		published_project.project = self
		published_project.project_slug_id = self.project_id
		published_project.save()
