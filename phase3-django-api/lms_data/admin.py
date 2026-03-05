from django.contrib import admin
from .models import (
    Library, Book, Author, Category,
    Member, Borrowing, Review,
    BookCategory, BookAuthor
)

admin.site.register(Library)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Member)
admin.site.register(Borrowing)
admin.site.register(Review)
admin.site.register(BookAuthor)
admin.site.register(BookCategory)
