from datetime import timedelta

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Avg, Sum, Value
from django.db.models.functions import Concat

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
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
    BorrowBookSerializer,
    ReturnBookSerializer,
    BookSearchSerializer,
    StatisticsSerializer,
)


# =========================================================
# Library
# =========================================================

@extend_schema_view(
    list=extend_schema(
        summary="List Libraries",
        description="Retrieve a paginated list of all libraries. Supports search and ordering.",
    ),
    retrieve=extend_schema(
        summary="Retrieve Library",
        description="Retrieve details of a specific library by ID.",
    ),
    create=extend_schema(
        summary="Create Library",
        description="Create a new library record.",
    ),
    update=extend_schema(
        summary="Update Library",
        description="Fully update an existing library record.",
    ),
    partial_update=extend_schema(
        summary="Partial Update Library",
        description="Partially update an existing library record.",
    ),
    destroy=extend_schema(
        summary="Delete Library",
        description="Delete a library record by ID.",
    ),
)
class LibraryViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing libraries.
    """

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["name", "campus_location"]
    ordering_fields = ["library_id", "name", "campus_location"]
    ordering = ["library_id"]


# =========================================================
# Author
# =========================================================

@extend_schema_view(
    list=extend_schema(
        summary="List Authors",
        description="Retrieve a paginated list of all authors. Supports search and ordering.",
    ),
    retrieve=extend_schema(
        summary="Retrieve Author",
        description="Retrieve details of a specific author by ID.",
    ),
    create=extend_schema(
        summary="Create Author",
        description="Create a new author record.",
    ),
    update=extend_schema(
        summary="Update Author",
        description="Fully update an existing author record.",
    ),
    partial_update=extend_schema(
        summary="Partial Update Author",
        description="Partially update an existing author record.",
    ),
    destroy=extend_schema(
        summary="Delete Author",
        description="Delete an author record by ID.",
    ),
)
class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing book authors.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["first_name", "last_name"]
    ordering_fields = ["first_name", "last_name", "birth_date"]


# =========================================================
# Category
# =========================================================

@extend_schema_view(
    list=extend_schema(
        summary="List Categories",
        description="Retrieve a paginated list of all categories. Supports search and ordering.",
    ),
    retrieve=extend_schema(
        summary="Retrieve Category",
        description="Retrieve details of a specific category by ID.",
    ),
    create=extend_schema(
        summary="Create Category",
        description="Create a new category record.",
    ),
    update=extend_schema(
        summary="Update Category",
        description="Fully update an existing category record.",
    ),
    partial_update=extend_schema(
        summary="Partial Update Category",
        description="Partially update an existing category record.",
    ),
    destroy=extend_schema(
        summary="Delete Category",
        description="Delete a category record by ID.",
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing book categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["name"]
    ordering_fields = ["category_id", "name"]
    ordering = ["category_id"]


# =========================================================
# Book
# =========================================================

@extend_schema_view(
    list=extend_schema(
        summary="List Books",
        description="Retrieve a paginated list of all books. Supports search and ordering.",
    ),
    retrieve=extend_schema(
        summary="Retrieve Book",
        description="Retrieve details of a specific book by ID.",
    ),
    create=extend_schema(
        summary="Create Book",
        description="Create a new book record.",
    ),
    update=extend_schema(
        summary="Update Book",
        description="Fully update an existing book record.",
    ),
    partial_update=extend_schema(
        summary="Partial Update Book",
        description="Partially update an existing book record.",
    ),
    destroy=extend_schema(
        summary="Delete Book",
        description="Delete a book record by ID.",
    ),
)
class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing books.
    Includes borrowing, returning, searching and recommendations.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = ["title", "isbn"]
    ordering_fields = ["book_id", "title", "publication_date"]
    ordering = ["book_id"]

    # ---------------- Borrow Book ----------------

    @extend_schema(
        summary="Borrow a Book",
        description="Allows a member to borrow a book if copies are available.",
        request=BorrowBookSerializer,
        responses={
            201: BorrowingSerializer,
            400: OpenApiResponse(description="Book unavailable or invalid request"),
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="borrow",
        serializer_class=BorrowBookSerializer,
    )
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

            if not book.is_available():
                return Response(
                    {"error": "Book not available"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            borrow_date = timezone.now().date()
            due_date = borrow_date + timedelta(days=14)

            borrowing = Borrowing.objects.create(
                book_id=book,
                member_id=member,
                borrow_date=borrow_date,
                due_date=due_date,
            )

            book.available_copies -= 1
            book.save(update_fields=["available_copies"])

        return Response(
            BorrowingSerializer(borrowing, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    # ---------------- Return Book ----------------

    @extend_schema(
        summary="Return a Book",
        description="Allows a member to return a borrowed book. Calculates late fee if overdue.",
        request=ReturnBookSerializer,
        responses={
            200: BorrowingSerializer,
            400: OpenApiResponse(description="Book already returned or invalid request"),
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="return",
        serializer_class=ReturnBookSerializer,
    )
    def return_book(self, request):

        serializer = ReturnBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        borrowing_id = serializer.validated_data["borrowing_id"]

        with transaction.atomic():

            borrowing = get_object_or_404(
                Borrowing.objects.select_for_update(),
                pk=borrowing_id,
            )

            if borrowing.return_date:
                return Response(
                    {"error": "Book already returned"},
                    status=status.HTTP_400_BAD_REQUEST,
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
            BorrowingSerializer(borrowing, context={"request": request}).data
        )

    # ---------------- Search ----------------

    @extend_schema(
        summary="Search Books",
        description="Search books by library, category or author name.",
        request=BookSearchSerializer,
        responses={
            200: BookSerializer(many=True),
            400: OpenApiResponse(description="Invalid search parameters"),
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="search",
        serializer_class=BookSearchSerializer,
    )
    def search_books(self, request):

        serializer = BookSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        books = Book.objects.all()

        library_id = serializer.validated_data.get("library_id")
        category_id = serializer.validated_data.get("category_id")
        author_name = serializer.validated_data.get("author_name")

        if library_id:
            books = books.filter(library_id=library_id)

        if category_id:
            books = books.filter(categories__category_id=category_id)

        if author_name:
            books = books.annotate(
                full_author_name=Concat(
                    "authors__first_name",
                    Value(" "),
                    "authors__last_name",
                )
            ).filter(full_author_name__iexact=author_name)

        books = books.distinct()

        return Response(
            BookSerializer(books, many=True, context={"request": request}).data
        )

    # ---------------- Availability ----------------

    @extend_schema(
        summary="Check Book Availability",
        description="Check the availability status of a specific book by ID.",
        responses={
            200: OpenApiResponse(description="Availability status"),
            404: OpenApiResponse(description="Book not found"),
        },
    )
    @action(detail=True, methods=["get"], url_path="availability")
    def availability(self, request, pk=None):

        book = get_object_or_404(Book, pk=pk)

        return Response(
            {
                "book": book.title,
                "availability": {
                    "total": book.total_copies,
                    "available": book.available_copies,
                    "status": (
                        "Available"
                        if book.available_copies > 0
                        else "Not Available"
                    ),
                },
            }
        )

    # ---------------- Recommendations ----------------

    @extend_schema(
        summary="Book Recommendations",
        description="Returns top 5 most borrowed books and top 5 highest rated books.",
        responses={
            200: OpenApiResponse(description="Most borrowed and top rated books"),
        },
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

        return Response(
            {
                "most_borrowed_books": BookSerializer(
                    popular_books,
                    many=True,
                    context={"request": request},
                ).data,
                "top_rated_books": BookSerializer(
                    top_rated_books,
                    many=True,
                    context={"request": request},
                ).data,
            }
        )


# =========================================================
# Member
# =========================================================

@extend_schema_view(
    list=extend_schema(
        summary="List Members",
        description="Retrieve a paginated list of all members. Supports search and ordering.",
    ),
    retrieve=extend_schema(
        summary="Retrieve Member",
        description="Retrieve details of a specific member by ID.",
    ),
    create=extend_schema(
        summary="Create Member",
        description="Register a new library member.",
    ),
    update=extend_schema(
        summary="Update Member",
        description="Fully update an existing member record.",
    ),
    partial_update=extend_schema(
        summary="Partial Update Member",
        description="Partially update an existing member record.",
    ),
    destroy=extend_schema(
        summary="Delete Member",
        description="Delete a member record by ID.",
    ),
)
class MemberViewSet(viewsets.ModelViewSet):

    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["first_name", "last_name", "contact_email"]
    ordering_fields = ["member_id", "first_name", "last_name"]
    ordering = ["member_id"]

    @extend_schema(
        summary="Member Borrowing History",
        description="Retrieve the full borrowing history of a specific member.",
        responses={
            200: BorrowingSerializer(many=True),
            404: OpenApiResponse(description="Member not found"),
        },
    )
    @action(detail=True, methods=["get"], url_path="borrowings")
    def borrowing_history(self, request, pk=None):

        member = get_object_or_404(Member, pk=pk)

        borrowings = member.borrowings.select_related("book_id").order_by(
            "-borrow_date"
        )

        serializer = BorrowingSerializer(
            borrowings,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)


# =========================================================
# Borrowing
# =========================================================

@extend_schema_view(
    list=extend_schema(
        summary="List Borrowings",
        description="Retrieve a paginated list of all borrowing transactions.",
    ),
    retrieve=extend_schema(
        summary="Retrieve Borrowing",
        description="Retrieve details of a specific borrowing transaction by ID.",
    ),
    create=extend_schema(
        summary="Create Borrowing",
        description="Create a new borrowing transaction directly.",
    ),
    update=extend_schema(
        summary="Update Borrowing",
        description="Fully update an existing borrowing transaction.",
    ),
    partial_update=extend_schema(
        summary="Partial Update Borrowing",
        description="Partially update an existing borrowing transaction.",
    ),
    destroy=extend_schema(
        summary="Delete Borrowing",
        description="Delete a borrowing transaction by ID.",
    ),
)
class BorrowingViewSet(viewsets.ModelViewSet):

    queryset = Borrowing.objects.select_related("book_id", "member_id")
    serializer_class = BorrowingSerializer

    filter_backends = [filters.OrderingFilter]

    ordering_fields = ["borrow_date", "return_date"]
    ordering = ["-borrowing_id"]


# =========================================================
# Review
# =========================================================

@extend_schema_view(
    list=extend_schema(
        summary="List Reviews",
        description="Retrieve a paginated list of all book reviews.",
    ),
    retrieve=extend_schema(
        summary="Retrieve Review",
        description="Retrieve details of a specific review by ID.",
    ),
    create=extend_schema(
        summary="Create Review",
        description="Submit a new book review.",
    ),
    update=extend_schema(
        summary="Update Review",
        description="Fully update an existing review.",
    ),
    partial_update=extend_schema(
        summary="Partial Update Review",
        description="Partially update an existing review.",
    ),
    destroy=extend_schema(
        summary="Delete Review",
        description="Delete a review by ID.",
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.select_related("book_id", "member_id")
    serializer_class = ReviewSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["comment"]
    ordering_fields = ["rating", "review_date"]
    ordering = ["-review_id"]


# =========================================================
# Statistics
# =========================================================

@extend_schema(
    summary="System Statistics",
    description="Retrieve aggregated statistics for the library system including total books, members, borrowings, currently borrowed books, average book rating, and total late fees collected.",
    responses={
        200: StatisticsSerializer,
        500: OpenApiResponse(description="Internal server error"),
    },
)
class StatisticsAPIView(APIView):

    @staticmethod
    def get(request):

        data = {
            "total_books": Book.objects.count(),
            "total_members": Member.objects.count(),
            "total_borrowings": Borrowing.objects.count(),
            "books_currently_borrowed": Borrowing.objects.filter(
                return_date__isnull=True
            ).count(),
            "average_book_rating": Review.objects.aggregate(
                Avg("rating")
            )["rating__avg"],
            "total_late_fees_collected": Borrowing.objects.aggregate(
                Sum("late_fee")
            )["late_fee__sum"],
        }

        return Response(data)