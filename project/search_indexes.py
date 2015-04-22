from haystack import indexes
from project.models import Project


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document = True, use_template = True)
	description = indexes.CharField(model_attr ='project_description')
	creator = indexes.CharField(model_attr = 'project_creator')

	def get_model(self):
			return Project

	#def index_queryset(self, using = None):
	#		"""Used When the entire index for model is updated."""
	#	return