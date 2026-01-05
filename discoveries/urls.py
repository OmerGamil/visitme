from django.urls import path
from . import views

urlpatterns = [
    path("explore/", views.ExploreView.as_view(), name="explore"),
    path('wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
    path('explore/<slug:slug>/', views.CountryDetailView.as_view(), name='country_detail'),
    path('city/<slug:slug>/', views.CityDetailView.as_view(), name='city_detail'), 
    path('landmark/<slug:slug>/', views.LandmarkDetailView.as_view(), name='landmark_detail'),
    path("rate/object/", views.rate_object, name="rate_object"),
    path('rate/comment/', views.submit_comment, name='submit_comment'),
    path("comment/delete/<int:comment_id>/", views.delete_comment, name="delete_comment"),
]
