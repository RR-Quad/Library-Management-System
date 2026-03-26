import pytest
from django.test import TestCase
from django.utils import timezone
from lms_data.models import Library, Author, Category, Book, Member, Borrowing, Review


class TestAuthorModel(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            first_name="J.K.",
            last_name="Rowling",
            nationality="British",
        )

    def test_author_created_successfully(self):
        self.assertEqual(self.author.first_name, "J.K.")
        self.assertEqual(self.author.last_name, "Rowling")

    def test_author_str(self):
        self.assertEqual(str(self.author), "J.K. Rowling")


class TestLibraryModel(TestCase):

    def setUp(self):
        self.library = Library.objects.create(
            name="Central Library",
            campus_location="Main Campus",
            contact_email="library@university.edu",
            phone_number="+1234567890",
        )

    def test_library_created_successfully(self):
        self.assertEqual(self.library.name, "Central Library")

    def test_library_str(self):
        self.assertEqual(str(self.library), "Central Library")


class TestBookModel(TestCase):

    def setUp(self):
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

    def test_book_created_successfully(self):
        self.assertEqual(self.book.title, "Harry Potter")

    def test_book_is_available(self):
        self.assertTrue(self.book.is_available())

    def test_book_not_available(self):
        self.book.available_copies = 0
        self.book.save()
        self.assertFalse(self.book.is_available())

    def test_book_str(self):
        self.assertEqual(str(self.book), "Harry Potter")


class TestMemberModel(TestCase):

    def setUp(self):
        self.member = Member.objects.create(
            first_name="John",
            last_name="Doe",
            contact_email="john@email.com",
            phone_number="+1234567890",
            member_type="student",
        )

    def test_member_created_successfully(self):
        self.assertEqual(self.member.first_name, "John")

    def test_member_str(self):
        self.assertEqual(str(self.member), "John Doe")

    def test_member_type(self):
        self.assertEqual(self.member.member_type, "student")


class TestBorrowingModel(TestCase):

    def setUp(self):
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
        self.borrowing = Borrowing.objects.create(
            book_id=self.book,
            member_id=self.member,
            borrow_date=timezone.now().date(),
            due_date=timezone.now().date() + timezone.timedelta(days=14),
        )

    def test_borrowing_created_successfully(self):
        self.assertIsNotNone(self.borrowing.borrowing_id)

    def test_borrowing_str(self):
        self.assertEqual(str(self.borrowing), f"Borrowing #{self.borrowing.borrowing_id}")

    def test_is_overdue_false(self):
        self.assertFalse(self.borrowing.is_overdue())

    def test_calculate_late_fee_no_late(self):
        self.borrowing.return_date = self.borrowing.due_date
        self.assertEqual(self.borrowing.calculate_late_fee(), 0)

    def test_calculate_late_fee_with_late(self):
        self.borrowing.return_date = self.borrowing.due_date + timezone.timedelta(days=3)
        self.assertEqual(self.borrowing.calculate_late_fee(), 15)


class TestCategoryModel(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Fantasy",
            description="Fantasy literature category",
        )

    def test_category_created_successfully(self):
        self.assertEqual(self.category.name, "Fantasy")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Fantasy")

    def test_category_description(self):
        self.assertEqual(self.category.description, "Fantasy literature category")


class TestReviewModel(TestCase):

    def setUp(self):
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
        self.review = Review.objects.create(
            book_id=self.book,
            member_id=self.member,
            rating=5,
            comment="Excellent book!",
        )

    def test_review_created_successfully(self):
        self.assertIsNotNone(self.review.review_id)

    def test_review_rating(self):
        self.assertEqual(self.review.rating, 5)

    def test_review_str(self):
        self.assertEqual(str(self.review), f"Review #{self.review.review_id}")

    def test_review_comment(self):
        self.assertEqual(self.review.comment, "Excellent book!")