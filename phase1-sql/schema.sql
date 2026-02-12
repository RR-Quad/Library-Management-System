-- ---------- Library ----------
CREATE TABLE library (
    library_id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    campus_location VARCHAR(30) NOT NULL,
    contact_email VARCHAR(50) UNIQUE NOT NULL,
    phone_number VARCHAR(10) UNIQUE NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------- Book ----------
CREATE TABLE book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    isbn VARCHAR(15) UNIQUE NOT NULL,
    publication_date DATE,
    total_copies INTEGER NOT NULL CHECK (total_copies >= 0),
    available_copies INTEGER NOT NULL CHECK (available_copies >= 0),
    library_id INTEGER NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_book_library
        FOREIGN KEY (library_id)
        REFERENCES library (library_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_available_copies
        CHECK (available_copies <= total_copies)
);

CREATE INDEX idx_book_library_id ON book(library_id);

-- ---------- Author ----------
CREATE TABLE author (
    author_id SERIAL PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    birth_date DATE,
    nationality VARCHAR(20),
    biography TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------- Category ----------
CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL,
    description TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------- Member ----------
CREATE TABLE member (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(10) UNIQUE NOT NULL,
    member_type VARCHAR(20) NOT NULL,
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_member_type
        CHECK (member_type IN ('student', 'faculty'))
);

-- ---------- Borrowing ----------
CREATE TABLE borrowing (
    borrowing_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    borrow_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    late_fee DECIMAL(10,2) DEFAULT NULL CHECK (late_fee >= 0),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_borrowing_member
        FOREIGN KEY (member_id)
        REFERENCES member (member_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_borrowing_book
        FOREIGN KEY (book_id)
        REFERENCES book (book_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_borrow_dates
        CHECK (due_date >= borrow_date)
);

CREATE INDEX idx_borrowing_book_id ON borrowing(book_id);
CREATE INDEX idx_borrowing_member_id ON borrowing(member_id);
CREATE INDEX idx_borrowing_borrow_date ON borrowing(borrow_date);
CREATE INDEX idx_borrowing_due_date ON borrowing(due_date);

-- ---------- Review ----------
CREATE TABLE review (
    review_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT,
    review_date DATE NOT NULL DEFAULT CURRENT_DATE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_review_member
        FOREIGN KEY (member_id)
        REFERENCES member (member_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_review_book
        FOREIGN KEY (book_id)
        REFERENCES book (book_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_rating
        CHECK (rating BETWEEN 1 AND 5),

    CONSTRAINT uq_member_book_review
        UNIQUE (member_id, book_id)
);

CREATE INDEX idx_review_book_id ON review(book_id);
CREATE INDEX idx_review_member_id ON review(member_id);

-- ---------- BookAuthor (Many-to-Many) ----------
CREATE TABLE book_author (
    book_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (book_id, author_id),

    CONSTRAINT fk_bookauthor_book
        FOREIGN KEY (book_id)
        REFERENCES book (book_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_bookauthor_author
        FOREIGN KEY (author_id)
        REFERENCES author (author_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_book_author_author_id ON book_author(author_id);

-- ---------- BookCategory (Many-to-Many) ----------
CREATE TABLE book_category (
    book_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (book_id, category_id),

    CONSTRAINT fk_bookcategory_book
        FOREIGN KEY (book_id)
        REFERENCES book (book_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_bookcategory_category
        FOREIGN KEY (category_id)
        REFERENCES category (category_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_book_category_category_id ON book_category(category_id);

-- Trigger Function for updated_at

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach Triggers to All Tables

-- Library
CREATE TRIGGER trg_update_library
BEFORE UPDATE ON library
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Book
CREATE TRIGGER trg_update_book
BEFORE UPDATE ON book
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Author
CREATE TRIGGER trg_update_author
BEFORE UPDATE ON author
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Category
CREATE TRIGGER trg_update_category
BEFORE UPDATE ON category
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Member
CREATE TRIGGER trg_update_member
BEFORE UPDATE ON member
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Borrowing
CREATE TRIGGER trg_update_borrowing
BEFORE UPDATE ON borrowing
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Review
CREATE TRIGGER trg_update_review
BEFORE UPDATE ON review
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- BookAuthor (junction)
CREATE TRIGGER trg_update_book_author
BEFORE UPDATE ON book_author
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- BookCategory (junction)
CREATE TRIGGER trg_update_book_category
BEFORE UPDATE ON book_category
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
