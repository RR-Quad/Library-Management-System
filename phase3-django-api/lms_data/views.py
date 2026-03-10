from django.db import transaction
from django.shortcuts import get_object_or_404
from datetime import timedelta

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, filters
from rest_framework.views import APIView

from django.utils import timezone
from django.db.models import Value, Count, Avg, Sum
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

from .models import Library, Book, Author, Category, Member, Borrowing, Review
from .serializers import (
    LibrarySerializer,
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    MemberSerializer,
    BorrowingSerializer,
    ReviewSerializer,
    StatisticsSerializer,
    BorrowBookSerializer,
    ReturnBookSerializer,
    BookSearchSerializer,
)


# =========================================================
# Library
# =========================================================

@extend_schema_view(
    list=extend_schema(
        summary="List libraries",
        description="Retrieve a list of all library branches."
    ),
    retrieve=extend_schema(
        summary="Retrieve library",
        description="Get details for a specific library."
    )
)
class LibraryViewSet(viewsets.ModelViewSet):

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    ordering_fields = ["library_id", "name", "campus_location"]
    ordering = ["library_id"]


# =========================================================
# Author
# =========================================================

@extend_schema_view(
    list=extend_schema(summary="List authors"),
    retrieve=extend_schema(summary="Retrieve author details")
)
class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    ordering_fields = ["first_name", "last_name", "birth_date"]


# =========================================================
# Category
# =========================================================

@extend_schema_view(
    list=extend_schema(summary="List categories"),
    retrieve=extend_schema(summary="Retrieve category details")
)
class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    ordering_fields = ["category_id", "name"]


# =========================================================
# Book
# =========================================================

