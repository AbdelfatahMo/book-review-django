from django.test import TestCase, RequestFactory
from reviews.views import welcome_view


class TestWelcomeView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_welcome_view(self):
        request=self.factory.get("/")
        response = welcome_view(request)
        self.assertEquals(response.status_code,200)
