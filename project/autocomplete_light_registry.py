import autocomplete_light

from projectcatagories.models import ProjectCatagory


class AutocompleteCatagory(autocomplete_light.AutocompleteModelBase):
	search_fields = ['catagory']
	

autocomplete_light.register(ProjectCatagory, AutocompleteCatagory)