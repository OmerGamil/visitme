from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from discoveries.models import Country, City, Landmark, Wishlist


def home(request):
    # --- Top items (sorted by average rating; your existing approach kept) ---
    countries = list(Country.objects.all())
    cities = list(City.objects.all())
    landmarks = list(Landmark.objects.all())

    countries.sort(key=lambda c: (c.average_rating() or 0), reverse=True)
    cities.sort(key=lambda c: (c.average_rating() or 0), reverse=True)
    landmarks.sort(key=lambda l: (l.average_rating() or 0), reverse=True)

    top_countries = countries[:6]
    top_cities = cities[:6]
    top_landmarks = landmarks[:6]

    # --- Build a fast lookup for the current user's wishlist ---
    wishlist_map = {}
    user_wishlist_objects = []

    if request.user.is_authenticated:
        # Only the fields we need; select content_type for fewer queries
        wishlist_qs = (
            Wishlist.objects
            .filter(user=request.user)
            .select_related("content_type")
            .only("content_type_id", "object_id")  # avoids loading unnecessary fields
        )
        for item in wishlist_qs:
            # Skip broken rows defensively
            if not item.content_type_id or not item.object_id:
                continue

            wishlist_map[(item.content_type_id, item.object_id)] = True

            # item.content_object can be None if the target row was deleted.
            obj = getattr(item, "content_object", None)
            if obj is not None:
                user_wishlist_objects.append(obj)

    # --- Helper: mark objects with .is_wishlisted without crashing on None ---
    def mark_wishlist_status(objects):
        for obj in objects:
            if obj is None:
                # Be defensive; don't ever call get_for_model(None)
                continue
            # Use for_concrete_model=False to keep proxy/abstract relations predictable
            ct_id = ContentType.objects.get_for_model(obj, for_concrete_model=False).id
            obj.is_wishlisted = (ct_id, obj.id) in wishlist_map

    # Only try to mark when there’s a logged-in user with a wishlist
    if wishlist_map:
        mark_wishlist_status(top_countries)
        mark_wishlist_status(top_cities)
        mark_wishlist_status(top_landmarks)
        mark_wishlist_status(user_wishlist_objects)

    return render(
        request,
        "home/index.html",
        {
            "top_countries": top_countries,
            "top_cities": top_cities,
            "top_landmarks": top_landmarks,
            "user_wishlist": user_wishlist_objects,  # safe, no None entries
        },
    )


class HiddenGemsView(TemplateView):
    template_name = "home/hidden_gems.html"


class AboutView(TemplateView):
    template_name = "home/about.html"
