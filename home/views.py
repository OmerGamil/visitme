from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from discoveries.models import Country, City, Landmark, Rating, Wishlist

def home(request):
    countries = list(Country.objects.all())
    cities = list(City.objects.all())
    landmarks = list(Landmark.objects.all())

    countries.sort(key=lambda c: c.average_rating() or 0, reverse=True)
    cities.sort(key=lambda c: c.average_rating() or 0, reverse=True)
    landmarks.sort(key=lambda l: l.average_rating() or 0, reverse=True)

    top_countries = countries[:6]
    top_cities = cities[:6]
    top_landmarks = landmarks[:6]

    # Get user's wishlist and build a lookup map
    wishlist_map = {}
    user_wishlist = []

    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).select_related("content_type")
        for item in wishlist:
            wishlist_map[(item.content_type_id, item.object_id)] = True
            user_wishlist.append(item.content_object)

    # Inject `is_wishlisted` attribute into each object
    def mark_wishlist_status(objects):
        for obj in objects:
            ct_id = ContentType.objects.get_for_model(obj).id
            obj.is_wishlisted = (ct_id, obj.id) in wishlist_map

    mark_wishlist_status(top_countries)
    mark_wishlist_status(top_cities)
    mark_wishlist_status(top_landmarks)
    mark_wishlist_status(user_wishlist)

    return render(request, "home/index.html", {
        "top_countries": top_countries,
        "top_cities": top_cities,
        "top_landmarks": top_landmarks,
        "user_wishlist": user_wishlist,
    })

class HiddenGemsView(TemplateView):
    template_name = "home/hidden_gems.html"

class AboutView(TemplateView):
    template_name = "home/about.html"