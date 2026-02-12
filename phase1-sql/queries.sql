-- 1] Books with their authors and categories

SELECT 
    b.book_id,
    b.title AS book_name,
    STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') AS authors,
    STRING_AGG(DISTINCT c.name, ', ') AS categories,
    l.name AS library
FROM book b
JOIN library l ON b.library_id = l.library_id
LEFT JOIN book_author ba ON b.book_id = ba.book_id
LEFT JOIN author a ON ba.author_id = a.author_id
LEFT JOIN book_category bc ON b.book_id = bc.book_id
LEFT JOIN category c ON bc.category_id = c.category_id
GROUP BY b.book_id, b.title, l.name
ORDER BY b.book_id;

-- 2] Most borrowed books in the last 36 days

SELECT 
    b.book_id,
    b.title,
    COUNT(br.borrowing_id) AS total_borrowed
FROM borrowing br
JOIN book b ON b.book_id = br.book_id
WHERE br.borrow_date >= CURRENT_DATE - INTERVAL '36 days'
GROUP BY b.book_id, b.title
ORDER BY total_borrowed DESC, b.book_id ASC;

-- 3] Members with overdue books and calculated late fees

WITH overdue AS (
    SELECT 
        br.member_id,
        m.first_name,
        m.last_name,
        br.borrowing_id,
        br.due_date,
        br.return_date,
        CASE 
            WHEN br.return_date > br.due_date
                THEN br.return_date - br.due_date
            WHEN br.return_date IS NULL 
                 AND CURRENT_DATE > br.due_date
                THEN CURRENT_DATE - br.due_date
        END AS excess_days
    FROM borrowing br
    JOIN member m ON br.member_id = m.member_id
    WHERE br.return_date > br.due_date
       OR (br.return_date IS NULL AND CURRENT_DATE > br.due_date)
)

SELECT 
    *,
    excess_days * 1 AS late_charges
FROM overdue
ORDER BY excess_days DESC;

-- 4] Average rating per book with author information

SELECT 
    b.book_id,
    b.title,
    STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') AS authors,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM book b
LEFT JOIN review r ON b.book_id = r.book_id
LEFT JOIN book_author ba ON b.book_id = ba.book_id
LEFT JOIN author a ON ba.author_id = a.author_id
GROUP BY b.book_id, b.title
ORDER BY b.book_id;

-- 5] Books available in each library with stock levels

SELECT 
    l.library_id,
    l.name AS library_name,
    b.book_id,
    b.title,
    b.total_copies,
    b.available_copies,
    (b.total_copies - b.available_copies) AS borrowed_copies
FROM library l
JOIN book b ON b.library_id = l.library_id
ORDER BY l.library_id, b.book_id;

-- 6] WINDOW FUNCTION: For each borrowing row, count how many borrowings exist for the same book

SELECT 
    borrowing_id,
    book_id,
    COUNT(*) OVER (PARTITION BY book_id) AS total_borrowings_for_book
FROM borrowing
ORDER BY borrowing_id;

-- 7] TRANSACTION MANAGEMENT: Borrowing a book safely

BEGIN;

UPDATE book
SET available_copies = available_copies - 1
WHERE book_id = 1 AND available_copies > 0;

INSERT INTO borrowing (
    member_id,
    book_id,
    borrow_date,
    due_date
)
VALUES (
    8,
    1,
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '14 days'
);

COMMIT;


