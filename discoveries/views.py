from django.views.generic import ListView, DetailView
from .models import Country, City

class CountryListView(ListView):
    model = Country
    template_name = 'discoveries/explore.html'
    context_object_name = 'countries'

class CountryDetailView(DetailView):
    model = Country
    template_name = 'discoveries/country_detail.html'
    context_object_name = 'country'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.filter(country=self.object)
        return context