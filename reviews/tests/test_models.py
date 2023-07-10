from django.test import TestCase
from reviews.models import Publisher, Book, Contributor
from django.utils import timezone


class TestPublisherModel(TestCase):
    def test_create_publisher(self):
        publisher = Publisher.objects.create(name='Packt',
                                             website='www.packt.com',
                                             email='contact@packt.com')
        self.assertIsInstance(publisher, Publisher)


class TestBookModel(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name='Packt',
                                                  website='www.packt.com',
                                                  email='contact@packt.com')
        self.contributor = Contributor.objects.create(first_names="mmma",
                                                      last_names="mdsad",
                                                      email='ddasda@dsad.com')

    def test_create_book(self):
        book = Book.objects.create(title="asdaadad", publication_date='1999-07-09',
                                   isbn='11551566456', publisher=self.publisher)
        book.contributor.set([self.contributor],through_defaults={'role': 'CO_AUTHOR'})
        self.assertIsInstance(book, Book)


class TestContributorModel(TestCase):
    def test_create_contributor(self):
        contributor = Contributor.objects.create(first_names="mmma",
                                                 last_names="mdsad",
                                                 email='ddasda@dsad.com')
        self.assertIsInstance(contributor,Contributor)