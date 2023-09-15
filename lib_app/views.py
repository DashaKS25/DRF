from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsOwnerOrCreate, IsLoggedInPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import IsAuthorFilterBackend

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrCreate, IsLoggedInPermission]
    filter_backends = [SearchFilter, OrderingFilter, IsAuthorFilterBackend]
    search_fields = ["title"]

    def get_queryset(self):
        queryset = Book.objects.all()
        author_age = self.request.query_params.get('author_age')

        if author_age is not None and author_age.isdigit():
            queryset = queryset.filter(authors__age__gte=author_age)
        return queryset

    """
    Author age use for filtering books/authors by age
    """

    def create(self, request, *args, **kwargs):
        request.data['title'] += '!'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Call perform_create
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        # save object
        serializer.save()

    """
    Calling perform_create method for saving new object(book)
    """


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @action(detail=True, methods=(['GET']))
    def books (self, request, pk=None):
        author = self.get_object()
        book_name = request.query_params.get('book_name', '')

        if book_name:

            books = author.books.filter(title__icontains=book_name)
        else:

            books = author.books.all()

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)