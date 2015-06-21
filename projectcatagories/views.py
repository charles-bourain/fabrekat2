from django.shortcuts import render
from .models import ProjectCatagory
from project.models import Project
import re

# Create your views here.

def format_regex_for_robust_search(catagory_string):
	letter_list = list(catagory_string)
	return ('\.*'+'\.*'.join(letter_list))




def find_previous_similiar_catagory(catagory_string):
	regex_for_robust_search = format_regex_for_robust_search(catagory_string)
	print 'Custom Regular Expression Search:', str(regex_for_robust_search)
	robust_catagory_filter = re.compile(regex_for_robust_search, re.IGNORECASE)
	catagory_list = ProjectCatagory.objects.all()
	for cat in catagory_list:
		filtered_cat = robust_catagory_filter.match(cat.catagory)
		if filtered_cat:
			print 'Catagory: ', cat
			return cat
		else:
			continue

	# beginning_catagory_filter.findall(catagory_list)




			
def  catagory_assign(project, form):
	
	project_index = project.id
	if form.is_valid():	
		catagory_string = form.cleaned_data['catagory'].lstrip().rstrip().strip().lower()	
		catagory_string = "".join(catagory_string.split())	
		try:
			catagory = ProjectCatagory.objects.get(catagory_word_index = catagory_string)		
		except:	
			similiar_catagory = find_previous_similiar_catagory(catagory_string)
			if not similiar_catagory:
				catagory = ProjectCatagory()
				catagory.save()		
				catagory.catagory_word_index = catagory_string		
				catagory.catagory = form.cleaned_data['catagory'].title().lstrip().rstrip()
			else:
				catagory = similiar_catagory

		catagory.catagory_for_project.add(project_index)
		catagory.save()		


def catagory_remove(project, catagory):	
	project_index = project.id
	print 'Project Index: '+ str(project_index)				
	catagory.catagory_for_project.remove(project_index)
	catagory.save()
