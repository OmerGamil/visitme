from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    story = models.TextField()
    cover_photo = CloudinaryField('image', default='default-country.jpg', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_cover_photo(self):
        content_type = ContentType.objects.get_for_model(Landmark)
        rated_places = Landmark.objects.filter(city__country=self).annotate(
            avg_rating=models.Avg(
                models.Subquery(
                    Rating.objects.filter(
                        content_type=content_type,
                        object_id=models.OuterRef('pk')
                    ).values('stars')
                )
            )
        ).order_by('-avg_rating')

        best_place = rated_places.first()
        return self.cover_photo.url if self.cover_photo else best_place.photos.first().image.url if best_place and best_place.photos.exists() else None

    def average_rating(self):
        content_type = ContentType.objects.get_for_model(self)
        avg_raw = Rating.objects.filter(content_type=content_type, object_id=self.id).aggregate(models.Avg('stars'))['stars__avg']
        return round(avg_raw / 2, 1) if avg_raw else None


class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    story = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    cover_photo = CloudinaryField('image', default='default-city.jpg', blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.country.name}"

    def get_cover_photo(self):
        content_type = ContentType.objects.get_for_model(Landmark)
        rated_places = Landmark.objects.filter(city=self).annotate(
            avg_rating=models.Avg(
                models.Subquery(
                    Rating.objects.filter(
                        content_type=content_type,
                        object_id=models.OuterRef('pk')
                    ).values('stars')
                )
            )
        ).order_by('-avg_rating')

        best_place = rated_places.first()
        return self.cover_photo.url if self.cover_photo else best_place.photos.first().image.url if best_place and best_place.photos.exists() else None

    def average_rating(self):
        content_type = ContentType.objects.get_for_model(self)
        avg_raw = Rating.objects.filter(content_type=content_type, object_id=self.id).aggregate(models.Avg('stars'))['stars__avg']
        return round(avg_raw / 2, 1) if avg_raw else None


class Landmark(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="landmarks")
    location = models.CharField(max_length=255)
    story = models.TextField()

    def __str__(self):
        return f"{self.name} in {self.city.name}"

    def average_rating(self):
        content_type = ContentType.objects.get_for_model(self)
        avg_raw = Rating.objects.filter(content_type=content_type, object_id=self.id).aggregate(models.Avg('stars'))['stars__avg']
        return round(avg_raw / 2, 1) if avg_raw else None


class Photo(models.Model):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE, related_name="photos")
    image = CloudinaryField('image')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Photo of {self.landmark.name}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i / 2)) for i in range(2, 11)])  # 1.0 to 5.0 by 0.5
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stars / 2} stars by {self.user}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.content_object}"
