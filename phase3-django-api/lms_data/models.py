## Imports


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


## Model Classes


# ---------- Library ----------

class Library(models.Model):

    library_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    campus_location = models.CharField(max_length=30)
    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "library"

    def __str__(self):
        return self.name


# ---------- Author ----------

class Author(models.Model):

    author_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=20, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "author"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ---------- Category ----------

class Category(models.Model):

    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


# ---------- Book ----------

class Book(models.Model):

    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    isbn = models.CharField(max_length=15, unique=True)
    publication_date = models.DateField()
    total_copies = models.IntegerField(validators=[MinValueValidator(0)])
    available_copies = models.IntegerField(validators=[MinValueValidator(0)])

    library_id = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name="books",
        db_column="library_id"
    )

    authors = models.ManyToManyField(
        Author,
        through="BookAuthor",
        related_name="books"
    )

    categories = models.ManyToManyField(
        Category,
        through="BookCategory",
        related_name="books"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "book"

    def clean(self):
        if self.available_copies > self.total_copies:
            raise ValidationError(
                "Available copies cannot exceed total copies."
            )

    @property
    def is_available(self):
        return self.available_copies > 0

    def __str__(self):
        return self.title


# ---------- Member ----------

class Member(models.Model):

    MEMBER_TYPES = [
        ("student", "Student"),
        ("faculty", "Faculty"),
    ]

    member_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    member_type = models.CharField(
        max_length=20,
        choices=MEMBER_TYPES
    )
    registration_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "member"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ---------- Borrowing ----------

class Borrowing(models.Model):

    borrowing_id = models.AutoField(primary_key=True)

    member_id = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="borrowings",
        db_column="member_id"
    )

    book_id = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings",
        db_column="book_id"
    )

    borrow_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    late_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "borrowing"

    def clean(self):
        if self.due_date < self.borrow_date:
            raise ValidationError(
                "Due date cannot be earlier than borrow date."
            )

    def is_overdue(self):
        if self.return_date is None:
            return timezone.now().date() > self.due_date
        return False

    def __str__(self):
        return f"{self.member_id} borrowed {self.book_id}"


# ---------- Review ----------

class Review(models.Model):

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
        ]
    )

    comment = models.TextField(null=True, blank=True)
    review_date = models.DateField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "review"
        unique_together = ("member_id", "book_id")

    def __str__(self):
        return f"{self.member_id} review for {self.book_id}"


# ---------- Junction Tables ----------

class BookAuthor(models.Model):

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "book_author"
        unique_together = ("book_id", "author_id")


class BookCategory(models.Model):

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "book_category"
        unique_together = ("book_id", "category_id")