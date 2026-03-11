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
            value={
                "library_id": 1,
                "name": "Central Library",
                "campus_location": "Main Campus",
                "contact_email": "library@university.edu",
                "phone_number": "+123456789",
            },
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
            value={
                "author_id": 1,
                "first_name": "J.K.",
                "last_name": "Rowling",
                "nationality": "British",
            }
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
            value={
                "category_id": 1,
                "name": "Fantasy",
                "description": "Fantasy literature category",
            }
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
            value={
                "book_id": 1,
                "title": "Harry Potter and the Philosopher's Stone",
                "isbn": "9780747532699",
                "publication_date": "1997-06-26",
                "total_copies": 10,
                "available_copies": 7,
                "library": {
                    "library_id": 1,
                    "name": "Central Library",
                    "campus_location": "Main Campus",
                },
            }
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
            value={
                "member_id": 5,
                "first_name": "John",
                "last_name": "Doe",
                "contact_email": "john.doe@email.com",
                "member_type": "student",
            }
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
            value={
                "borrowing_id": 10,
                "member_name": "John Doe",
                "borrow_date": "2026-03-10",
                "due_date": "2026-03-24",
                "return_date": None,
                "late_fee": None,
            }
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
            value={
                "review_id": 2,
                "rating": 5,
                "comment": "Excellent book!",
                "review_date": "2026-03-11",
            }
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
            value={
                "book_id": 1,
                "member_id": 5
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
            value={
                "borrowing_id": 10
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
            value={
                "library_id": 1,
                "category_id": 3,
                "author_name": "J.K. Rowling"
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

class StatisticsSerializer(serializers.Serializer):

    total_books = serializers.IntegerField()
    total_members = serializers.IntegerField()
    total_borrowings = serializers.IntegerField()
    books_currently_borrowed = serializers.IntegerField()
    average_book_rating = serializers.FloatField(allow_null=True)
    total_late_fees_collected = serializers.FloatField(allow_null=True)
# =========================================================
# End
# =========================================================