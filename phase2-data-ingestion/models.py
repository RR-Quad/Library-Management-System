## Imports


from sqlalchemy import (Column, Integer, String, Date, Text, ForeignKey, CheckConstraint, UniqueConstraint, DECIMAL, Index)
from sqlalchemy.orm import relationship, declarative_base


## Object Instantiation


Base = declarative_base()


## Classes


class Library(Base):
    __tablename__ = "library"

    library_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    campus_location = Column(String(30), nullable=False)
    contact_email = Column(String(50), nullable=False, unique=True)
    phone_number = Column(String(10), nullable=False, unique=True)

    # Relationships
    books = relationship(
        "Book",
        back_populates="library",
        cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = "book"

    book_id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    isbn = Column(String(15), nullable=False, unique=True)
    publication_date = Column(Date)
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)
    library_id = Column(
        Integer,
        ForeignKey("library.library_id", ondelete="CASCADE"),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint("total_copies >= 0", name="chk_total_copies"),
        CheckConstraint("available_copies >= 0", name="chk_available_copies_non_negative"),
        CheckConstraint("available_copies <= total_copies", name="chk_available_copies"),
        Index("idx_book_library_id", "library_id"),
    )

    # Relationships
    library = relationship("Library", back_populates="books")

    authors = relationship(
        "Author",
        secondary="book_author",
        back_populates="books"
    )

    categories = relationship(
        "Category",
        secondary="book_category",
        back_populates="books"
    )

    borrowings = relationship(
        "Borrowing",
        back_populates="book",
        cascade="all, delete-orphan"
    )

    reviews = relationship(
        "Review",
        back_populates="book",
        cascade="all, delete-orphan"
    )


class Author(Base):
    __tablename__ = "author"

    author_id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    birth_date = Column(Date)
    nationality = Column(String(20))
    biography = Column(Text)

    __table_args__ = (
        UniqueConstraint(
            "first_name",
            "last_name",
            "birth_date",
            name="uq_author_identity"
        ),
    )

    books = relationship(
        "Book",
        secondary="book_author",
        back_populates="authors"
    )


class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    description = Column(Text)

    books = relationship(
        "Book",
        secondary="book_category",
        back_populates="categories"
    )


class Member(Base):
    __tablename__ = "member"

    member_id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    contact_email = Column(String(50), nullable=False, unique=True)
    phone_number = Column(String(10), nullable=False, unique=True)
    member_type = Column(String(20), nullable=False)
    registration_date = Column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "member_type IN ('student', 'faculty')",
            name="chk_member_type"
        ),
    )

    borrowings = relationship(
        "Borrowing",
        back_populates="member",
        cascade="all, delete-orphan"
    )

    reviews = relationship(
        "Review",
        back_populates="member",
        cascade="all, delete-orphan"
    )


class Borrowing(Base):
    __tablename__ = "borrowing"

    borrowing_id = Column(Integer, primary_key=True)
    member_id = Column(
        Integer,
        ForeignKey("member.member_id", ondelete="CASCADE"),
        nullable=False
    )
    book_id = Column(
        Integer,
        ForeignKey("book.book_id", ondelete="CASCADE"),
        nullable=False
    )
    borrow_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    late_fee = Column(DECIMAL(10, 2))

    __table_args__ = (
        CheckConstraint("late_fee >= 0", name="chk_late_fee"),
        CheckConstraint("due_date >= borrow_date", name="chk_borrow_dates"),
        Index("idx_borrowing_book_id", "book_id"),
        Index("idx_borrowing_member_id", "member_id"),
        Index("idx_borrowing_borrow_date", "borrow_date"),
        Index("idx_borrowing_due_date", "due_date"),
    )

    member = relationship("Member", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")


class Review(Base):
    __tablename__ = "review"

    review_id = Column(Integer, primary_key=True)
    member_id = Column(
        Integer,
        ForeignKey("member.member_id", ondelete="CASCADE"),
        nullable=False
    )
    book_id = Column(
        Integer,
        ForeignKey("book.book_id", ondelete="CASCADE"),
        nullable=False
    )
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    review_date = Column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5", name="chk_rating"),
        UniqueConstraint("member_id", "book_id", name="uq_member_book_review"),
        Index("idx_review_book_id", "book_id"),
        Index("idx_review_member_id", "member_id"),
    )

    member = relationship("Member", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")


class BookAuthor(Base):
    __tablename__ = "book_author"

    book_id = Column(
        Integer,
        ForeignKey("book.book_id", ondelete="CASCADE"),
        primary_key=True
    )
    author_id = Column(
        Integer,
        ForeignKey("author.author_id", ondelete="CASCADE"),
        primary_key=True
    )

    __table_args__ = (
        Index("idx_book_author_author_id", "author_id"),
    )


class BookCategory(Base):
    __tablename__ = "book_category"

    book_id = Column(
        Integer,
        ForeignKey("book.book_id", ondelete="CASCADE"),
        primary_key=True
    )
    category_id = Column(
        Integer,
        ForeignKey("category.category_id", ondelete="CASCADE"),
        primary_key=True
    )

    __table_args__ = (
        Index("idx_book_category_category_id", "category_id"),
    )


## End