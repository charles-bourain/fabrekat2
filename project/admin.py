from django.contrib import admin
from project.models import Project, PurchasedComponent, FabricatedComponent, ProjectStep

#class FabricatedComponentInline (admin.TabularInline):
#	model = FabricatedComponent
	
class PurchasedComponentInline (admin.TabularInline):
	model = PurchasedComponent

class FabricatedComponentInline(admin.TabularInline):
	model = FabricatedComponent
	fk_name = 'fabricated_component_for_project'

class ProjectStepInline(admin.TabularInline):
	model = ProjectStep
	

class ProjectAdmin (admin.ModelAdmin):
	inlines = [
	PurchasedComponentInline,
	FabricatedComponentInline,
	ProjectStepInline,
	]

# Register your models here. 
admin.site.register(Project, ProjectAdmin)
