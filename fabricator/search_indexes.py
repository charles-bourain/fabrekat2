from haystack import indexes
from fabricator.models import Fabricator


class FabricatorIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document = True, use_template = True)
	qualifications = indexes.CharField(model_attr ='fabricator_qualifications')
	creator = indexes.CharField(model_attr = 'fabricator')
	location = indexes.CharField(model_attr = 'fabricator_location')

	def get_model(self):
			return Fabricator

	#def index_queryset(self, using = None):
	#		"""Used When the entire index for model is updated."""
	#	return