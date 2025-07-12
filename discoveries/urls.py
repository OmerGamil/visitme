from django.urls import path
from . import views

urlpatterns = [
    path('explore/', views.CountryListView.as_view(), name='explore'),
    path('explore/<slug:slug>/', views.CountryDetailView.as_view(), name='country_detail'),
]
