from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from ..models import Book
from ..serializers import BookSerializer

BOOK_LIST_URL = reverse('shelf:book-list')
BOOK_ADD_URL = reverse('shelf:book-add')


def detail_url(book_id):
    return reverse('shelf:book-detail', args=[book_id])


def sample_book(title='Дубровский', publisher='Издательский Дом Мещерякова', year=2016):
    return Book.objects.create(title=title, publisher=publisher, year=year)

class PublicBookApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_retrieve_book_list(self):
        """Test retrieving a list of ingredients"""
        Book.objects.create(
            title='Дубровский',
            publisher='Издательский Дом Мещерякова',
            year=2011
        )

        Book.objects.create(
            title='Сказки Пушкина',
            publisher='Издательский Дом AstA',
            year=2016
        )

        res = self.client.get(BOOK_LIST_URL)

        books = Book.objects.all().order_by('id')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_book_create_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(BOOK_ADD_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_detail_login_required(self):
        url = reverse('shelf:book-detail', args=[1])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test_user@test.com'
            'password'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_book_successful(self):
        payload = {
            'title': 'Дубровский',
            'publisher': 'Издательский Дом Мещерякова',
            'year': 2011
        }
        res = self.client.post(BOOK_ADD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Book.objects.filter(
            title=payload['title']
        ).exists()

        self.assertTrue(exists)

    def test_create_book_invalid(self):
        payload = {
            'title': '',
            'publisher': 'Издательский Дом Мещерякова',
            'year': 2011
        }
        res = self.client.post(BOOK_ADD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_book(self):
        book = sample_book()

        payload = {
            'title': 'Дубровский часть 2',
        }
        url = detail_url(book.id)

        self.client.put(url, payload)
        book.refresh_from_db()
        self.assertEqual(book.title, payload['title'])

    def test_full_update_book(self):
        book = sample_book()

        payload = {
            'title': 'Няня',
            'publisher': 'Издательский Дом Аста',
            'year': 2015
        }
        url = detail_url(book.id)

        self.client.put(url, payload)
        book.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(book, key))

    def test_remove_book(self):
        book = sample_book()
        url = detail_url(book.id)
        self.client.delete(url)

        exists = Book.objects.filter(
            id=book.id
        ).exists()

        self.assertFalse(exists)
