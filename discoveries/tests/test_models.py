from django.test import TestCase
from django.contrib.auth.models import User
from discoveries.models import Country, City, Landmark, Rating, Comment, Wishlist, Photo
from django.contrib.contenttypes.models import ContentType

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass')
        self.country = Country.objects.create(name="Austria", slug="austria", story="History of Austria")
        self.city = City.objects.create(name="Vienna", slug="vienna", country=self.country, story="Vienna story")
        self.landmark = Landmark.objects.create(name="Schönbrunn Palace", slug="schonbrunn-palace", city=self.city, location="Schönbrunn, Vienna", story="Imperial Palace")
        self.photo = Photo.objects.create(landmark=self.landmark, image="https://example.com/image.jpg", caption="Palace view")
        self.rating = Rating.objects.create(user=self.user, stars=8, content_type=self.country.get_content_type(), object_id=self.country.id)
        self.comment = Comment.objects.create(user=self.user, text="Beautiful place!", content_type=self.country.get_content_type(), object_id=self.country.id, rating=self.rating)
        self.wishlist = Wishlist.objects.create(user=self.user, content_type=self.country.get_content_type(), object_id=self.country.id)

    def test_country_str(self):
        self.assertEqual(str(self.country), "Austria")

    def test_city_str(self):
        self.assertEqual(str(self.city), "Vienna, Austria")

    def test_landmark_str(self):
        self.assertEqual(str(self.landmark), "Schönbrunn Palace in Vienna")

    def test_photo_str(self):
        self.assertEqual(str(self.photo), "Photo of Schönbrunn Palace")

    def test_rating_str(self):
        self.assertEqual(str(self.rating), "4.0 stars by tester")

    def test_comment_str(self):
        self.assertEqual(str(self.comment), f"Comment by tester on {self.country}")

    def test_wishlist_str(self):
        self.assertEqual(str(self.wishlist), f"{self.user} wishes {self.country}")

    def test_average_rating_country(self):
        self.assertEqual(self.country.average_rating(), 4.0)

    def test_cover_photo_country(self):
        # Should fallback to landmark photo
        url = self.country.get_cover_photo()
        self.assertTrue(url.startswith("http"))
