from django.shortcuts import render
from .models import ProjectCatagory
from project.models import Project

# Create your views here.

def catagory_formatter(catagory_string):
	cat_str_list = list(catagory_string)
	
	while ''.join(cat_str_list).isalpha() == False:
		for item in cat_str_list:
			if item.isalpha() == False:
				cat_str_list.remove(item)

	return ''.join(cat_str_list).upper()


# def  catagory_assign(project, form):
# 	if form.is_valid():	
# 		formatted_cat_str = catagory_formatter(form.cleaned_data['catagory'])
# 		try:
# 			previous_cat_obj = ProjectCatagory.objects.get(catagory_word_index = formatted_cat_str)
# 			project.project_catagory = previous_cat_obj
# 			project.save()
# 		except:		
# 			form.save(commit = False)
# 			# print "Printing Catagory Pre-Save Index Value: " + str(form.cleaned_data['catagory_word_index'])
# 			form.instance.catagory_word_index = formatted_cat_str
# 			form.save()

# 		# print 'PRINT FORM CATAGORY WORD INDEX: ' + str(form.catagory_word_index)	
# 		project.project_catagory = ProjectCatagory.objects.get(catagory_word_index = formatted_cat_str)
# 		project.save()

def  catagory_assign(project, form):
	project_index = project.id
	print 'Project Index: '+ str(project_index)
	if form.is_valid():	
		formatted_cat_str = catagory_formatter(form.cleaned_data['catagory'])
		try:
			previous_cat_obj = ProjectCatagory.objects.get(catagory_word_index = formatted_cat_str)
			catagory = previous_cat_obj
			
		except:		
			catagory = ProjectCatagory()
			catagory.save()
			catagory.catagory_word_index = formatted_cat_str
			catagory.catagory = form.cleaned_data['catagory']
		
		catagory.catagory_for_project.add(project_index)
		catagory.save()

def catagory_remove(project, catagory):
	project_index = project.id
	print 'Project Index: '+ str(project_index)				
	catagory.catagory_for_project.remove(project_index)
	catagory.save()
			


#Catagory Database Builder:
	# Reduce catagories to a non-space, ALL CAP, this will be an indentifier column
	# There is a unicode column for what it is actually called
	# example - unicode column = 'Costume Making', reduced column = 'COSTUMEMAKING'
	# all inputed catagories are broken down into the reduced column and compared
	# May want to do a scrub of names, in this case 'Costume Making' could also be named 'Costume Tailoring'.
	# The scrub could happen daily on the serverside only.  The scrub could be automated.
	# For catagories that have a certain amount of projects in them, they can be then compared to catagories with a large amount of projects and the wording compared.
	# autocomplete light can be used to prevent mutliple types

