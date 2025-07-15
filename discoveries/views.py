from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Country, City, Landmark, Wishlist, Rating, Comment

# ---------- DRY Mixin ----------

class DetailContextMixin:
    model = None
    object_type = None
    related_model = None  # e.g. City for Country → Cities

    def get_related_queryset(self, obj):
        """Return middle list items (e.g. cities or landmarks)"""
        if self.related_model is None:
            return None
        if self.object_type == "country":
            return self.related_model.objects.filter(country=obj)
        if self.object_type == "city":
            return self.related_model.objects.filter(city=obj)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        content_type = ContentType.objects.get_for_model(obj)

        # Required for base_detail.html
        context["object"] = obj
        context["object_type"] = self.object_type

        # Search query for middle list
        query = self.request.GET.get("q")
        related_qs = self.get_related_queryset(obj)
        if related_qs is not None:
            if query:
                related_qs = related_qs.filter(Q(name__icontains=query))
            context["middle_list"] = related_qs

        # Wishlist
        if self.request.user.is_authenticated:
            wishlist_ids = Wishlist.objects.filter(
                user=self.request.user
            ).values_list("object_id", flat=True)
            context["wishlist_ids"] = list(wishlist_ids)

            # Rating
            user_rating = Rating.objects.filter(
                user=self.request.user,
                content_type=content_type,
                object_id=obj.id
            ).first()
            context["user_rating"] = user_rating.stars / 2 if user_rating else 0

            # Comment
            user_comment = Comment.objects.filter(
                user=self.request.user,
                content_type=content_type,
                object_id=obj.id
            ).first()
            context["user_comment"] = user_comment

            # Other reviews
            context["reviews"] = Comment.objects.filter(
                content_type=content_type,
                object_id=obj.id
            ).exclude(user=self.request.user).select_related("user").order_by("-created_at")
        else:
            context["wishlist_ids"] = []
            context["user_rating"] = 0
            context["user_comment"] = None
            context["reviews"] = Comment.objects.filter(
                content_type=content_type,
                object_id=obj.id
            ).select_related("user").order_by("-created_at")

        # Ratings for all users
        ratings = Rating.objects.filter(
            content_type=content_type,
            object_id=obj.id
        )
        context["ratings_by_user"] = {r.user_id: r.stars / 2 for r in ratings}

        return context


# ---------- VIEWS ----------

class CountryListView(ListView):
    model = Country
    template_name = 'discoveries/explore.html'
    context_object_name = 'countries'

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Country.objects.filter(name__icontains=query)
        return Country.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            country_type = ContentType.objects.get_for_model(Country)
            wishlist_ids = Wishlist.objects.filter(
                user=self.request.user,
                content_type=country_type
            ).values_list('object_id', flat=True)
            context['wishlist_ids'] = list(wishlist_ids)
        else:
            context['wishlist_ids'] = []
        return context


class CountryDetailView(DetailContextMixin, DetailView):
    model = Country
    template_name = "discoveries/country_detail.html"
    context_object_name = "country"
    object_type = "country"
    related_model = City


class CityDetailView(DetailContextMixin, DetailView):
    model = City
    template_name = "discoveries/city_detail.html"
    context_object_name = "city"
    object_type = "city"
    related_model = Landmark


class LandmarkDetailView(DetailContextMixin, DetailView):
    model = Landmark
    template_name = "discoveries/landmark_detail.html"
    context_object_name = "landmark"
    object_type = "landmark"
    related_model = None


# ---------- AJAX Views ----------

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


@require_POST
@login_required
def rate_object(request):
    try:
        stars = float(request.POST.get("stars"))
        if stars < 1 or stars > 5:
            raise ValueError
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'error': 'Invalid rating'}, status=400)

    object_id = request.POST.get("object_id")
    content_type_id = request.POST.get("content_type_id")
    content_type = get_object_or_404(ContentType, id=content_type_id)

    # Remove existing
    Rating.objects.filter(user=request.user, content_type=content_type, object_id=object_id).delete()

    # Create new
    Rating.objects.create(
        user=request.user,
        stars=int(stars * 2),
        content_type=content_type,
        object_id=object_id
    )

    ratings = Rating.objects.filter(content_type=content_type, object_id=object_id)
    average = sum(r.stars for r in ratings) / (2 * len(ratings))

    return JsonResponse({'success': True, 'average_rating': round(average, 1)})


@require_POST
@login_required
def submit_comment(request):
    comment_text = request.POST.get("text")
    object_id = request.POST.get("object_id")
    content_type_id = request.POST.get("content_type_id")

    if not (comment_text and object_id and content_type_id):
        return JsonResponse({"success": False, "error": "Missing fields"})

    try:
        content_type = ContentType.objects.get_for_id(content_type_id)
    except ContentType.DoesNotExist:
        return JsonResponse({"success": False, "error": "Invalid content type"})

    latest_rating = Rating.objects.filter(
        user=request.user,
        content_type=content_type,
        object_id=object_id
    ).order_by("-created_at").first()

    comment, created = Comment.objects.update_or_create(
        user=request.user,
        content_type=content_type,
        object_id=object_id,
        defaults={"text": comment_text, "rating": latest_rating}
    )

    return JsonResponse({
        "success": True,
        "created": created,
        "text": comment.text,
        "timestamp": comment.created_at.strftime("%b %d, %Y %H:%M")
    })
