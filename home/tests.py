from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from discoveries.models import Country, City, Landmark, Wishlist
from django.contrib.contenttypes.models import ContentType

class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.country = Country.objects.create(name="Austria", slug="austria", story="Country story")
        self.city = City.objects.create(name="Vienna", slug="vienna", country=self.country, story="City story")
        self.landmark = Landmark.objects.create(name="Palace", slug="palace", city=self.city, location="Center", story="Landmark story")

    def test_home_view_anonymous(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("top_countries", response.context)
        self.assertIn("top_cities", response.context)
        self.assertIn("top_landmarks", response.context)
        self.assertIn("user_wishlist", response.context)
        self.assertEqual(len(response.context["user_wishlist"]), 0)

    def test_home_view_logged_in_with_wishlist(self):
        self.client.login(username="testuser", password="testpass")
        ct = ContentType.objects.get_for_model(Country)
        Wishlist.objects.create(user=self.user, content_type=ct, object_id=self.country.id)

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.country, response.context["user_wishlist"])
        context_country = response.context["top_countries"][0]
        self.assertTrue(context_country.is_wishlisted)


    def test_about_view(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/about.html")

    def test_hidden_gems_view(self):
        response = self.client.get(reverse("hidden_gems"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/hidden_gems.html")
