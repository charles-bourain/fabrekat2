from haystack import indexes
from .models import PublishedProject


class PublishedProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True, use_template = True)

    def get_model(self):
            return PublishedProject

    #def index_queryset(self, using = None):
    #       """Used When the entire index for model is updated."""
    #   return