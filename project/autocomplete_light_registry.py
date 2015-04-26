import autocomplete_light

from .models import Project

autocomplete_light.register(Project,
	search_fields = ['^project_name',],
	)