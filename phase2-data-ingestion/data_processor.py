## Notes

# Create foreign key mapping
# Check why Library_id skips entries
# Verify the default format for phone numbers
# Sort imports (Built-in, Installed, Local) and remove unused imports at the end
# Do log files need timestamps?
# Create Indexes

## Imports


import os
import csv
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import argparse

from models import Library, Author, Book, Member
from schemas import (
    LibrarySchema,
    AuthorSchema,
    BookSchema,
    MemberSchema
)

# ==========================================================
# Logging Configuration
# ==========================================================

def configure_logging(log_level: str):
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers (important)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    file_handler = logging.FileHandler("task_1.log")
    file_handler.setLevel(numeric_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)

logger = logging.getLogger(__name__)

# ==========================================================
# Database Setup
# ==========================================================

def create_session_factory(database_url: str):
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        future=True
    )

    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False
    )

# ==========================================================
# Transaction Management
# ==========================================================

@contextmanager
def session_scope(Session):
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Fatal transaction failure: {str(e)}")
        raise
    finally:
        session.close()


# ==========================================================
# CSV Reader
# ==========================================================

def stream_csv(file_path: str):
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row_number, row in enumerate(reader, start=2):
            yield row_number, row


# ==========================================================
# Processing Functions
# ==========================================================

def process_libraries(session, file_path: str):
    for row_number, row in stream_csv(file_path):

        logger.debug(f"Libraries: Processing row {row_number - 1}: {row}")

        try:
            validated = LibrarySchema(**row)

            with session.begin_nested():

                library = Library(
                    name=validated.name,
                    campus_location=validated.campus_location,
                    contact_email=validated.contact_email,
                    phone_number=validated.phone_number
                )

                session.add(library)
                session.flush()

            logger.info(f"Libraries: Row {row_number - 1} inserted.")

        except IntegrityError:
            logger.warning(f"Libraries: Row {row_number - 1} duplicate.")
        except Exception as e:
            logger.error(f"Libraries: Row {row_number - 1} error:\n{e}")


def process_authors(session, file_path: str):
    for row_number, row in stream_csv(file_path):

        logger.debug(f"Authors: Processing row {row_number - 1}: {row}")

        try:
            validated = AuthorSchema(**row)

            existing_author = session.query(Author).filter_by(
                first_name=validated.first_name,
                last_name=validated.last_name,
                birth_date=validated.birth_date
            ).first()

            if existing_author:
                logger.warning(
                    f"Authors: Row {row_number - 1} duplicate."
                )
                continue

            with session.begin_nested():

                author = Author(
                    first_name=validated.first_name,
                    last_name=validated.last_name,
                    birth_date=validated.birth_date,
                    nationality=validated.nationality,
                    biography=validated.biography
                )

                session.add(author)
                session.flush()

            logger.info(f"Authors: Row {row_number - 1} inserted.")

        except IntegrityError:
            logger.warning(f"Authors: Row {row_number - 1} duplicate.")
        except Exception as e:
            logger.error(f"Authors: Row {row_number - 1} error:\n{e}")


def process_books(session, file_path: str):
    for row_number, row in stream_csv(file_path):

        logger.debug(f"Books: Processing row {row_number - 1}: {row}")

        try:
            validated = BookSchema(**row)

            # Ensure referenced library exists
            library = session.query(Library).filter_by(
                library_id=validated.library_id
            ).first()

            if not library:
                raise ValueError(
                    f"Library with ID {validated.library_id} not found."
                )

            with session.begin_nested():

                book = Book(
                    title=validated.title,
                    isbn=validated.isbn,
                    publication_date=validated.publication_date,
                    total_copies=validated.total_copies,
                    available_copies=validated.available_copies,
                    library_id=validated.library_id
                )

                session.add(book)
                session.flush()

            logger.info(f"Books: Row {row_number - 1} inserted.")

        except IntegrityError:
            logger.warning(f"Books: Row {row_number - 1} duplicate.")
        except Exception as e:
            logger.error(f"Books: Row {row_number - 1} error:\n{e}")


def process_members(session, file_path: str):
    for row_number, row in stream_csv(file_path):

        logger.debug(f"Members: Processing row {row_number - 1}: {row}")

        try:
            validated = MemberSchema(**row)

            with session.begin_nested():

                member = Member(
                    first_name=validated.first_name,
                    last_name=validated.last_name,
                    contact_email=validated.contact_email,
                    phone_number=validated.phone_number,
                    member_type=validated.member_type,
                    registration_date=validated.registration_date
                )

                session.add(member)
                session.flush()

            logger.info(f"Members: Row {row_number - 1} inserted.")


        except IntegrityError as e:
            logger.warning(f"Members: Row {row_number - 1} duplicate.")
        except Exception as e:
            logger.error(f"Members: Row {row_number - 1} error:\n{e}")


# ==========================================================
# Master Orchestrator
# ==========================================================

def ingest_from_directory(directory_path: str, Session):

    libraries_path = os.path.join(directory_path, "libraries.csv")
    authors_path = os.path.join(directory_path, "authors.csv")
    books_path = os.path.join(directory_path, "books.csv")
    members_path = os.path.join(directory_path, "members.csv")

    required_files = [
        libraries_path,
        authors_path,
        books_path,
        members_path
    ]

    for file_path in required_files:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing required file: {file_path}")

    with session_scope(Session) as session:
        logger.info("Starting ingestion process...")
        process_libraries(session, libraries_path)
        process_authors(session, authors_path)
        process_books(session, books_path)
        process_members(session, members_path)
        logger.info("Ingestion completed successfully.")

# ==========================================================
# Entry Point
# ==========================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Library Data Ingestion Tool"
    )

    parser.add_argument(
        "-d", "--directory",
        required=True,
        help="Path to directory containing CSV files"
    )

    parser.add_argument(
        "--db",
        "--database-url",
        dest="database_url",
        required=True,
        help="Database connection URL"
    )

    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)"
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    configure_logging(args.log_level)
    logger = logging.getLogger(__name__)
    Session = create_session_factory(args.database_url)

    ingest_from_directory(args.directory, Session)
