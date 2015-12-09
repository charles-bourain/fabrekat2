from django.contrib import admin
from .models import ProjectStep, StepOrder, ProjectFile


class StepFileInline(admin.TabularInline):
    model = ProjectFile



class StepAdmin (admin.ModelAdmin):
    inlines = [
    StepFileInline,
    ]

admin.site.register(ProjectStep, StepAdmin)
admin.site.register(StepOrder)

# Register your models here.
