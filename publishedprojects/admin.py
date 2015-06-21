from django.contrib import admin
from .models import PublishedProject
from project.models import Project


class ProjectInline (admin.TabularInline):
	model = Project


class PublishedProjectAdmin (admin.ModelAdmin):
	inlines = [
	ProjectInline,
	]	

# Register your models here.
admin.site.register(PublishedProject, PublishedProjectAdmin)