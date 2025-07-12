from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Country, City, Wishlist
from django.db.models import Q

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

class CountryListView(ListView):
    model = Country
    template_name = 'discoveries/explore.html'
    context_object_name = 'countries'

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Country.objects.filter(Q(name__icontains=query))
        return Country.objects.all()

class CountryDetailView(DetailView):
    model = Country
    template_name = 'discoveries/country_detail.html'
    context_object_name = 'country'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.filter(country=self.object)
        return context


@require_POST
@login_required
def toggle_wishlist(request):
    content_type_id = request.POST.get('content_type_id')
    object_id = request.POST.get('object_id')
    content_type = ContentType.objects.get_for_id(content_type_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=object_id
    )

    if not created:
        wishlist_item.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})