from django.contrib import admin
from .models import Country, City, Landmark, Photo, Rating, Comment
from django_summernote.admin import SummernoteModelAdmin

class PhotoInline(admin.TabularInline): 
    model = Photo
    extra = 1
    fields = ['image', 'caption']

@admin.register(Country)
class CountryAdmin(SummernoteModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('story',)

@admin.register(City)
class CityAdmin(SummernoteModelAdmin):
    list_display = ('name', 'slug', 'country')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('story',)

@admin.register(Landmark)
class LandmarkAdmin(SummernoteModelAdmin):
    list_display = ('name', 'slug', 'city')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('story',)
    inlines = [PhotoInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('landmark', 'caption')
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