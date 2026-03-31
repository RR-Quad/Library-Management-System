from rest_framework import serializers
from drf_spectacular.utils import (
    extend_schema_serializer,
    OpenApiExample,
)

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

    class Meta:
        model = Author
        fields = ["author_id", "first_name", "last_name"]


class NestedCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["category_id", "name"]


class NestedLibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Library
        fields = ["library_id", "name", "campus_location"]


class NestedMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ["member_id", "first_name", "last_name"]


# =========================================================
# Main Serializers
# =========================================================

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Library Example",
            summary="Example of a library record",
            description="Represents a physical university library location.",
            value={
                "library_id": 1,
                "name": "Main Library",
                "campus_location": "Central Campus",
                "contact_email": "library@university.edu",
                "phone_number": "+123456789",
            },
            response_only=False,
        )
    ]
)
class LibrarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Library
        fields = "__all__"
        read_only_fields = ["library_id", "created_at", "updated_at"]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Author Example",
            summary="Example of an author record",
            description="Represents a book author.",
            value={
                "author_id": 1,
                "first_name": "J.K.",
                "last_name": "Rowling",
                "birth_date": "1965-07-31",
                "nationality": "British",
                "biography": "Author of the Harry Potter series.",
            },
            response_only=False,
        )
    ]
)
class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"
        read_only_fields = ["author_id", "created_at", "updated_at"]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Category Example",
            summary="Example of a category record",
            description="Represents a book category or genre.",
            value={
                "category_id": 1,
                "name": "Literature",
                "description": "Books related to literary works, novels, and writings.",
            },
            response_only=False,
        )
    ]
)
class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["category_id", "created_at", "updated_at"]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Book Example",
            summary="Example of a book record",
            description="Represents a book available in a library.",
            value={
                "book_id": 1,
                "title": "Harry Potter and the Philosopher's Stone",
                "isbn": "9780747532699",
                "publication_date": "1997-06-26",
                "total_copies": 10,
                "available_copies": 7,
                "library_id": "http://localhost:8000/api/libraries/1/",
                "library": {
                    "library_id": 1,
                    "name": "Main Library",
                    "campus_location": "Central Campus",
                },
                "authors": [
                    {
                        "author_id": 1,
                        "first_name": "J.K.",
                        "last_name": "Rowling",
                    }
                ],
                "categories": [
                    {
                        "category_id": 1,
                        "name": "Literature",
                    }
                ],
            },
            response_only=False,
        )
    ]
)
class BookSerializer(serializers.HyperlinkedModelSerializer):

    library = NestedLibrarySerializer(source="library_id", read_only=True)
    authors = NestedAuthorSerializer(many=True, read_only=True)
    categories = NestedCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ["book_id", "created_at", "updated_at"]

    def validate(self, data):
        total = data.get("total_copies")
        available = data.get("available_copies")

        if total is not None and available is not None:
            if available > total:
                raise serializers.ValidationError(
                    "Available copies cannot exceed total copies."
                )

        return data


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Member Example",
            summary="Example of a member record",
            description="Represents a registered library member.",
            value={
                "member_id": 5,
                "first_name": "John",
                "last_name": "Doe",
                "contact_email": "john.doe@email.com",
                "phone_number": "+1234567890",
                "member_type": "student",
                "registration_date": "2026-01-01",
            },
            response_only=False,
        )
    ]
)
class MemberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Member
        fields = "__all__"
        read_only_fields = ["member_id", "created_at", "updated_at"]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Borrowing Example",
            summary="Example of a borrowing transaction",
            description="Represents a book borrowing transaction.",
            value={
                "borrowing_id": 10,
                "member_name": "John Doe",
                "member": {
                    "member_id": 5,
                    "first_name": "John",
                    "last_name": "Doe",
                },
                "book": {
                    "book_id": 1,
                    "title": "Harry Potter and the Philosopher's Stone",
                    "isbn": "9780747532699",
                },
                "borrow_date": "2026-03-10",
                "due_date": "2026-03-24",
                "return_date": None,
                "late_fee": None,
            },
            response_only=False,
        )
    ]
)
class BorrowingSerializer(serializers.HyperlinkedModelSerializer):

    book = BookSerializer(source="book_id", read_only=True)
    member = NestedMemberSerializer(source="member_id", read_only=True)

    member_name = serializers.SerializerMethodField(
        help_text="Full name of the member who borrowed the book."
    )

    class Meta:
        model = Borrowing
        fields = "__all__"
        read_only_fields = ["borrowing_id", "created_at", "updated_at"]

    @staticmethod
    def get_member_name(obj) -> str:
        return f"{obj.member_id.first_name} {obj.member_id.last_name}"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Review Example",
            summary="Example of a book review",
            description="Represents a member review for a book.",
            value={
                "review_id": 2,
                "rating": 5,
                "comment": "Excellent book!",
                "review_date": "2026-03-11",
                "member_id": "http://localhost:8000/api/members/1/",
                "book_id": "http://localhost:8000/api/books/1/",
            },
            response_only=False,
        )
    ]
)
class ReviewSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["review_id", "created_at", "updated_at"]


# =========================================================
# Functional Serializers (Action-based endpoints)
# =========================================================

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Borrow Book Request",
            summary="Borrow book request example",
            description="Provide book_id and member_id to borrow a book.",
            value={
                "book_id": 1,
                "member_id": 5,
            },
            request_only=True,
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

    @staticmethod
    def validate_book_id(value):
        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Book does not exist.")
        return value

    @staticmethod
    def validate_member_id(value):
        if not Member.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Member does not exist.")
        return value


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Return Book Request",
            summary="Return book request example",
            description="Provide borrowing_id to return a borrowed book.",
            value={
                "borrowing_id": 10,
            },
            request_only=True,
        )
    ]
)
class ReturnBookSerializer(serializers.Serializer):

    borrowing_id = serializers.IntegerField(
        help_text="Borrowing transaction ID."
    )

    @staticmethod
    def validate_borrowing_id(value):
        if not Borrowing.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "Borrowing record does not exist."
            )
        return value


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Book Search Example",
            summary="Book search request example",
            description="Search books by library, category, or author name. All fields are optional.",
            value={
                "library_id": 1,
                "category_id": 3,
                "author_name": "J.K. Rowling",
            },
            request_only=True,
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
        help_text="Full author name (first and last)."
    )


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Statistics Example",
            summary="Library statistics example",
            description="Aggregated statistics for the entire library system.",
            value={
                "total_books": 150,
                "total_members": 320,
                "total_borrowings": 540,
                "books_currently_borrowed": 45,
                "average_book_rating": 4.2,
                "total_late_fees_collected": 125.50,
            },
            response_only=True,
        )
    ]
)
class StatisticsSerializer(serializers.Serializer):

    total_books = serializers.IntegerField(
        help_text="Total number of books in the library system."
    )
    total_members = serializers.IntegerField(
        help_text="Total number of registered members."
    )
    total_borrowings = serializers.IntegerField(
        help_text="Total number of borrowing transactions."
    )
    books_currently_borrowed = serializers.IntegerField(
        help_text="Number of books currently borrowed and not yet returned."
    )
    average_book_rating = serializers.FloatField(
        allow_null=True,
        help_text="Average rating across all book reviews."
    )
    total_late_fees_collected = serializers.FloatField(
        allow_null=True,
        help_text="Total late fees collected from overdue borrowings."
    )

# =========================================================
# End
# =========================================================