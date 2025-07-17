from django.contrib import admin
from .models import Country, City, Landmark, Photo, Rating, Comment, Wishlist
from django_summernote.admin import SummernoteModelAdmin

class PhotoInline(admin.TabularInline): 
    model = Photo
    extra = 1
    fields = ['image', 'caption']

class LandmarkInline(admin.TabularInline):
    model = Landmark
    extra = 1
    fields = ['name', 'slug', 'story', 'location', 'brief']

class CityInline(admin.TabularInline):
    model = City
    extra = 1 
    fields = ['name', 'slug', 'story', 'cover_photo', 'brief']

@admin.register(Country)
class CountryAdmin(SummernoteModelAdmin):
    inlines = [CityInline]
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('story',)

@admin.register(City)
class CityAdmin(SummernoteModelAdmin):
    inlines = [LandmarkInline]
    list_display = ('name', 'slug', 'country')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('story',)

@admin.register(Landmark)
class LandmarkAdmin(SummernoteModelAdmin):
    inlines = [PhotoInline]
    list_display = ('name', 'slug', 'city')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('story',)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('landmark', 'caption', 'image_preview')
    search_fields = ('landmark__name', 'caption')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'stars', 'user', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('stars', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'user', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'user', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)