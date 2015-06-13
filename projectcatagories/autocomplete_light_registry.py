import autocomplete_light

from .models import ProjectCatagory


autocomplete_light.register(ProjectCatagory,
	search_fields = ['^project_catagory'],
	)