-- ---------- LIBRARIES (3) ----------
INSERT INTO library (name, campus_location, contact_email, phone_number) VALUES
('Main Library', 'North Campus', 'main@uni.edu', '555-1001'),
('Science Library', 'Science Block', 'science@uni.edu', '555-1002'),
('Law Library', 'Law Building', 'law@uni.edu', '555-1003');

-- ---------- AUTHORS (8) ----------
INSERT INTO author (first_name, last_name, birth_date, nationality) VALUES
('Alan','Turing','1912-06-23','British'),
('Donald','Knuth','1938-01-10','American'),
('Isaac','Newton','1643-01-04','British'),
('Albert','Einstein','1879-03-14','German'),
('Jane','Austen','1775-12-16','British'),
('Mark','Twain','1835-11-30','American'),
('Oliver','Holmes','1841-03-08','American'),
('Hannah','Arendt','1906-10-14','German');

-- ---------- CATEGORIES (5) ----------
INSERT INTO category (name, description) VALUES
('Computer Science', 'Computing and programming'),
('Mathematics', 'Mathematical theory and applications'),
('Physics', 'Physical sciences'),
('Law', 'Legal systems and studies'),
('Literature', 'Novels and literary works');

-- ---------- MEMBERS (20) ----------
INSERT INTO member (first_name, last_name, contact_email, phone_number, member_type, registration_date) VALUES
('Alice','Brown','alice@uni.edu','555-2001','student','2025-01-15'),
('Bob','Smith','bob@uni.edu','555-2002','student','2025-02-10'),
('Carol','Jones','carol@uni.edu','555-2003','faculty','2025-03-05'),
('David','Miller','david@uni.edu','555-2004','student','2025-03-20'),
('Eve','Wilson','eve@uni.edu','555-2005','faculty','2025-04-12'),
('Frank','Moore','frank@uni.edu','555-2006','student','2025-05-08'),
('Grace','Taylor','grace@uni.edu','555-2007','student','2025-05-25'),
('Henry','Anderson','henry@uni.edu','555-2008','faculty','2025-06-15'),
('Ivy','Thomas','ivy@uni.edu','555-2009','student','2025-07-03'),
('Jack','Jackson','jack@uni.edu','555-2010','student','2025-07-22'),
('Karen','White','karen@uni.edu','555-2011','faculty','2025-08-10'),
('Leo','Harris','leo@uni.edu','555-2012','student','2025-08-28'),
('Mona','Martin','mona@uni.edu','555-2013','student','2025-09-12'),
('Nina','Thompson','nina@uni.edu','555-2014','faculty','2025-09-30'),
('Oscar','Garcia','oscar@uni.edu','555-2015','student','2025-10-14'),
('Paul','Martinez','paul@uni.edu','555-2016','student','2025-10-29'),
('Quinn','Robinson','quinn@uni.edu','555-2017','faculty','2025-11-12'),
('Rose','Clark','rose@uni.edu','555-2018','student','2025-11-27'),
('Sam','Rodriguez','sam@uni.edu','555-2019','student','2025-12-05'),
('Tina','Lewis','tina@uni.edu','555-2020','faculty','2025-12-20');

-- ---------- BOOKS (15 across 3 libraries) ----------
INSERT INTO book (title, isbn, publication_date, total_copies, available_copies, library_id) VALUES
('Computing Machinery','ISBN-001','1936-01-01',5,3,1),
('The Art of Programming','ISBN-002','1968-01-01',6,4,1),
('Principia Mathematica','ISBN-003','1687-07-05',4,2,1),
('Relativity Theory','ISBN-004','1916-01-01',5,5,2),
('Quantum Mechanics','ISBN-005','1950-01-01',3,1,2),
('Advanced Algorithms','ISBN-006','2005-01-01',6,6,1),
('Linear Algebra','ISBN-007','1998-01-01',5,3,2),
('Contract Law','ISBN-008','2010-01-01',4,2,3),
('Criminal Law','ISBN-009','2012-01-01',4,4,3),
('Legal Philosophy','ISBN-010','1975-01-01',3,1,3),
('Pride and Prejudice','ISBN-011','1813-01-28',7,5,1),
('Emma','ISBN-012','1815-12-23',6,4,1),
('Tom Sawyer','ISBN-013','1876-06-01',5,3,1),
('Political Ethics','ISBN-014','1958-01-01',3,2,2),
('Modern Physics','ISBN-015','2001-01-01',4,4,2);

