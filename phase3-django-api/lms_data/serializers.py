from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from .models import (
    Library,
    Book,
    Author,
    Category,
    Member,
    Borrowing,
    Review,
)


# =========================================================
# Nested Serializers
# =========================================================

class NestedAuthorSerializer(serializers.ModelSerializer):
    """Compact representation of an author used inside book responses."""

    class Meta:
        model = Author
        fields = ["author_id", "first_name", "last_name"]


class NestedCategorySerializer(serializers.ModelSerializer):
    """Compact representation of a category used inside book responses."""

    class Meta:
        model = Category
        fields = ["category_id", "name"]


class NestedLibrarySerializer(serializers.ModelSerializer):
    """Compact representation of a library used inside book responses."""

    class Meta:
        model = Library
        fields = ["library_id", "name", "campus_location"]


# =========================================================
# Core Model Serializers
# =========================================================

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Library Example",
            summary="Example library record",
            value={
                "library_id": 1,
                "name": "Central Library",
                "campus_location": "North Campus",
                "contact_email": "library@university.edu",
                "phone_number": "555-123-4567"
            }
        )
    ]
)
class LibrarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Library
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Author Example",
            value={
                "author_id": 3,
                "first_name": "George",
                "last_name": "Orwell",
                "nationality": "British"
            }
        )
    ]
)
class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Category Example",
            value={
                "category_id": 2,
                "name": "Science Fiction",
                "description": "Books based on futuristic concepts."
            }
        )
    ]
)
class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Book Example",
            summary="Example book response",
            value={
                "book_id": 10,
                "title": "1984",
                "isbn": "9780451524935",
                "publication_date": "1949-06-08",
                "total_copies": 5,
                "available_copies": 3,
                "library": {
                    "library_id": 1,
                    "name": "Central Library",
                    "campus_location": "North Campus"
                },
                "authors": [
                    {
                        "author_id": 3,
                        "first_name": "George",
                        "last_name": "Orwell"
                    }
                ],
                "categories": [
                    {
                        "category_id": 2,
                        "name": "Science Fiction"
                    }
                ]
            }
        )
    ]
)
class BookSerializer(serializers.HyperlinkedModelSerializer):

    library = NestedLibrarySerializer(
        source="library_id",
        read_only=True,
        help_text="Library where this book is stored."
    )

    authors = NestedAuthorSerializer(
        many=True,
        read_only=True,
        help_text="Authors who wrote the book."
    )

    categories = NestedCategorySerializer(
        many=True,
        read_only=True,
        help_text="Categories associated with this book."
    )

    class Meta:
        model = Book
        fields = [
            "book_id",
            "title",
            "isbn",
            "publication_date",
            "total_copies",
            "available_copies",
            "library",
            "authors",
            "categories",
        ]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Member Example",
            value={
                "member_id": 7,
                "first_name": "Jane",
                "last_name": "Doe",
                "member_type": "student",
                "contact_email": "jane@example.com",
                "phone_number": "555-444-9999"
            }
        )
    ]
)
class MemberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Member
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Borrowing Example",
            value={
                "borrowing_id": 15,
                "book_title": "1984",
                "member_name": "Jane Doe",
                "borrow_date": "2025-03-01",
                "due_date": "2025-03-15",
                "return_date": None,
                "late_fee": 0
            }
        )
    ]
)
class BorrowingSerializer(serializers.HyperlinkedModelSerializer):

    book_title = serializers.CharField(
        source="book_id.title",
        read_only=True,
        help_text="Title of the borrowed book."
    )

    member_name = serializers.SerializerMethodField(
        help_text="Full name of the member who borrowed the book."
    )

    class Meta:
        model = Borrowing
        fields = "__all__"

    def get_member_name(self, obj) -> str:
        return f"{obj.member_id.first_name} {obj.member_id.last_name}"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Review Example",
            value={
                "review_id": 3,
                "book_id": 10,
                "member_id": 7,
                "rating": 5,
                "comment": "Excellent dystopian novel.",
                "review_date": "2025-03-10"
            }
        )
    ]
)
class ReviewSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"


class StatisticsSerializer(serializers.Serializer):
    """
    Serializer for library analytics and aggregated statistics.
    """

    total_books = serializers.IntegerField(
        help_text="Total number of books in the system."
    )

    total_members = serializers.IntegerField(
        help_text="Total number of registered library members."
    )

    total_borrowings = serializers.IntegerField(
        help_text="Total number of borrowing transactions recorded."
    )

    books_currently_borrowed = serializers.IntegerField(
        help_text="Number of books currently borrowed and not yet returned."
    )

    average_book_rating = serializers.FloatField(
        allow_null=True,
        help_text="Average rating across all book reviews."
    )

    total_late_fees_collected = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        allow_null=True,
        help_text="Total amount of late fees collected."
    )


# =========================================================
# Functional Serializers (Custom Endpoints)
# =========================================================

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Borrow Request",
            summary="Borrow a book request",
            value={
                "book_id": 10,
                "member_id": 7
            }
        )
    ]
)
class BorrowBookSerializer(serializers.Serializer):

    book_id = serializers.IntegerField(
        help_text="ID of the book to be borrowed."
    )

    member_id = serializers.IntegerField(
        help_text="ID of the member borrowing the book."
    )


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Return Request",
            value={
                "borrowing_id": 15
            }
        )
    ]
)
class ReturnBookSerializer(serializers.Serializer):

    borrowing_id = serializers.IntegerField(
        help_text="ID of the borrowing record to return."
    )


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Book Search Request",
            value={
                "library_id": 1,
                "category_id": 2,
                "author_name": "George Orwell"
            }
        )
    ]
)
class BookSearchSerializer(serializers.Serializer):

    library_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Filter books by library ID."
    )

    category_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Filter books by category ID."
    )

    author_name = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Filter books by full author name."
    )