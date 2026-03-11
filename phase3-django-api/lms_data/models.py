from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# =========================================================
# Base Model (Reusable timestamps)
# =========================================================

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# =========================================================
# Library
# =========================================================

class Library(TimeStampedModel):
    library_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=30)
    campus_location = models.CharField(max_length=30)

    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = "library"
        ordering = ["library_id"]
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
    author_id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=20, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "author"
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["last_name"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# =========================================================
# Category
# =========================================================

class Category(TimeStampedModel):
    category_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "category"
        ordering = ["name"]

    def __str__(self):
        return self.name


# =========================================================
# Book
# =========================================================

class Book(TimeStampedModel):
    book_id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=50)
    isbn = models.CharField(max_length=15, unique=True)

    publication_date = models.DateField()

    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()

    library_id = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name="books",
        db_column="library_id",
    )

    authors = models.ManyToManyField(
        Author,
        through="BookAuthor",
        related_name="books",
    )

    categories = models.ManyToManyField(
        Category,
        through="BookCategory",
        related_name="books",
    )

    class Meta:
        db_table = "book"
        ordering = ["book_id"]
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
        return self.available_copies > 0

    def __str__(self):
        return self.title


# =========================================================
# Member
# =========================================================

class Member(TimeStampedModel):

    class MemberType(models.TextChoices):
        STUDENT = "student", "Student"
        FACULTY = "faculty", "Faculty"

    member_id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

    member_type = models.CharField(
        max_length=20,
        choices=MemberType.choices
    )

    registration_date = models.DateField(default=timezone.now)

    class Meta:
        db_table = "member"
        ordering = ["member_id"]
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

    borrowing_id = models.AutoField(primary_key=True)

    member_id = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="borrowings",
        db_column="member_id",
    )

    book_id = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings",
        db_column="book_id",
    )

    borrow_date = models.DateField(default=timezone.now)
    due_date = models.DateField()

    return_date = models.DateField(null=True, blank=True)

    late_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        db_table = "borrowing"
        ordering = ["-borrowing_id"]
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
        if not self.return_date:
            return timezone.now().date() > self.due_date
        return False

    def calculate_late_fee(self, fee_per_day=5):
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

    review_id = models.AutoField(primary_key=True)

    member_id = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_column="member_id",
    )

    book_id = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_column="book_id",
    )

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comment = models.TextField(blank=True, null=True)
    review_date = models.DateField(default=timezone.now)

    class Meta:
        db_table = "review"
        ordering = ["-review_date"]
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

    book_id = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        db_column="book_id"
    )

    author_id = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        db_column="author_id"
    )

    class Meta:
        db_table = "book_author"
        constraints = [
            models.UniqueConstraint(
                fields=["book_id", "author_id"],
                name="unique_book_author"
            )
        ]


class BookCategory(TimeStampedModel):

    book_id = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        db_column="book_id"
    )

    category_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_column="category_id"
    )

    class Meta:
        db_table = "book_category"
        constraints = [
            models.UniqueConstraint(
                fields=["book_id", "category_id"],
                name="unique_book_category"
            )
        ]