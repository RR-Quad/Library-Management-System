from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# =========================================================
# Base Model
# =========================================================

class TimeStampedModel(models.Model):
    """
    Abstract base model that provides automatic
    created_at and updated_at timestamp fields.
    """

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp when the record was created."
    )

    updated_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp when the record was last updated."
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# =========================================================
# Library
# =========================================================

class Library(TimeStampedModel):
    """
    Represents a physical university library location.
    """

    library_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for the library."
    )

    name = models.CharField(
        max_length=30,
        help_text="Name of the library."
    )

    campus_location = models.CharField(
        max_length=30,
        help_text="Campus location where the library is situated."
    )

    contact_email = models.EmailField(
        unique=True,
        help_text="Official contact email for the library."
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        help_text="Contact phone number for the library."
    )

    class Meta:
        db_table = "library"
        ordering = ["library_id"]
        verbose_name = "Library"
        verbose_name_plural = "Libraries"

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["campus_location"]),
        ]

    def __str__(self):
        return self.name


# =========================================================
# Author
# =========================================================

class Author(TimeStampedModel):
    """
    Represents a book author.
    """

    author_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for the author."
    )

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
        blank=True,
        null=True,
        help_text="Author's nationality."
    )

    biography = models.TextField(
        blank=True,
        null=True,
        help_text="Short biography of the author."
    )

    class Meta:
        db_table = "author"
        ordering = ["last_name", "first_name"]
        verbose_name = "Author"
        verbose_name_plural = "Authors"

        indexes = [
            models.Index(fields=["last_name"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# =========================================================
# Category
# =========================================================

class Category(TimeStampedModel):
    """
    Represents a book category or genre.
    """

    category_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for the category."
    )

    name = models.CharField(
        max_length=30,
        unique=True,
        help_text="Category or genre name."
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description of the category."
    )

    class Meta:
        db_table = "category"
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# =========================================================
# Book
# =========================================================

class Book(TimeStampedModel):
    """
    Represents a book available in a library.
    """

    book_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for the book."
    )

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

    total_copies = models.PositiveIntegerField(
        help_text="Total number of copies owned by the library."
    )

    available_copies = models.PositiveIntegerField(
        help_text="Number of copies currently available for borrowing."
    )

    library_id = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name="books",
        db_column="library_id",
        help_text="Library where this book is located."
    )

    authors = models.ManyToManyField(
        "Author",
        through="BookAuthor",
        related_name="books",
        help_text="Authors who wrote the book."
    )

    categories = models.ManyToManyField(
        "Category",
        through="BookCategory",
        related_name="books",
        help_text="Categories associated with the book."
    )

    class Meta:
        db_table = "book"
        ordering = ["book_id"]
        verbose_name = "Book"
        verbose_name_plural = "Books"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(available_copies__lte=models.F("total_copies")),
                name="available_copies_lte_total_copies"
            )
        ]

        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["isbn"]),
        ]

    def is_available(self):
        """Return True if the book has available copies."""
        return self.available_copies > 0

    def __str__(self):
        return self.title


# =========================================================
# Member
# =========================================================

class Member(TimeStampedModel):
    """
    Represents a registered library member.
    """

    class MemberType(models.TextChoices):
        STUDENT = "student", "Student"
        FACULTY = "faculty", "Faculty"

    member_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for the member."
    )

    first_name = models.CharField(
        max_length=20,
        help_text="Member's first name."
    )

    last_name = models.CharField(
        max_length=20,
        help_text="Member's last name."
    )

    contact_email = models.EmailField(
        unique=True,
        help_text="Member email address."
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        help_text="Member contact phone number."
    )

    member_type = models.CharField(
        max_length=20,
        choices=MemberType.choices,
        help_text="Type of member (Student or Faculty)."
    )

    registration_date = models.DateField(
        default=timezone.now().date,
        help_text="Date the member registered with the library."
    )

    class Meta:
        db_table = "member"
        ordering = ["member_id"]
        verbose_name = "Member"
        verbose_name_plural = "Members"

        indexes = [
            models.Index(fields=["last_name"]),
            models.Index(fields=["contact_email"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# =========================================================
# Borrowing
# =========================================================

class Borrowing(TimeStampedModel):
    """
    Represents a book borrowing transaction.
    """

    borrowing_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for the borrowing transaction."
    )

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
        help_text="Book that was borrowed."
    )

    borrow_date = models.DateField(
        default=timezone.now().date,
        help_text="Date when the book was borrowed."
    )

    due_date = models.DateField(
        help_text="Date by which the book must be returned."
    )

    return_date = models.DateField(
        null=True,
        blank=True,
        help_text="Actual return date of the book."
    )

    late_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Late fee charged if returned after due date."
    )

    class Meta:
        db_table = "borrowing"
        ordering = ["-borrowing_id"]
        verbose_name = "Borrowing"
        verbose_name_plural = "Borrowings"

        indexes = [
            models.Index(fields=["borrow_date"]),
            models.Index(fields=["due_date"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(due_date__gte=models.F("borrow_date")),
                name="due_date_after_borrow_date",
            )
        ]

    def is_overdue(self):
        """Check if the borrowing is overdue."""
        if not self.return_date:
            return timezone.now().date() > self.due_date
        return False

    def calculate_late_fee(self, fee_per_day=5):
        """Calculate late fee if book returned late."""
        if self.return_date and self.return_date > self.due_date:
            days = (self.return_date - self.due_date).days
            return days * fee_per_day
        return 0

    def __str__(self):
        return f"Borrowing #{self.borrowing_id}"


# =========================================================
# Review
# =========================================================

class Review(TimeStampedModel):
    """
    Represents a member review for a book.
    """

    review_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for the review."
    )

    member_id = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_column="member_id",
        help_text="Member who wrote the review."
    )

    book_id = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_column="book_id",
        help_text="Book being reviewed."
    )

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating between 1 (lowest) and 5 (highest)."
    )

    comment = models.TextField(
        blank=True,
        null=True,
        help_text="Optional written review."
    )

    review_date = models.DateField(
        default=timezone.now().date,
        help_text="Date the review was submitted."
    )

    class Meta:
        db_table = "review"
        ordering = ["-review_date"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

        constraints = [
            models.UniqueConstraint(
                fields=["member_id", "book_id"],
                name="unique_member_book_review"
            )
        ]

    def __str__(self):
        return f"Review #{self.review_id}"


# =========================================================
# Junction Tables
# =========================================================

class BookAuthor(TimeStampedModel):
    """
    Junction table linking books and authors.
    """

    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, db_column="book_id")
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, db_column="author_id")

    class Meta:
        db_table = "book_author"
        verbose_name = "Book Author"
        verbose_name_plural = "Book Authors"

        constraints = [
            models.UniqueConstraint(
                fields=["book_id", "author_id"],
                name="unique_book_author"
            )
        ]


class BookCategory(TimeStampedModel):
    """
    Junction table linking books and categories.
    """

    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, db_column="book_id")
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, db_column="category_id")

    class Meta:
        db_table = "book_category"
        verbose_name = "Book Category"
        verbose_name_plural = "Book Categories"

        constraints = [
            models.UniqueConstraint(
                fields=["book_id", "category_id"],
                name="unique_book_category"
            )
        ]