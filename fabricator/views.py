from django.shortcuts import render

from fabricator.models import Fabricator
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from account.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect


class FabricatorCreateView(LoginRequiredMixin, CreateView):
	template_name = 'fabricator/create.html'
	model = Fabricator
	success_url = 'fab_detail'

	def get(self, request, *args, **kwargs):
				self.object = None
				form_class = self.get_form_class()
				form = self.get_form(form_class)
				return self.render_to_response(
					self.get_context_data(
					form = form,
						)
					)
	def post(self, request, *args, **kwargs):
		print 'Post Initiated....'
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		print 'is_Valid Check on Forms....'
		if (
			form.is_valid()
			):		

			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		print 'All Forms Are Valid'
		
		self.object = form.save(commit = False)
		self.object.fabricator = self.request.user
		self.object = form.save()

		return HttpResponseRedirect('fab_detail', name = self.object.user)

	def form_invalid(self, form):
		print 'FORMS WERE INVALID'
		return self.render_to_response(
			self.get_context_data(
				form = form,
			)
		)


class FabricatorProfileView(DetailView):
	template_name = 'fabricator/detail.html'
	model = Fabricator

	def get_object(self):
		return self.request.user



