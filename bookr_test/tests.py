from django.test import TestCase, Client ,RequestFactory
from django.contrib.auth.models import User ,AnonymousUser
from .views import greeting_user
# Create your tests here.


# class TestPublisherModel(TestCase):
#     def setUp(self):
#         self.p = Publisher(name='Packt',
#                            website='www.packt.com',
#                            email='contact@packt.com')

#     def test_creae_publisher(self):
#         self.assertIsInstance(self.p, Publisher)

#     def test_str_representation(self):
#         self.assertEquals(self.p.name, "Packt")


# class TestGreetingView(TestCase):
#     def setUp(self) -> None:
#         self.c = Client()

#     def test_grerting_view(self):
#         reponse=self.c.get("/test/greeting")
#         self.assertEqual(reponse.status_code,200 )

### Test Authentication
# class TestLoginGreetingView(TestCase):
#     def setUp(self):
#         test_user = User.objects.create(username='testuser')
#         test_user.set_password('test@#628password')
#         test_user.save()
#         self.client = Client()

#     def test_user_greeting_not_authenticated(self):
#         response = self.client.get('/test/greeting-user')
#         self.assertEquals(response.status_code, 302)

#     def test_user_authenticated(self):
#         login = self.client.login(username='testuser',
#                                   password='test@#628password')
#         self.assertEquals(login,True)
#         response = self.client.get('/test/greeting-user')
#         self.assertEquals(response.status_code, 200)

class TestLoginGreetingView(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='testuser')
        self.test_user.set_password('test@#628password')
        self.test_user.save()
        self.factory = RequestFactory()

    def test_user_greeting_not_authenticated(self):
        request = self.factory.get('/test/greeting-user')
        request.user=AnonymousUser()
        response=greeting_user(request)
        self.assertEquals(response.status_code, 302)

    def test_user_authenticated(self):
        request=self.factory.get("/test/greeting-user")
        request.user=self.test_user
        response=greeting_user(request)
        self.assertEquals(response.status_code, 200)

