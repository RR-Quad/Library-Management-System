"""
Database models for the Library Management System.

These models define the relational schema used for managing:
- Libraries
- Books
- Authors
- Categories
- Members
- Borrowing transactions
- Book reviews

The system supports many-to-many relationships between books,
authors, and categories via explicit junction tables.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


# =========================================================
# Library Model
# =========================================================

class Library(models.Model):
    """
    Represents a physical library branch within the institution.
    """

    library_id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=30,
        help_text="Name of the library branch."
    )

    campus_location = models.CharField(
        max_length=30,
        help_text="Campus location where the library is situated."
    )

    contact_email = models.EmailField(
        unique=True,
        help_text="Official email address of the library."
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        help_text="Primary contact phone number for the library."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the record was created."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated."
    )

    class Meta:
        db_table = "library"
        ordering = ["name"]

    def __str__(self):
        return self.name


# =========================================================
# Author Model
# =========================================================

class Author(models.Model):
    """
    Represents an author who has written one or more books.
    """

    author_id = models.AutoField(primary_key=True)

    first_name = models.CharField(
        max_length=20,
        help_text="Author's first name."
    )

    last_name = models.CharField(
        max_length=20,
        help_text="Author's last name."
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text="Author's date of birth."
    )

    nationality = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Country of origin or nationality."
    )

    biography = models.TextField(
        null=True,
        blank=True,
        help_text="Short biography describing the author."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "author"
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# =========================================================
# Category Model
# =========================================================

class Category(models.Model):
    """
    Represents a classification used to organize books
    into genres or subject areas.
    """

    category_id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=30,
        unique=True,
        help_text="Name of the category (e.g., Science Fiction, History)."
    )

    description = models.TextField(
        null=True,
        blank=True,
        help_text="Optional description of the category."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category"
        ordering = ["name"]

    def __str__(self):
        return self.name


# =========================================================
# Book Model
# =========================================================

class Book(models.Model):
    """
    Represents a book available in the library collection.
    """

    book_id = models.AutoField(primary_key=True)

    title = models.CharField(
        max_length=50,
        help_text="Title of the book."
    )

    isbn = models.CharField(
        max_length=15,
        unique=True,
        help_text="International Standard Book Number."
    )

    publication_date = models.DateField(
        help_text="Date the book was originally published."
    )

    total_copies = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Total number of copies owned by the library."
    )

    available_copies = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of copies currently available for borrowing."
    )

    library_id = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name="books",
        db_column="library_id",
        help_text="Library branch that owns this book."
    )

    authors = models.ManyToManyField(
        Author,
        through="BookAuthor",
        related_name="books",
        help_text="Authors who wrote the book."
    )

    categories = models.ManyToManyField(
        Category,
        through="BookCategory",
        related_name="books",
        help_text="Categories that describe this book."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "book"
        ordering = ["title"]

    def clean(self):
        """
        Ensures available copies never exceed total copies.
        """
        if self.available_copies > self.total_copies:
            raise ValidationError(
                "Available copies cannot exceed total copies."
            )

    @property
    def is_available(self):
        """
        Returns True if at least one copy of the book is available.
        """
        return self.available_copies > 0

    def __str__(self):
        return self.title


# =========================================================
# Member Model
# =========================================================

class Member(models.Model):
    """
    Represents a registered library member who can borrow books.
    """

    MEMBER_TYPES = [
        ("student", "Student"),
        ("faculty", "Faculty"),
    ]

    member_id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    contact_email = models.EmailField(
        unique=True,
        help_text="Member's primary email address."
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        help_text="Member's contact phone number."
    )

    member_type = models.CharField(
        max_length=20,
        choices=MEMBER_TYPES,
        help_text="Type of library membership."
    )

    registration_date = models.DateField(
        default=timezone.now,
        help_text="Date when the member registered."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "member"
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# =========================================================
# Borrowing Model
# =========================================================

class Borrowing(models.Model):
    """
    Represents a borrowing transaction between a member and a book.
    """

    borrowing_id = models.AutoField(primary_key=True)

    member_id = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="borrowings",
        db_column="member_id",
        help_text="Member who borrowed the book."
    )

    book_id = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings",
        db_column="book_id",
        help_text="Book being borrowed."
    )

    borrow_date = models.DateField(
        default=timezone.now,
        help_text="Date when the book was borrowed."
    )

    due_date = models.DateField(
        help_text="Date when the book must be returned."
    )

    return_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when the book was returned."
    )

    late_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Late fee charged for overdue returns."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "borrowing"
        ordering = ["-borrow_date"]

    def clean(self):
        if self.due_date < self.borrow_date:
            raise ValidationError(
                "Due date cannot be earlier than borrow date."
            )

    def is_overdue(self):
        """
        Returns True if the borrowing is overdue.
        """
        if self.return_date is None:
            return timezone.now().date() > self.due_date
        return False

    def __str__(self):
        return f"{self.member_id} borrowed {self.book_id}"


# =========================================================
# Review Model
# =========================================================

class Review(models.Model):
    """
    Represents a rating and optional comment submitted
    by a member for a specific book.
    """

    review_id = models.AutoField(primary_key=True)

    member_id = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_column="member_id"
    )

    book_id = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_column="book_id"
    )

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        help_text="Rating between 1 (lowest) and 5 (highest)."
    )

    comment = models.TextField(
        null=True,
        blank=True,
        help_text="Optional written review."
    )

    review_date = models.DateField(
        default=timezone.now,
        help_text="Date the review was submitted."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "review"
        unique_together = ("member_id", "book_id")

    def __str__(self):
        return f"{self.member_id} review for {self.book_id}"


# =========================================================
# Junction Tables
# =========================================================

class BookAuthor(models.Model):
    """
    Junction table linking books and authors.
    """

    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "book_author"
        unique_together = ("book_id", "author_id")


class BookCategory(models.Model):
    """
    Junction table linking books and categories.
    """

    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "book_category"
        unique_together = ("book_id", "category_id")