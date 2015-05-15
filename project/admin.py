from django.contrib import admin
from project.models import Project, PurchasedComponent

#class FabricatedComponentInline (admin.TabularInline):
#	model = FabricatedComponent
	
class PurchasedComponentInline (admin.TabularInline):
	model = PurchasedComponent

class ProjectAdmin (admin.ModelAdmin):
	inlines = [
	# PurchasedComponentInline,
#	FabricatedComponentInline,
	]
# Register your models here. 
admin.site.register(Project, ProjectAdmin)
