from django.test import TestCase
from lms_data.tests.factories import (
    LibraryFactory,
    AuthorFactory,
    CategoryFactory,
    BookFactory,
    MemberFactory,
    BorrowingFactory,
    ReviewFactory,
)


class TestLibraryFactory(TestCase):

    def test_create_library(self):
        library = LibraryFactory()
        self.assertIsNotNone(library.library_id)
        self.assertIsNotNone(library.name)
        self.assertIsNotNone(library.contact_email)

    def test_create_multiple_libraries(self):
        libraries = LibraryFactory.create_batch(3)
        self.assertEqual(len(libraries), 3)
        emails = [l.contact_email for l in libraries]
        self.assertEqual(len(emails), len(set(emails)))


class TestAuthorFactory(TestCase):

    def test_create_author(self):
        author = AuthorFactory()
        self.assertIsNotNone(author.author_id)
        self.assertIsNotNone(author.first_name)
        self.assertIsNotNone(author.last_name)

    def test_create_multiple_authors(self):
        authors = AuthorFactory.create_batch(5)
        self.assertEqual(len(authors), 5)

    def test_author_has_nationality(self):
        author = AuthorFactory()
        self.assertIsNotNone(author.nationality)

    def test_author_has_biography(self):
        author = AuthorFactory()
        self.assertIsNotNone(author.biography)


class TestCategoryFactory(TestCase):

    def test_create_category(self):
        category = CategoryFactory()
        self.assertIsNotNone(category.category_id)
        self.assertIsNotNone(category.name)

    def test_create_multiple_categories(self):
        categories = CategoryFactory.create_batch(3)
        self.assertEqual(len(categories), 3)
        names = [c.name for c in categories]
        self.assertEqual(len(names), len(set(names)))

    def test_category_has_description(self):
        category = CategoryFactory()
        self.assertIsNotNone(category.description)


class TestBookFactory(TestCase):

    def test_create_book(self):
        book = BookFactory()
        self.assertIsNotNone(book.book_id)
        self.assertIsNotNone(book.title)
        self.assertIsNotNone(book.library_id)

    def test_available_copies_lte_total(self):
        book = BookFactory()
        self.assertLessEqual(book.available_copies, book.total_copies)

    def test_create_multiple_books(self):
        books = BookFactory.create_batch(3)
        self.assertEqual(len(books), 3)

    def test_book_has_isbn(self):
        book = BookFactory()
        self.assertIsNotNone(book.isbn)

    def test_book_has_publication_date(self):
        book = BookFactory()
        self.assertIsNotNone(book.publication_date)

    def test_book_isbn_unique(self):
        books = BookFactory.create_batch(3)
        isbns = [b.isbn for b in books]
        self.assertEqual(len(isbns), len(set(isbns)))


class TestMemberFactory(TestCase):

    def test_create_member(self):
        member = MemberFactory()
        self.assertIsNotNone(member.member_id)
        self.assertIsNotNone(member.first_name)
        self.assertIsNotNone(member.last_name)

    def test_member_type_valid(self):
        member = MemberFactory()
        self.assertIn(member.member_type, ["student", "faculty"])

    def test_create_multiple_members(self):
        members = MemberFactory.create_batch(4)
        self.assertEqual(len(members), 4)

    def test_member_has_email(self):
        member = MemberFactory()
        self.assertIsNotNone(member.contact_email)

    def test_member_email_unique(self):
        members = MemberFactory.create_batch(3)
        emails = [m.contact_email for m in members]
        self.assertEqual(len(emails), len(set(emails)))

    def test_member_has_registration_date(self):
        member = MemberFactory()
        self.assertIsNotNone(member.registration_date)


class TestBorrowingFactory(TestCase):

    def test_create_borrowing(self):
        borrowing = BorrowingFactory()
        self.assertIsNotNone(borrowing.borrowing_id)
        self.assertIsNotNone(borrowing.book_id)
        self.assertIsNotNone(borrowing.member_id)

    def test_due_date_after_borrow_date(self):
        borrowing = BorrowingFactory()
        self.assertGreater(borrowing.due_date, borrowing.borrow_date)

    def test_create_multiple_borrowings(self):
        borrowings = BorrowingFactory.create_batch(3)
        self.assertEqual(len(borrowings), 3)

    def test_borrowing_has_no_return_date_by_default(self):
        borrowing = BorrowingFactory()
        self.assertIsNone(borrowing.return_date)

    def test_borrowing_has_no_late_fee_by_default(self):
        borrowing = BorrowingFactory()
        self.assertIsNone(borrowing.late_fee)


class TestReviewFactory(TestCase):

    def assertBetween(self, value, min_val, max_val):
        self.assertGreaterEqual(value, min_val)
        self.assertLessEqual(value, max_val)

    def test_create_review(self):
        review = ReviewFactory()
        self.assertIsNotNone(review.review_id)
        self.assertIsNotNone(review.member_id)
        self.assertIsNotNone(review.book_id)

    def test_review_rating_in_range(self):
        review = ReviewFactory()
        self.assertBetween(review.rating, 1, 5)

    def test_review_has_comment(self):
        review = ReviewFactory()
        self.assertIsNotNone(review.comment)

    def test_review_has_date(self):
        review = ReviewFactory()
        self.assertIsNotNone(review.review_date)

    def test_create_multiple_reviews(self):
        reviews = [ReviewFactory() for _ in range(3)]
        self.assertEqual(len(reviews), 3)