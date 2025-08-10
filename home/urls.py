from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("about/", views.AboutView.as_view(), name="about"),
    path("hidden-gems/", views.HiddenGemsView.as_view(), name="hidden_gems"),
]