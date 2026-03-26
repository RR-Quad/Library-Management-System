from django.test import TestCase
from lms_data.serializers import (
    AuthorSerializer,
    LibrarySerializer,
    CategorySerializer,
    BookSerializer,
    MemberSerializer,
    BorrowingSerializer,
    ReviewSerializer,
)
from lms_data.models import Library, Book, Member
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()

class TestAuthorSerializer(TestCase):

    def setUp(self):
        self.valid_data = {
            "first_name": "J.K.",
            "last_name": "Rowling",
            "nationality": "British",
        }

    def test_valid_data(self):
        serializer = AuthorSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_missing_first_name(self):
        self.valid_data.pop("first_name")
        serializer = AuthorSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_missing_last_name(self):
        self.valid_data.pop("last_name")
        serializer = AuthorSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)

    def test_optional_nationality(self):
        data = {"first_name": "John", "last_name": "Doe"}
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_first_name_max_length(self):
        self.valid_data["first_name"] = "A" * 21
        serializer = AuthorSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)


class TestLibrarySerializer(TestCase):

    def setUp(self):
        self.valid_data = {
            "name": "Central Library",
            "campus_location": "Main Campus",
            "contact_email": "library@university.edu",
            "phone_number": "+1234567890",
        }

    def test_valid_data(self):
        serializer = LibrarySerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        self.valid_data["contact_email"] = "notanemail"
        serializer = LibrarySerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("contact_email", serializer.errors)

    def test_missing_name(self):
        self.valid_data.pop("name")
        serializer = LibrarySerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_missing_campus_location(self):
        self.valid_data.pop("campus_location")
        serializer = LibrarySerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("campus_location", serializer.errors)

    def test_missing_phone_number(self):
        self.valid_data.pop("phone_number")
        serializer = LibrarySerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)

    def test_name_max_length(self):
        self.valid_data["name"] = "A" * 31
        serializer = LibrarySerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

class TestCategorySerializer(TestCase):

    def setUp(self):
        self.valid_data = {
            "name": "Fantasy",
            "description": "Fantasy literature",
        }

    def test_valid_data(self):
        serializer = CategorySerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_missing_name(self):
        self.valid_data.pop("name")
        serializer = CategorySerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_optional_description(self):
        data = {"name": "Horror"}
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_name_max_length(self):
        self.valid_data["name"] = "A" * 31
        serializer = CategorySerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


class TestBookSerializer(TestCase):

    def setUp(self):
        self.request = factory.get("/")
        self.library = Library.objects.create(
            name="Central Library",
            campus_location="Main Campus",
            contact_email="library@university.edu",
            phone_number="+1234567890",
        )
        self.valid_data = {
            "title": "Harry Potter",
            "isbn": "9780747532699",
            "publication_date": "1997-06-26",
            "total_copies": 10,
            "available_copies": 7,
            "library_id": f"http://testserver/api/libraries/{self.library.library_id}/",
        }

    def test_valid_data(self):
        serializer = BookSerializer(data=self.valid_data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_available_copies_exceed_total(self):
        self.valid_data["available_copies"] = 15
        serializer = BookSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_missing_title(self):
        self.valid_data.pop("title")
        serializer = BookSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_missing_isbn(self):
        self.valid_data.pop("isbn")
        serializer = BookSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("isbn", serializer.errors)

    def test_missing_publication_date(self):
        self.valid_data.pop("publication_date")
        serializer = BookSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("publication_date", serializer.errors)

    def test_missing_total_copies(self):
        self.valid_data.pop("total_copies")
        serializer = BookSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("total_copies", serializer.errors)


class TestMemberSerializer(TestCase):

    def setUp(self):
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "contact_email": "john@email.com",
            "phone_number": "+1234567890",
            "member_type": "student",
        }

    def test_valid_data(self):
        serializer = MemberSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_member_type(self):
        self.valid_data["member_type"] = "invalid_type"
        serializer = MemberSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("member_type", serializer.errors)

    def test_invalid_email(self):
        self.valid_data["contact_email"] = "notanemail"
        serializer = MemberSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("contact_email", serializer.errors)

    def test_missing_first_name(self):
        self.valid_data.pop("first_name")
        serializer = MemberSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_missing_last_name(self):
        self.valid_data.pop("last_name")
        serializer = MemberSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)

    def test_missing_phone_number(self):
        self.valid_data.pop("phone_number")
        serializer = MemberSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)

    def test_faculty_member_type(self):
        self.valid_data["member_type"] = "faculty"
        serializer = MemberSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())


class TestReviewSerializer(TestCase):

    def setUp(self):
        self.request = factory.get("/")
        self.library = Library.objects.create(
            name="Central Library",
            campus_location="Main Campus",
            contact_email="library@university.edu",
            phone_number="+1234567890",
        )
        self.book = Book.objects.create(
            title="Harry Potter",
            isbn="9780747532699",
            publication_date="1997-06-26",
            total_copies=10,
            available_copies=7,
            library_id=self.library,
        )
        self.member = Member.objects.create(
            first_name="John",
            last_name="Doe",
            contact_email="john@email.com",
            phone_number="+1234567890",
            member_type="student",
        )
        self.valid_data = {
            "rating": 5,
            "comment": "Excellent book!",
            "member_id": f"http://testserver/api/members/{self.member.member_id}/",
            "book_id": f"http://testserver/api/books/{self.book.book_id}/",
        }

    def test_valid_data(self):
        serializer = ReviewSerializer(data=self.valid_data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_rating_above_max(self):
        self.valid_data["rating"] = 6
        serializer = ReviewSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("rating", serializer.errors)

    def test_rating_below_min(self):
        self.valid_data["rating"] = 0
        serializer = ReviewSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("rating", serializer.errors)

    def test_missing_rating(self):
        self.valid_data.pop("rating")
        serializer = ReviewSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("rating", serializer.errors)

    def test_optional_comment(self):
        self.valid_data.pop("comment")
        serializer = ReviewSerializer(data=self.valid_data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)


class TestBorrowingSerializer(TestCase):

    def setUp(self):
        self.request = factory.get("/")
        self.library = Library.objects.create(
            name="Central Library",
            campus_location="Main Campus",
            contact_email="library@university.edu",
            phone_number="+1234567890",
        )
        self.book = Book.objects.create(
            title="Harry Potter",
            isbn="9780747532699",
            publication_date="1997-06-26",
            total_copies=10,
            available_copies=7,
            library_id=self.library,
        )
        self.member = Member.objects.create(
            first_name="John",
            last_name="Doe",
            contact_email="john@email.com",
            phone_number="+1234567890",
            member_type="student",
        )
        self.valid_data = {
            "borrow_date": "2026-03-01",
            "due_date": "2026-03-15",
            "member_id": f"http://testserver/api/members/{self.member.member_id}/",
            "book_id": f"http://testserver/api/books/{self.book.book_id}/",
        }

    def test_valid_data(self):
        serializer = BorrowingSerializer(data=self.valid_data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_due_date(self):
        self.valid_data.pop("due_date")
        serializer = BorrowingSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("due_date", serializer.errors)

    def test_invalid_date_format(self):
        self.valid_data["due_date"] = "not-a-date"
        serializer = BorrowingSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("due_date", serializer.errors)

    def test_missing_member_id(self):
        self.valid_data.pop("member_id")
        serializer = BorrowingSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("member_id", serializer.errors)

    def test_missing_book_id(self):
        self.valid_data.pop("book_id")
        serializer = BorrowingSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("book_id", serializer.errors)