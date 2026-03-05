# lms_data/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Library, Book, Author, Category, Member, Borrowing, Review
from .serializers import (
    LibrarySerializer,
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    MemberSerializer,
    BorrowingSerializer,
    ReviewSerializer
)

# ---------------- Library ----------------
class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name', 'campus_location']
    search_fields = ['library_id', 'name', 'campus_location']

# ---------------- Author ----------------
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['first_name', 'last_name', 'birth_date']
    search_fields = ['first_name', 'last_name', 'biography']

# ---------------- Category ----------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name']
    search_fields = ['name', 'description']

# ---------------- Book ----------------
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['library_id']
    ordering_fields = ['title', 'publication_date', 'total_copies']
    search_fields = ['title', 'isbn']

# ---------------- Member ----------------
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['first_name', 'last_name', 'registration_date', 'member_type']
    search_fields = ['first_name', 'last_name', 'contact_email', 'phone_number']

# ---------------- Borrowing ----------------
class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['borrow_date', 'return_date']
    ordering = ('-borrow_date')

# ---------------- Review ----------------
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['member_id', 'book_id']
    ordering_fields = ['rating', 'review_date']
    ordering = ('-review_date')

