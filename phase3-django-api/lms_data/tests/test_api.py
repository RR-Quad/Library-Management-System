from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
from lms_data.models import Library, Author, Category, Book, Member, Borrowing, Review


class TestLibraryAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.library = Library.objects.create(
            name="Central Library",
            campus_location="Main Campus",
            contact_email="library@university.edu",
            phone_number="+1234567890",
        )

    def test_list_libraries(self):
        response = self.client.get("/api/libraries/")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_library(self):
        response = self.client.get(f"/api/libraries/{self.library.library_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Central Library")

    def test_create_library(self):
        data = {
            "name": "Science Library",
            "campus_location": "Science Campus",
            "contact_email": "science@university.edu",
            "phone_number": "+9876543210",
        }
        response = self.client.post("/api/libraries/", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_library(self):
        data = {
            "name": "Updated Library",
            "campus_location": "Main Campus",
            "contact_email": "library@university.edu",
            "phone_number": "+1234567890",
        }
        response = self.client.put(f"/api/libraries/{self.library.library_id}/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Updated Library")

    def test_delete_library(self):
        response = self.client.delete(f"/api/libraries/{self.library.library_id}/")
        self.assertEqual(response.status_code, 204)

    def test_retrieve_nonexistent_library(self):
        response = self.client.get("/api/libraries/9999/")
        self.assertEqual(response.status_code, 404)

    def test_partial_update_library(self):
        response = self.client.patch(f"/api/libraries/{self.library.library_id}/", {
            "name": "Patched Library"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Patched Library")

    def test_create_library_missing_email(self):
        data = {
            "name": "Science Library",
            "campus_location": "Science Campus",
            "phone_number": "+9876543210",
        }
        response = self.client.post("/api/libraries/", data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_library_duplicate_email(self):
        data = {
            "name": "Another Library",
            "campus_location": "Another Campus",
            "contact_email": "library@university.edu",
            "phone_number": "+9876543210",
        }
        response = self.client.post("/api/libraries/", data, format="json")
        self.assertEqual(response.status_code, 400)


class TestAuthorAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            first_name="J.K.",
            last_name="Rowling",
            nationality="British",
        )

    def test_list_authors(self):
        response = self.client.get("/api/authors/")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_author(self):
        response = self.client.get(f"/api/authors/{self.author.author_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "J.K.")

    def test_create_author(self):
        data = {
            "first_name": "George",
            "last_name": "Orwell",
            "nationality": "British",
        }
        response = self.client.post("/api/authors/", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_author(self):
        data = {
            "first_name": "Joanne",
            "last_name": "Rowling",
            "nationality": "British",
        }
        response = self.client.put(f"/api/authors/{self.author.author_id}/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "Joanne")

    def test_delete_author(self):
        response = self.client.delete(f"/api/authors/{self.author.author_id}/")
        self.assertEqual(response.status_code, 204)

    def test_retrieve_nonexistent_author(self):
        response = self.client.get("/api/authors/9999/")
        self.assertEqual(response.status_code, 404)

    def test_partial_update_author(self):
        response = self.client.patch(f"/api/authors/{self.author.author_id}/", {
            "nationality": "American"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["nationality"], "American")

    def test_create_author_missing_first_name(self):
        response = self.client.post("/api/authors/", {
            "last_name": "Orwell"
        }, format="json")
        self.assertEqual(response.status_code, 400)


class TestCategoryAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Fantasy",
            description="Fantasy literature",
        )

    def test_list_categories(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_category(self):
        response = self.client.get(f"/api/categories/{self.category.category_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Fantasy")

    def test_create_category(self):
        data = {
            "name": "Science Fiction",
            "description": "Sci-fi literature",
        }
        response = self.client.post("/api/categories/", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_delete_category(self):
        response = self.client.delete(f"/api/categories/{self.category.category_id}/")
        self.assertEqual(response.status_code, 204)

    def test_update_category(self):
        response = self.client.put(f"/api/categories/{self.category.category_id}/", {
            "name": "Updated Fantasy",
            "description": "Updated description",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Updated Fantasy")

    def test_partial_update_category(self):
        response = self.client.patch(f"/api/categories/{self.category.category_id}/", {
            "name": "Patched Fantasy"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Patched Fantasy")

    def test_retrieve_nonexistent_category(self):
        response = self.client.get("/api/categories/9999/")
        self.assertEqual(response.status_code, 404)

    def test_create_duplicate_category(self):
        response = self.client.post("/api/categories/", {
            "name": "Fantasy",
        }, format="json")
        self.assertEqual(response.status_code, 400)


class TestBookAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
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

    def test_list_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_book(self):
        response = self.client.get(f"/api/books/{self.book.book_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Harry Potter")

    def test_book_availability(self):
        response = self.client.get(f"/api/books/{self.book.book_id}/availability/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["availability"]["available"], 7)

    def test_borrow_book(self):
        response = self.client.post("/api/books/borrow/", {
            "book_id": self.book.book_id,
            "member_id": self.member.member_id,
        }, format="json")
        self.assertEqual(response.status_code, 201)

    def test_borrow_unavailable_book(self):
        self.book.available_copies = 0
        self.book.save()
        response = self.client.post("/api/books/borrow/", {
            "book_id": self.book.book_id,
            "member_id": self.member.member_id,
        }, format="json")
        self.assertEqual(response.status_code, 400)

    def test_return_book(self):
        borrowing = Borrowing.objects.create(
            book_id=self.book,
            member_id=self.member,
            borrow_date=timezone.now().date(),
            due_date=timezone.now().date() + timezone.timedelta(days=14),
        )
        response = self.client.post("/api/books/return/", {
            "borrowing_id": borrowing.borrowing_id,
        }, format="json")
        self.assertEqual(response.status_code, 200)

    def test_return_already_returned_book(self):
        borrowing = Borrowing.objects.create(
            book_id=self.book,
            member_id=self.member,
            borrow_date=timezone.now().date(),
            due_date=timezone.now().date() + timezone.timedelta(days=14),
            return_date=timezone.now().date(),
        )
        response = self.client.post("/api/books/return/", {
            "borrowing_id": borrowing.borrowing_id,
        }, format="json")
        self.assertEqual(response.status_code, 400)

    def test_search_books(self):
        response = self.client.post("/api/books/search/", {
            "library_id": self.library.library_id,
        }, format="json")
        self.assertEqual(response.status_code, 200)

    def test_recommendations(self):
        response = self.client.get("/api/books/recommendations/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("most_borrowed_books", response.data)
        self.assertIn("top_rated_books", response.data)


class TestMemberAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.member = Member.objects.create(
            first_name="John",
            last_name="Doe",
            contact_email="john@email.com",
            phone_number="+1234567890",
            member_type="student",
        )

    def test_list_members(self):
        response = self.client.get("/api/members/")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_member(self):
        response = self.client.get(f"/api/members/{self.member.member_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "John")

    def test_create_member(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "contact_email": "jane@email.com",
            "phone_number": "+0987654321",
            "member_type": "faculty",
        }
        response = self.client.post("/api/members/", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_delete_member(self):
        response = self.client.delete(f"/api/members/{self.member.member_id}/")
        self.assertEqual(response.status_code, 204)

    def test_member_borrowing_history(self):
        response = self.client.get(f"/api/members/{self.member.member_id}/borrowings/")
        self.assertEqual(response.status_code, 200)


class TestStatisticsAPI(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_statistics(self):
        response = self.client.get("/api/statistics/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_books", response.data)
        self.assertIn("total_members", response.data)
        self.assertIn("total_borrowings", response.data)

class TestReviewAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
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

    def test_list_reviews(self):
        response = self.client.get("/api/reviews/")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_review(self):
        response = self.client.get(f"/api/reviews/{self.review.review_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["rating"], 5)

    def test_create_review(self):
        member2 = Member.objects.create(
            first_name="Jane",
            last_name="Doe",
            contact_email="jane@email.com",
            phone_number="+0987654321",
            member_type="faculty",
        )
        data = {
            "member_id": f"http://testserver/api/members/{member2.member_id}/",
            "book_id": f"http://testserver/api/books/{self.book.book_id}/",
            "rating": 4,
            "comment": "Great book!",
        }
        response = self.client.post("/api/reviews/", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_review(self):
        data = {
            "member_id": f"http://testserver/api/members/{self.member.member_id}/",
            "book_id": f"http://testserver/api/books/{self.book.book_id}/",
            "rating": 3,
            "comment": "Good book!",
        }
        response = self.client.put(f"/api/reviews/{self.review.review_id}/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["rating"], 3)

    def test_delete_review(self):
        response = self.client.delete(f"/api/reviews/{self.review.review_id}/")
        self.assertEqual(response.status_code, 204)

    def test_duplicate_review(self):
        data = {
            "member_id": f"http://testserver/api/members/{self.member.member_id}/",
            "book_id": f"http://testserver/api/books/{self.book.book_id}/",
            "rating": 4,
            "comment": "Another review!",
        }
        response = self.client.post("/api/reviews/", data, format="json")
        self.assertEqual(response.status_code, 400)