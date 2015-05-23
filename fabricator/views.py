from django.shortcuts import render
import os
from fabricator.models import Fabricator
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from account.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from .forms import FabricatorForm
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
import pygeoip
from django.conf import settings

def get_city_from_ip(request):
	gi = pygeoip.GeoIP(os.path.join('GeoIP','GeoLiteCity.dat'))
	ip = '67.183.143.114'
	#ip = request.META.get('REMOTE_ADDR', None)
	metro_code = gi.record_by_addr(str(ip)).get('metro-code')
	return metro_code

def get_geoposition_from_ip(request):
	gi = pygeoip.GeoIP(os.path.join('GeoIP','GeoLiteCity.dat'))
	ip = '67.183.143.114'
	#ip = request.META.get('REMOTE_ADDR', None)
	latitude = gi.record_by_addr(str(ip)).get('latitude')
	logitude = gi.record_by_addr(str(ip)).get('longitude')

	return str(latitude)+','+str(logitude)


class FabricatorCreateView(LoginRequiredMixin, CreateView):
	template_name = 'fabricator/create.html'
	model = Fabricator
	success_url = 'fab_detail'
	form_class = FabricatorForm

	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = FabricatorForm(initial = {'fabricator_location':get_geoposition_from_ip(request)})
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
		self.object.fabricator_slug = self.object.fabricator
		self.object = form.save()

		return HttpResponseRedirect('fab_detail', name = self.object.fabricator)

	def form_invalid(self, form):
		print 'FORMS WERE INVALID'
		return self.render_to_response(
			self.get_context_data(
				form = form,
			)
		)


def fabricator_detail(request, name):
	
	fabricator = get_object_or_404(Fabricator, fabricator_slug=name)

	context = {
		'fabricator': fabricator,
	}

	return render_to_response(
		'fabricator/detail.html',
		context,
		context_instance = RequestContext(request),
	)



