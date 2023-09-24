from django.test import TestCase
from .models import Book, Author
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group



class BookModelTest(TestCase):
    def setUp(self) -> None:
        self.authors = Author.objects.create(name="Oleg", age=50)
        self.book = Book.objects.create(title="Volf", authors=self.authors)

    def test_authors_book(self):
        author = Author.objects.create(name="Petro", age=51)
        book = Book.objects.first()
        self.assertNotEquals(book.authors, author)

    def test_book_author_relationship(self):
        """
              Test to check relationships Author vs Book
        """
        self.assertEqual(self.book.authors, self.authors)
        self.assertIn(self.book, self.authors.books.all())

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Volf")
        self.assertEqual(self.book.authors, self.authors)

    def test_book_str(self):
        expected_string = f"book - {self.book.title} author = {self.authors}"
        self.assertEqual(str(self.book), expected_string)


class AuthorModelTest(TestCase):
    def setUp(self) -> None:
        self.author = Author.objects.create(name="Oleg", age=50)

    def test_author_creation(self):
        self.assertEqual(self.author.name, "Oleg")
        self.assertEqual(self.author.age, 50)

    def test_author_str(self):
        expected_string = "Oleg"
        self.assertEqual(str(self.author), expected_string)

    def test_author_age_default_value(self):
        author_with_default_age = Author.objects.create(name="Petro")
        self.assertEqual(author_with_default_age.age, 30)


class BookViewSetAPITest(APITestCase):
    """
    Set up test data before running each test.

    """
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author_group = Group.objects.create(name='author')
        self.user.groups.add(self.author_group)
        self.authors = Author.objects.create(name='John', age=40)

    def test_create_book_as_author(self):
        """
        Test creating a book by an "author" group.

        """
        self.client.force_authenticate(user=self.user)

        url = '/books/'
        data = {
            'title': 'New Book',
            'authors': self.authors.id,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'New Book!')


    def test_create_book_not_author_group(self):
        """
        Test creating a book by a user not in the 'author' group.

        """
        self.user.groups.clear()
        self.client.force_authenticate(user=self.user)

        url = '/books/'
        data = {
            'title': 'New Book',
            'authors': self.authors.id,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_age(self):
        """
        Test filtering books by author's age.

        """
        self.client.force_authenticate(user=self.user)
        url = f'/books/?author_age={self.authors.age}'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure that all books in the response have the author's correct age
        for book in response.data:
            self.assertEqual(book['authors']['age'], self.authors.age)