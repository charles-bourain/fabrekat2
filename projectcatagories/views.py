from django.shortcuts import render
from .models import ProjectCatagory
from project.models import Project
import re

# Create your views here.

# def catagory_formatter(catagory_string):
# 	catagory_string = catagory_string.strip()
# 	catagory_filter = re.compile(r'^catagory_string$')
# 	alpha_filter = re.compile(r'[a-z0-9]*')
# 	if catagory_filter.search(catagory_string):

	
	# while ''.join(cat_str_list).isalpha() == False:
	# 	for item in cat_str_list:
	# 		if item.isalpha() == False:
	# 			cat_str_list.remove(item)

	

# def  catagory_assign(project, form):
# 	project_index = project.id
# 	print 'Project Index: '+ str(project_index)
# 	if form.is_valid():	
# 		formatted_cat_str = catagory_formatter(form.cleaned_data['catagory'])
# 		try:
# 			previous_cat_obj = ProjectCatagory.objects.get(catagory_word_index = formatted_cat_str)
# 			catagory = previous_cat_obj
			
# 		except:		
# 			catagory = ProjectCatagory()
# 			catagory.save()			
# 			catagory.catagory_word_index = "formatted_cat_str"
# 			catagory.catagory = form.cleaned_data['catagory']
		
# 		catagory.catagory_for_project.add(project_index)
# 		catagory.save()

# def catagory_remove(project, catagory):	
# 	project_index = project.id
# 	print 'Project Index: '+ str(project_index)				
# 	catagory.catagory_for_project.remove(project_index)
# 	catagory.save()


# def catagory_formatter(catagory_string):
# 	catagory_string = catagory_string.strip()
# 	catagory_filter = re.compile(r'^catagory_string$')
# 	if not catagory_filter.search(catagory_string):

def format_regex_for_robust_search(catagory_string):
	letter_list = list(catagory_string)
	print r"." + re.escape('.'.join(letter_list))
	return re.escape('.'+'.'.join(letter_list))




def find_previous_similiar_catagory(catagory_string):
	regex_for_robust_search = format_regex_for_robust_search(catagory_string)
	print 'Custom Regular Expression Search:', str(regex_for_robust_search)
	robust_catagory_filter = re.compile(regex_for_robust_search, re.IGNORECASE)
	catagory_list = ProjectCatagory.objects.all()
	for cat in catagory_list:
		filtered_cat = robust_catagory_filter.search(cat.catagory)
		print filtered_cat
		if filtered_cat:
			return filtered_cat
		else:
			continue

	# beginning_catagory_filter.findall(catagory_list)




			
def  catagory_assign(project, form):
	project_index = project.id
	if form.is_valid():	
		catagory_string = form.cleaned_data['catagory'].lstrip().rstrip().title()		
		try:
			catagory = ProjectCatagory.objects.get(catagory = catagory_string)		
		except:	
			similiar_catagory = find_previous_similiar_catagory(catagory_string)
			if not similiar_catagory:
				catagory = ProjectCatagory()
				catagory.save()				
				catagory.catagory = catagory_string
			else:
				catagory = similiar_catagory

		catagory.catagory_for_project.add(project_index)
		catagory.save()		


def catagory_remove(project, catagory):	
	project_index = project.id
	print 'Project Index: '+ str(project_index)				
	catagory.catagory_for_project.remove(project_index)
	catagory.save()
