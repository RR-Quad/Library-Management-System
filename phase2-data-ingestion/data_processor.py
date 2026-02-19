## Notes

# Use Clean Data (Relevant ISBNs, valid phone numbers)
# Create foreign key mapping
# Check if duplicates/errors are being handled or not and make logs more specific
# Sort imports (Built-in, Installed, Local) and remove unused imports at the end
# Need to take the logging level from the user. Right now, it is set to INFO by default
# Path to the csv files should be provided by the user as well, through CLI

## Imports


import os
import csv
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

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

logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================================
# Database Setup
# ==========================================================

load_dotenv()

# Read environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# Validate required variables
if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    raise ValueError("Database environment variables are not properly set.")

# Create SQLAlchemy URL safely (handles special characters automatically)
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True
)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# ==========================================================
# Transaction Management
# ==========================================================

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.info(f"Fatal transaction failure: {str(e)}")
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

            logger.info(f"Libraries: Row {row_number} inserted.")

        except IntegrityError:
            logger.info(f"Libraries: Row {row_number} duplicate.")
        except Exception as e:
            logger.info(f"Libraries: Row {row_number} error: {str(e)}")


def process_authors(session, file_path: str):
    for row_number, row in stream_csv(file_path):

        try:
            validated = AuthorSchema(**row)

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

            logger.info(f"Authors: Row {row_number} inserted.")

        except IntegrityError:
            logger.info(f"Authors: Row {row_number} duplicate.")
        except Exception as e:
            logger.info(f"Authors: Row {row_number} error: {str(e)}")


def process_books(session, file_path: str):
    for row_number, row in stream_csv(file_path):

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
                    library_id=validated.library_id  # ✅ FIXED
                )

                session.add(book)
                session.flush()

            logger.info(f"Books: Row {row_number} inserted.")

        except IntegrityError:
            logger.info(f"Books: Row {row_number} duplicate.")
        except Exception as e:
            logger.info(f"Books: Row {row_number} error: {str(e)}")


def process_members(session, file_path: str):
    for row_number, row in stream_csv(file_path):

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

            logger.info(f"Members: Row {row_number} inserted.")


        except IntegrityError as e:
            logger.info(f"Members: Row {row_number} duplicate. Error: {str(e)}")
        except Exception as e:
            logger.info(f"Members: Row {row_number} error: {str(e)}")


# ==========================================================
# Master Orchestrator
# ==========================================================

def ingest_from_directory(directory_path: str):

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

    with session_scope() as session:

        process_libraries(session, libraries_path)
        process_authors(session, authors_path)
        process_books(session, books_path)
        process_members(session, members_path)


# ==========================================================
# Entry Point
# ==========================================================

BASE_DIR = r"D:\RR_Quad\Projects\Library Management System\phase2-data-ingestion\sample_data"

if __name__ == "__main__":
    ingest_from_directory(BASE_DIR)
