from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Country, City, Wishlist, Rating, Comment
from django.db.models import Q

from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
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

class CountryDetailView(DetailView):
    model = Country
    template_name = 'discoveries/country_detail.html'
    context_object_name = 'country'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country = self.object
        content_type = ContentType.objects.get_for_model(Country)

        # City Search
        query = self.request.GET.get("q")
        cities_qs = City.objects.filter(country=country)
        if query:
            cities_qs = cities_qs.filter(Q(name__icontains=query))
        context['cities'] = cities_qs

        if self.request.user.is_authenticated:
            wishlist_ids = Wishlist.objects.filter(
                user=self.request.user
            ).values_list('object_id', flat=True)
            context['wishlist_ids'] = list(wishlist_ids)

            # User rating
            user_rating = Rating.objects.filter(
                user=self.request.user,
                content_type=content_type,
                object_id=country.id
            ).first()
            context['user_rating'] = user_rating.stars / 2 if user_rating else 0

            # User comment
            user_comment = Comment.objects.filter(
                user=self.request.user,
                content_type=content_type,
                object_id=country.id
            ).first()
            context['user_comment'] = user_comment

            # Other reviews (not this user)
            context['reviews'] = Comment.objects.filter(
                content_type=content_type,
                object_id=country.id
            ).exclude(user=self.request.user).select_related('user').order_by('-created_at')

        else:
            context['wishlist_ids'] = []
            context['user_rating'] = 0
            context['user_comment'] = None

            context['reviews'] = Comment.objects.filter(
                content_type=content_type,
                object_id=country.id
            ).select_related('user').order_by('-created_at')

        # Ratings by user ID for use in templates
        ratings = Rating.objects.filter(
            content_type=content_type,
            object_id=country.id
        )
        context['ratings_by_user'] = {r.user_id: r.stars / 2 for r in ratings}

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


@require_POST
@login_required
def rate_country(request, country_id):
    from django.shortcuts import get_object_or_404

    stars = request.POST.get("stars")
    try:
        stars = float(stars)
        if stars < 1 or stars > 5:
            raise ValueError
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'error': 'Invalid rating'}, status=400)

    country = get_object_or_404(Country, pk=country_id)
    content_type = ContentType.objects.get_for_model(Country)

    # Remove existing rating(s) by this user for this country
    Rating.objects.filter(user=request.user, content_type=content_type, object_id=country.id).delete()

    # Save new rating (stored as 2 to 10, i.e., x2)
    Rating.objects.create(
        user=request.user,
        stars=int(stars * 2),
        content_type=content_type,
        object_id=country.id
    )

    # Calculate average
    all_stars = Rating.objects.filter(content_type=content_type, object_id=country.id)
    average = sum([r.stars for r in all_stars]) / (2 * len(all_stars))

    return JsonResponse({'success': True, 'average_rating': round(average, 1)})


@require_POST
@login_required
def submit_comment(request):
    comment_text = request.POST.get("text")  # updated from 'comment'
    object_id = request.POST.get("object_id")
    content_type_id = request.POST.get("content_type_id")

    if not (comment_text and object_id and content_type_id):
        return JsonResponse({"success": False, "error": "Missing fields"})

    try:
        content_type = ContentType.objects.get_for_id(content_type_id)
    except ContentType.DoesNotExist:
        return JsonResponse({"success": False, "error": "Invalid content type"})

    # Find latest rating by this user for the object (optional link)
    latest_rating = Rating.objects.filter(
        user=request.user,
        content_type=content_type,
        object_id=object_id
    ).order_by("-created_at").first()

    # Either update or create the user's comment for this object
    comment, created = Comment.objects.update_or_create(
        user=request.user,
        content_type=content_type,
        object_id=object_id,
        defaults={
            "text": comment_text,
            "rating": latest_rating
        }
    )

    return JsonResponse({
        "success": True,
        "created": created,
        "text": comment.text,
        "timestamp": comment.created_at.strftime("%b %d, %Y %H:%M")
    })