@extend_schema_view(
    list=extend_schema(summary="List books"),
    retrieve=extend_schema(summary="Retrieve book details")
)
class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.select_related("library_id").prefetch_related(
        "authors",
        "categories"
    )

    serializer_class = BookSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]

    ordering_fields = ["book_id", "title"]
    ordering = ["book_id"]

    # -----------------------------------------------------

    @extend_schema(
        summary="Borrow a book",
        description="Borrow a book if copies are available. "
                    "A due date is automatically set to 14 days.",
        request=BorrowBookSerializer,
        responses={201: BorrowingSerializer},
        tags=["Borrowing"]
    )
    @action(detail=False, methods=["post"], url_path="borrow")
    def borrow_book(self, request):

        serializer = BorrowBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_id = serializer.validated_data["book_id"]
        member_id = serializer.validated_data["member_id"]

        with transaction.atomic():

            book = get_object_or_404(
                Book.objects.select_for_update(),
                pk=book_id
            )

            member = get_object_or_404(Member, pk=member_id)

            if not book.is_available:
                return Response(
                    {"error": "Book not available"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            borrow_date = timezone.now().date()
            due_date = borrow_date + timedelta(days=14)

            borrowing = Borrowing.objects.create(
                book_id=book,
                member_id=member,
                borrow_date=borrow_date,
                due_date=due_date
            )

            book.available_copies -= 1
            book.save(update_fields=["available_copies"])

        return Response(
            BorrowingSerializer(borrowing).data,
            status=status.HTTP_201_CREATED
        )

    # -----------------------------------------------------

    @extend_schema(
        summary="Return a borrowed book",
        description="Marks a borrowed book as returned and "
                    "calculates late fees if overdue.",
        request=ReturnBookSerializer,
        responses={200: BorrowingSerializer},
        tags=["Borrowing"]
    )
    @action(detail=False, methods=["post"], url_path="return")
    def return_book(self, request):

        serializer = ReturnBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        borrowing_id = serializer.validated_data["borrowing_id"]

        with transaction.atomic():

            borrowing = get_object_or_404(
                Borrowing.objects.select_for_update(),
                pk=borrowing_id
            )

            if borrowing.return_date is not None:
                return Response(
                    {"error": "Book already returned"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return_date = timezone.now().date()

            days_late = max((return_date - borrowing.due_date).days, 0)
            late_fee = days_late * 1

            borrowing.return_date = return_date
            borrowing.late_fee = late_fee

            borrowing.save(update_fields=["return_date", "late_fee"])

            book = borrowing.book_id
            book.available_copies += 1
            book.save(update_fields=["available_copies"])

        return Response(
            BorrowingSerializer(borrowing).data
        )

    # -----------------------------------------------------

    @extend_schema(
        summary="Search books",
        description="Search books by library, category, or author name.",
        request=BookSearchSerializer,
        responses={200: BookSerializer(many=True)}
    )
    @action(detail=False, methods=["post"], url_path="search")
    def search_books(self, request):

        serializer = BookSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        library_id = serializer.validated_data.get("library_id")
        category_id = serializer.validated_data.get("category_id")
        author_name = serializer.validated_data.get("author_name")

        books = self.get_queryset()

        if library_id:
            books = books.filter(library_id=library_id)

        if category_id:
            books = books.filter(categories__category_id=category_id)

        if author_name:

            books = books.annotate(
                full_author_name=Concat(
                    "authors__first_name",
                    Value(" "),
                    "authors__last_name"
                )
            ).filter(full_author_name__iexact=author_name)

        books = books.distinct()

        return Response(
            BookSerializer(books, many=True).data
        )

    # -----------------------------------------------------

    @extend_schema(
        summary="Check book availability",
        description="Returns availability information for a specific book."
    )
    @action(detail=True, methods=["get"], url_path="availability")
    def availability(self, request, pk=None):

        book = get_object_or_404(Book, pk=pk)

        return Response({
            "book": book.title,
            "availability": {
                "total": book.total_copies,
                "available": book.available_copies,
                "status": "Available" if book.is_available else "Not Available"
            }
        })

    # -----------------------------------------------------

    @extend_schema(
        summary="Book recommendations",
        description="Returns recommended books based on popularity "
                    "and highest ratings."
    )
    @action(detail=False, methods=["get"], url_path="recommendations")
    def recommendations(self, request):

        popular_books = (
            Book.objects
            .annotate(borrow_count=Count("borrowings"))
            .order_by("-borrow_count")[:5]
        )

        top_rated_books = (
            Book.objects
            .annotate(avg_rating=Avg("reviews__rating"))
            .filter(avg_rating__isnull=False)
            .order_by("-avg_rating")[:5]
        )

        return Response({
            "most_borrowed_books":
                BookSerializer(popular_books, many=True).data,
            "top_rated_books":
                BookSerializer(top_rated_books, many=True).data
        })


# =========================================================
# Member
# =========================================================

@extend_schema_view(
    list=extend_schema(summary="List members"),
    retrieve=extend_schema(summary="Retrieve member details")
)
class MemberViewSet(viewsets.ModelViewSet):

    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    ordering_fields = ["member_id", "first_name", "last_name"]
    ordering = ["member_id"]

    @extend_schema(
        summary="Member borrowing history",
        description="Returns the borrowing history for a specific member.",
        responses={200: BorrowingSerializer(many=True)}
    )
    @action(detail=True, methods=["get"], url_path="borrowings")
    def borrowing_history(self, request, pk=None):

        member = get_object_or_404(Member, pk=pk)

        borrowings = member.borrowings.all().order_by("-borrow_date")

        return Response(
            BorrowingSerializer(borrowings, many=True).data
        )


# =========================================================
# Borrowing
# =========================================================

class BorrowingViewSet(viewsets.ModelViewSet):

    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    filter_backends = [filters.OrderingFilter]

    ordering_fields = ["borrow_date", "return_date"]
    ordering = ["-borrowing_id"]


# =========================================================
# Review
# =========================================================

class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    ordering_fields = ["rating", "review_date"]
    ordering = ["-review_id"]


# =========================================================
# Statistics / Analytics
# =========================================================

class StatisticsAPIView(APIView):

    @extend_schema(
        summary="Library statistics",
        description="Returns aggregated statistics about library usage and activity.",
        responses={200: StatisticsSerializer}
    )
    def get(self, request):

        data = {
            "total_books": Book.objects.count(),
            "total_members": Member.objects.count(),
            "total_borrowings": Borrowing.objects.count(),
            "books_currently_borrowed":
                Borrowing.objects.filter(return_date__isnull=True).count(),
            "average_book_rating":
                Review.objects.aggregate(avg=Avg("rating"))["avg"],
            "total_late_fees_collected":
                Borrowing.objects.aggregate(total=Sum("late_fee"))["total"]
        }

        return Response(data)