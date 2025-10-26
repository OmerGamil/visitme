from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from discoveries.models import Country, City, Landmark, Rating, Comment, Wishlist
from django.contrib.contenttypes.models import ContentType

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.country = Country.objects.create(name="Austria", slug="austria", story="History")
        self.city = City.objects.create(name="Vienna", slug="vienna", country=self.country, story="City story")
        self.landmark = Landmark.objects.create(name="Palace", slug="palace", city=self.city, location="Central", story="Landmark story")

    def test_explore_view(self):
        url = reverse("explore")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Explore Countries")

    def test_country_detail_view(self):
        url = reverse("country_detail", kwargs={"slug": self.country.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.country.name)

    def test_city_detail_view(self):
        url = reverse("city_detail", kwargs={"slug": self.city.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.city.name)

    def test_landmark_detail_view(self):
        url = reverse("landmark_detail", kwargs={"slug": self.landmark.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.landmark.name)

    def test_toggle_wishlist_add_and_remove(self):
        self.client.login(username='testuser', password='pass1234')
        ct = ContentType.objects.get_for_model(Country)

        # Add
        response = self.client.post(reverse("toggle_wishlist"), {
            "content_type_id": ct.id,
            "object_id": self.country.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "added"})
        self.assertEqual(Wishlist.objects.count(), 1)

        # Remove
        response = self.client.post(reverse("toggle_wishlist"), {
            "content_type_id": ct.id,
            "object_id": self.country.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "removed"})
        self.assertEqual(Wishlist.objects.count(), 0)

    def test_rate_object_ajax(self):
        self.client.login(username='testuser', password='pass1234')
        ct = ContentType.objects.get_for_model(Country)

        response = self.client.post(reverse("rate_object"), {
            "stars": 5,
            "content_type_id": ct.id,
            "object_id": self.country.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("average_rating", response.json())
        self.assertEqual(Rating.objects.count(), 1)

    def test_submit_comment_ajax(self):
        self.client.login(username='testuser', password='pass1234')
        ct = ContentType.objects.get_for_model(Country)

        # First rate the country
        Rating.objects.create(user=self.user, stars=10, content_type=ct, object_id=self.country.id)

        response = self.client.post(reverse("submit_comment"), {
            "text": "Wonderful!",
            "content_type_id": ct.id,
            "object_id": self.country.id
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(Comment.objects.count(), 1)
