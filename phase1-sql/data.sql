-- ---------- LIBRARIES (5) ----------
INSERT INTO library (name, campus_location, contact_email, phone_number) VALUES
('Main', 'Central Campus', 'main.library@uni.edu', '+910000000000'),
('Fundamental Science', 'Science Block', 'fundamental.science.library@uni.edu', '+910000000001'),
('Social Science', 'Social Sciences Block', 'social.science.library@uni.edu', '+910000000002'),
('Engineering', 'Engineering Block', 'engineering.library@uni.edu', '+910000000003'),
('Business', 'Business School', 'business.library@uni.edu', '+910000000004'),
('Book Warehouse', 'Central Campus', 'warehouse@uni.edu', '+910000000005');

-- ---------- BOOKS (15 across 3 libraries) ----------
INSERT INTO book (title, isbn, publication_date, total_copies, available_copies, library_id)VALUES

-- Library 1 (Main)
('Pride And Prejudice', '9780141439518', '1813-01-28', 5, 5, 1),
('Sapiens', '9780062316097', '2011-01-01', 6, 5, 1),
('The Republic', '9780140455113', '0380-01-01', 4, 4, 1),

-- Library 2 (Fundamental Science)
('A Brief History Of Time', '9780553380163', '1988-01-01', 5, 4, 2),
('The Selfish Gene', '9780199291151', '1976-01-01', 4, 4, 2),
('Principia Mathematica', '9780521626068', '1687-07-05', 4, 3, 2),
('Chemistry The Central Science', '9780134414232', '2017-01-01', 6, 5, 2),

-- Library 3 (Social Science)
('The Prince', '9780140449150', '1532-01-01', 4, 4, 3),
('On Liberty', '9780140432077', '1859-01-01', 4, 3, 3),
('The Federalist Papers', '9780140444957', '1788-01-01', 4, 3, 3),

-- Library 4 (Engineering)
('Introduction To Algorithms', '9780262033848', '2009-01-01', 6, 5, 4),
('Clean Code', '9780132350884', '2008-01-01', 5, 5, 4),
('Digital Design', '9780132774208', '2012-01-01', 5, 5, 4),

-- Library 5 (Business)
('The Intelligent Investor', '9780060555665', '1949-01-01', 6, 5, 5),
('Principles Of Economics', '9780538453059', '2011-01-01', 5, 5, 5);


-- ---------- AUTHORS (8) ----------
INSERT INTO author (first_name, last_name, birth_date, nationality, biography) VALUES

-- Pride And Prejudice
('Jane', 'Austen', '1775-12-16', 'British',
'English novelist known primarily for her six major novels including Pride And Prejudice.'),

-- Sapiens
('Yuval Noah', 'Harari', '1976-02-24', 'Israeli',
'Historian and professor known for popular science books on human history.'),

-- The Republic
('Plato', 'Philosopher', '0428-01-01', 'Greek',
'Ancient Greek philosopher and founder of the Academy in Athens.'),

-- A Brief History Of Time
('Stephen', 'Hawking', '1942-01-08', 'British',
'Theoretical physicist and cosmologist known for work on black holes.'),

-- The Selfish Gene
('Richard', 'Dawkins', '1941-03-26', 'British',
'Evolutionary biologist known for gene-centered view of evolution.'),

-- Principia Mathematica
('Isaac', 'Newton', '1643-01-04', 'British',
'Mathematician and physicist who formulated laws of motion and gravity.'),

-- Chemistry The Central Science
('Theodore', 'Brown', '1944-01-01', 'American',
'Chemist and co-author of the textbook Chemistry The Central Science.'),

-- The Prince
('Niccolo', 'Machiavelli', '1469-05-03', 'Italian',
'Renaissance political philosopher known for The Prince.'),

-- On Liberty
('John Stuart', 'Mill', '1806-05-20', 'British',
'Philosopher and political economist known for liberal political theory.'),

-- The Federalist Papers
('Alexander', 'Hamilton', '1755-01-11', 'American',
'Founding Father of the United States and co-author of The Federalist Papers.'),

-- Introduction To Algorithms
('Thomas', 'Cormen', '1956-01-01', 'American',
'Computer scientist and co-author of Introduction To Algorithms.'),

-- Clean Code
('Robert', 'Martin', '1952-12-05', 'American',
'Software engineer known for Clean Code and agile principles.'),

-- Digital Design
('Morris', 'Mano', '1921-02-20', 'American',
'Computer engineer and author of Digital Design.'),

-- The Intelligent Investor
('Benjamin', 'Graham', '1894-05-09', 'American',
'Economist and investor known as the father of value investing.'),

-- Principles Of Economics
('N. Gregory', 'Mankiw', '1958-02-03', 'American',
'Economist and author of Principles Of Economics.');