-- ---------- BOOK ↔ AUTHOR ----------
INSERT INTO book_author VALUES
(1,1),(2,2),(3,3),(4,4),(5,4),
(6,2),(7,3),(8,7),(9,7),(10,8),
(11,5),(12,5),(13,6),(14,8),(15,4);

-- ---------- BOOK ↔ CATEGORY ----------
INSERT INTO book_category VALUES
(1,1),(2,1),(6,1),
(3,2),(7,2),
(4,3),(5,3),(15,3),
(8,4),(9,4),(10,4),(14,4),
(11,5),(12,5),(13,5);

-- ---------- Borrowing ----------
INSERT INTO borrowing (member_id, book_id, borrow_date, due_date, return_date, late_fee)
VALUES
-- 1-5: Returned on time
(1, 1, '2026-01-01', '2026-01-15', '2026-01-10', 0),
(2, 2, '2026-01-03', '2026-01-17', '2026-01-17', 0),
(3, 3, '2026-01-05', '2026-01-19', '2026-01-18', 0),
(4, 4, '2026-01-07', '2026-01-21', '2026-01-20', 0),
(5, 5, '2026-01-09', '2026-01-23', '2026-01-23', 0),

-- 6-10: Returned late
(6, 6, '2026-01-02', '2026-01-16', '2026-01-18', 2),
(7, 7, '2026-01-04', '2026-01-18', '2026-01-20', 2),
(8, 8, '2026-01-06', '2026-01-20', '2026-01-25', 5),
(9, 9, '2026-01-08', '2026-01-22', '2026-01-24', 2),
(10, 10, '2026-01-10', '2026-01-24', '2026-01-28', 4),

-- 11-15: Not returned yet / deadline in the past
(11, 11, '2026-01-12', '2026-01-26', NULL, NULL),
(12, 12, '2026-01-14', '2026-01-28', NULL, NULL),
(13, 13, '2026-01-16', '2026-01-30', NULL, NULL),
(14, 14, '2026-01-18', '2026-02-01', NULL, NULL),
(15, 15, '2026-01-20', '2026-02-03', NULL, NULL),

-- 16-20: Mixed returned on time / late
(16, 1, '2026-01-22', '2026-02-05', '2026-02-04', 0),
(17, 2, '2026-01-24', '2026-02-07', '2026-02-10', 3),
(18, 3, '2026-01-26', '2026-02-09', '2026-02-08', 0),
(19, 4, '2026-01-28', '2026-02-11', '2026-02-13', 2),
(20, 5, '2026-01-30', '2026-02-13', '2026-02-14', 1),

-- 21-25: Not returned yet / deadline in the future
(17, 6, '2026-02-01', '2026-02-15', NULL, NULL),
(4, 7, '2026-02-03', '2026-02-17', NULL, NULL),
(11, 8, '2026-02-05', '2026-02-19', NULL, NULL),
(6, 9, '2026-02-07', '2026-02-21', NULL, NULL),
(8, 10, '2026-02-09', '2026-02-23', NULL, NULL);

-- ---------- REVIEWS (12) ----------
INSERT INTO review (member_id, book_id, rating, comment, review_date)
VALUES
(1,1,5,'Excellent','2026-01-10'),
(2,2,4,'Very detailed','2026-01-12'),
(3,3,5,'Classic','2026-01-15'),
(4,4,4,'Great read','2026-01-18'),
(5,5,3,'Complex','2026-01-20'),
(6,6,5,'Highly recommended','2026-01-22'),
(7,7,4,'Clear','2026-01-25'),
(8,8,3,'Informative','2026-01-27'),
(9,9,4,'Good','2026-01-30'),
(10,10,3,'Thought-provoking','2026-02-01'),
(11,11,5,'Masterpiece','2026-02-05'),
(12,12,4,'Enjoyable','2026-02-08');