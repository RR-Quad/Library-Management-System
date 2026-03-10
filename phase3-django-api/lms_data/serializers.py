## Imports


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


## Nested Serializer Classes


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


## Main Serializer Classes


class LibrarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Library
        fields = "__all__"


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.HyperlinkedModelSerializer):

    library = NestedLibrarySerializer(source="library_id", read_only=True)
    authors = NestedAuthorSerializer(many=True, read_only=True)
    categories = NestedCategorySerializer(many=True, read_only=True)

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

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class BorrowingSerializer(serializers.HyperlinkedModelSerializer):

    book_title = serializers.CharField(source="book_id.title", read_only=True)
    member_name = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = "__all__"

    def get_member_name(self, obj):
        return f"{obj.member_id.first_name} {obj.member_id.last_name}"

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


## Functional Serializer Classes


class BorrowBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    member_id = serializers.IntegerField()


class ReturnBookSerializer(serializers.Serializer):
    borrowing_id = serializers.IntegerField()


class BookSearchSerializer(serializers.Serializer):
    library_id = serializers.IntegerField(required=False, allow_null=True)
    category_id = serializers.IntegerField(required=False, allow_null=True)
    author_name = serializers.CharField(required=False, allow_blank=True)


## End