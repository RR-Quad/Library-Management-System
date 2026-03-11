from rest_framework import serializers
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

class LibrarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Library
        fields = "__all__"
        read_only_fields = ["library_id", "created_at", "updated_at"]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"
        read_only_fields = ["author_id", "created_at", "updated_at"]


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["category_id", "created_at", "updated_at"]


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


class MemberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Member
        fields = "__all__"
        read_only_fields = ["member_id", "created_at", "updated_at"]


class BorrowingSerializer(serializers.HyperlinkedModelSerializer):

    book = BookSerializer(source="book_id", read_only=True)
    member = NestedMemberSerializer(source="member_id", read_only=True)

    member_name = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = "__all__"
        read_only_fields = ["borrowing_id", "created_at", "updated_at"]

    def get_member_name(self, obj):
        return f"{obj.member_id.first_name} {obj.member_id.last_name}"


class ReviewSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["review_id", "created_at", "updated_at"]


# =========================================================
# Functional Serializers (Action-based endpoints)
# =========================================================

class BorrowBookSerializer(serializers.Serializer):

    book_id = serializers.IntegerField()
    member_id = serializers.IntegerField()

    def validate_book_id(self, value):
        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Book does not exist.")
        return value

    def validate_member_id(self, value):
        if not Member.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Member does not exist.")
        return value


class ReturnBookSerializer(serializers.Serializer):

    borrowing_id = serializers.IntegerField()

    def validate_borrowing_id(self, value):
        if not Borrowing.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Borrowing record does not exist.")
        return value


class BookSearchSerializer(serializers.Serializer):

    library_id = serializers.IntegerField(required=False, allow_null=True)
    category_id = serializers.IntegerField(required=False, allow_null=True)
    author_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )


# =========================================================
# End
# =========================================================