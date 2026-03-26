from django.test import TestCase
from lms_data.models import Library, Author, Category, Book, Member, Borrowing, Review


class TestFixtures(TestCase):

    fixtures = ["initial_data.json"]

    def test_libraries_loaded(self):
        self.assertEqual(Library.objects.count(), 2)

    def test_authors_loaded(self):
        self.assertEqual(Author.objects.count(), 2)

    def test_categories_loaded(self):
        self.assertEqual(Category.objects.count(), 2)

    def test_books_loaded(self):
        self.assertEqual(Book.objects.count(), 2)

    def test_members_loaded(self):
        self.assertEqual(Member.objects.count(), 2)

    def test_borrowings_loaded(self):
        self.assertEqual(Borrowing.objects.count(), 1)

    def test_reviews_loaded(self):
        self.assertEqual(Review.objects.count(), 1)

    def test_library_data_correct(self):
        library = Library.objects.get(pk=1)
        self.assertEqual(library.name, "Central Library")
        self.assertEqual(library.campus_location, "Main Campus")

    def test_author_data_correct(self):
        author = Author.objects.get(pk=1)
        self.assertEqual(author.first_name, "J.K.")
        self.assertEqual(author.last_name, "Rowling")

    def test_book_linked_to_library(self):
        book = Book.objects.get(pk=1)
        self.assertEqual(book.library_id.library_id, 1)

    def test_book_linked_to_author(self):
        book = Book.objects.get(pk=1)
        self.assertIn("Rowling", [a.last_name for a in book.authors.all()])

    def test_book_linked_to_category(self):
        book = Book.objects.get(pk=1)
        self.assertIn("Fantasy", [c.name for c in book.categories.all()])

    def test_borrowing_linked_to_member_and_book(self):
        borrowing = Borrowing.objects.get(pk=1)
        self.assertEqual(borrowing.member_id.first_name, "John")
        self.assertEqual(borrowing.book_id.title, "Harry Potter and the Philosopher's Stone")

    def test_review_rating(self):
        review = Review.objects.get(pk=1)
        self.assertEqual(review.rating, 5)