-- ---------- MEMBERS (20) ----------
INSERT INTO member (first_name, last_name, contact_email, phone_number, member_type, registration_date) VALUES
('Aarav', 'Sharma', 'aarav.sharma@uni.edu', '+911000000000', 'Student', '2024-01-05'),
('Ishita', 'Verma', 'ishita.verma@uni.edu', '+911000000001', 'Student', '2024-01-18'),
('Rohan', 'Mehta', 'rohan.mehta@uni.edu', '+911000000002', 'Faculty', '2024-02-12'),
('Sneha', 'Reddy', 'sneha.reddy@uni.edu', '+911000000003', 'Student', '2024-02-28'),
('Aditya', 'Nair', 'aditya.nair@uni.edu', '+911000000004', 'Student', '2024-03-10'),
('Priya', 'Iyer', 'priya.iyer@uni.edu', '+911000000005', 'Faculty', '2024-03-22'),
('Karthik', 'Rao', 'karthik.rao@uni.edu', '+911000000006', 'Student', '2024-04-08'),
('Ananya', 'Gupta', 'ananya.gupta@uni.edu', '+911000000007', 'Student', '2024-04-19'),
('Vikram', 'Singh', 'vikram.singh@uni.edu', '+911000000008', 'Faculty', '2024-05-03'),
('Meera', 'Chopra', 'meera.chopra@uni.edu', '+911000000009', 'Student', '2024-05-21'),
('Arjun', 'Patel', 'arjun.patel@uni.edu', '+911000000010', 'Student', '2024-06-11'),
('Divya', 'Kulkarni', 'divya.kulkarni@uni.edu', '+911000000011', 'Faculty', '2024-06-29'),
('Rahul', 'Joshi', 'rahul.joshi@uni.edu', '+911000000012', 'Student', '2024-07-15'),
('Neha', 'Malhotra', 'neha.malhotra@uni.edu', '+911000000013', 'Student', '2024-07-30'),
('Siddharth', 'Bansal', 'siddharth.bansal@uni.edu', '+911000000014', 'Faculty', '2024-08-14'),
('Pooja', 'Desai', 'pooja.desai@uni.edu', '+911000000015', 'Student', '2024-08-26'),
('Manish', 'Tiwari', 'manish.tiwari@uni.edu', '+911000000016', 'Student', '2024-09-09'),
('Kavya', 'Menon', 'kavya.menon@uni.edu', '+911000000017', 'Faculty', '2024-10-02'),
('Harsh', 'Agarwal', 'harsh.agarwal@uni.edu', '+911000000018', 'Student', '2024-11-18'),
('Tanvi', 'Saxena', 'tanvi.saxena@uni.edu', '+911000000019', 'Faculty', '2024-12-05');

-- ---------- CATEGORIES (18) ----------
INSERT INTO category (name, description) VALUES
-- Main Library Categories
('Literature', 'Books related to literary works, novels, and writings.'),
('History', 'Books covering historical events and civilizations.'),
('Philosophy', 'Books exploring philosophical thought and theories.'),
('Religion', 'Books on religious studies and spiritual traditions.'),

-- Fundamental Science Categories
('Physics', 'Books related to physical sciences and theoretical physics.'),
('Chemistry', 'Books covering chemical sciences and applications.'),
('Biology', 'Books focused on life sciences and biological systems.'),
('Mathematics', 'Books on mathematical theories and problem solving.'),
('Geology', 'Books related to earth sciences and geological studies.'),

-- Social Science Categories
('Politics', 'Books covering political systems and governance.'),
('Law', 'Books related to legal systems and jurisprudence.'),

-- Engineering Categories
('Manufacturing Engineering', 'Books related to production and manufacturing systems.'),
('Mechanical Engineering', 'Books covering mechanics and machine design.'),
('Electrical Engineering', 'Books on electrical systems and power technologies.'),
('Computer Engineering', 'Books related to computing hardware and systems.'),

-- Business Categories
('Finance', 'Books covering financial systems and investments.'),
('Management', 'Books focused on organizational and business management.'),
('Economics', 'Books on economic theory and market systems.');

-- ---------- BOOK ↔ AUTHOR ----------
INSERT INTO book_author VALUES
(1,1),   -- Pride And Prejudice → Jane Austen
(2,2),   -- Sapiens → Yuval Noah Harari
(3,3),   -- The Republic → Plato
(4,4),   -- A Brief History Of Time → Stephen Hawking
(5,5),   -- The Selfish Gene → Richard Dawkins
(6,6),   -- Principia Mathematica → Isaac Newton
(7,7),   -- Chemistry The Central Science → Theodore Brown
(8,8),   -- The Prince → Niccolo Machiavelli
(9,9),   -- On Liberty → John Stuart Mill
(10,10), -- The Federalist Papers → Alexander Hamilton
(11,11), -- Introduction To Algorithms → Thomas Cormen
(12,12), -- Clean Code → Robert Martin
(13,13), -- Digital Design → Morris Mano
(14,14), -- The Intelligent Investor → Benjamin Graham
(15,15); -- Principles Of Economics → N. Gregory Mankiw

-- ---------- BOOK ↔ CATEGORY ----------
INSERT INTO book_category VALUES
(1,1),   -- Pride And Prejudice → Literature
(2,2),   -- Sapiens → History
(3,3),   -- The Republic → Philosophy

-- Library 2
(4,5),   -- A Brief History Of Time → Physics
(5,7),   -- The Selfish Gene → Biology
(6,8),   -- Principia Mathematica → Mathematics
(7,6),   -- Chemistry The Central Science → Chemistry

-- Library 3
(8,10),  -- The Prince → Politics
(9,3),   -- On Liberty → Philosophy
(10,10), -- The Federalist Papers → Politics

-- Library 4
(11,15), -- Introduction To Algorithms → Computer Engineering
(12,15), -- Clean Code → Computer Engineering
(13,14), -- Digital Design → Electrical Engineering

-- Library 5
(14,16), -- The Intelligent Investor → Finance
(15,18); -- Principles Of Economics → Economics

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