-- ============================================================
-- DROP ALL TABLES - Library Management System
-- ============================================================

-- Drop junction tables first
DROP TABLE IF EXISTS book_category CASCADE;
DROP TABLE IF EXISTS book_author CASCADE;

-- Drop dependent tables
DROP TABLE IF EXISTS review CASCADE;
DROP TABLE IF EXISTS borrowing CASCADE;

-- Drop main entity tables
DROP TABLE IF EXISTS book CASCADE;
DROP TABLE IF EXISTS member CASCADE;
DROP TABLE IF EXISTS author CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS library CASCADE;

-- Drop trigger function
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
