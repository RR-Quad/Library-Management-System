import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from lms_data.models import (
    Library,
    Author,
    Category,
    Book,
    Member,
    Borrowing,
    Review,
)


class LibraryFactory(DjangoModelFactory):

    class Meta:
        model = Library

    name = factory.Sequence(lambda n: f"Library {n}")
    campus_location = factory.Sequence(lambda n: f"Campus {n}")
    contact_email = factory.Sequence(lambda n: f"library{n}@university.edu")
    phone_number = factory.Sequence(lambda n: f"+123456789{n}")


class AuthorFactory(DjangoModelFactory):

    class Meta:
        model = Author

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    nationality = factory.Faker("country")
    biography = factory.Faker("text")


class CategoryFactory(DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker("sentence")


class BookFactory(DjangoModelFactory):

    class Meta:
        model = Book

    title = factory.Sequence(lambda n: f"Book {n}")
    isbn = factory.Sequence(lambda n: f"978000000{n:04d}")
    publication_date = factory.Faker("date")
    total_copies = factory.Faker("random_int", min=5, max=20)
    available_copies = factory.LazyAttribute(lambda o: o.total_copies - 1)
    library_id = factory.SubFactory(LibraryFactory)


class MemberFactory(DjangoModelFactory):

    class Meta:
        model = Member

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    contact_email = factory.Sequence(lambda n: f"member{n}@email.com")
    phone_number = factory.Sequence(lambda n: f"+987654321{n}")
    member_type = factory.Iterator(["student", "faculty"])
    registration_date = factory.LazyFunction(timezone.now().date)


class BorrowingFactory(DjangoModelFactory):

    class Meta:
        model = Borrowing

    member_id = factory.SubFactory(MemberFactory)
    book_id = factory.SubFactory(BookFactory)
    borrow_date = factory.LazyFunction(timezone.now().date)
    due_date = factory.LazyAttribute(
        lambda o: o.borrow_date + timezone.timedelta(days=14)
    )


class ReviewFactory(DjangoModelFactory):

    class Meta:
        model = Review

    member_id = factory.SubFactory(MemberFactory)
    book_id = factory.SubFactory(BookFactory)
    rating = factory.Faker("random_int", min=1, max=5)
    comment = factory.Faker("sentence")
    review_date = factory.LazyFunction(timezone.now().date)