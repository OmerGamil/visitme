from django.urls import path
from . import views
from .views import toggle_wishlist

urlpatterns = [
    path('explore/', views.CountryListView.as_view(), name='explore'),
    path('wishlist/toggle/', toggle_wishlist, name='toggle_wishlist'),
    path('explore/<slug:slug>/', views.CountryDetailView.as_view(), name='country_detail'),
    path('rate/country/<int:country_id>/', views.rate_country, name='rate_country'),
    path('rate/comment/', views.submit_comment, name='submit_comment'),
]
