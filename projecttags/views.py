from django.shortcuts import render
from .models import ProjectTag
from project.models import Project
import re

# Create your views here.

def format_regex_for_robust_search(tag_string):
	letter_list = list(tag_string)
	return ('\.*'+'\.*'.join(letter_list))




def find_previous_similiar_tag(tag_string):
	regex_for_robust_search = format_regex_for_robust_search(tag_string)
	print 'Custom Regular Expression Search:', str(regex_for_robust_search)
	robust_tag_filter = re.compile(regex_for_robust_search, re.IGNORECASE)
	tag_list = ProjectTag.objects.all()
	for tag in tag_list:
		filtered_tag = robust_tag_filter.match(tag.tag)
		if filtered_tag:
			print 'tag: ', tag
			return tag
		else:
			continue

	# beginning_tag_filter.findall(tag_list)




			
def  tag_assign(project, form):
	
	project_index = project.id
	if form.is_valid():	
		tag_string = form.cleaned_data['tag'].lstrip().rstrip().strip().lower()	
		tag_string = "".join(tag_string.split())	
		try:
			tag = ProjectTag.objects.get(tag_word_index = tag_string)		
		except:	
			similiar_tag = find_previous_similiar_tag(tag_string)
			if not similiar_tag:
				tag = ProjectTag()
				tag.save()		
				tag.tag_word_index = tag_string		
				tag.tag = form.cleaned_data['tag'].title().lstrip().rstrip()
			else:
				tag = similiar_tag

		tag.tag_for_project.add(project_index)
		tag.save()		


def tag_remove(project, tag):	
	project_index = project.id
	print 'Project Index: '+ str(project_index)				
	tag.tag_for_project.remove(project_index)
	tag.save()
