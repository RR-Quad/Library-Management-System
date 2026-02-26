import time
import argparse
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from models import Book
from schemas import BookSchema
from api_client import OpenLibraryClient


# ---------------------------
# Logging Configuration
# ---------------------------
logging.basicConfig(
    filename="task_2.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Fetch books from OpenLibrary and insert into database."
    )

    parser.add_argument(
        "--author",
        required=True,
        help="Author name (e.g. 'Charles Dickens')"
    )

    parser.add_argument(
        "--limit",
        type=int,
        required=True,
        help="Number of valid books to fetch"
    )

    parser.add_argument(
        "--db",
        required=True,
        help="Database connection URL"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    author_name = args.author
    limit = args.limit
    database_url = args.db

    logger.info("Starting book fetch process.")
    logger.info(f"Author: {author_name}, Limit: {limit}")

    try:
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        logger.info("Database connection established.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return

    client = OpenLibraryClient()

    logger.info("Searching author...")
    author_key = client.search_author(author_name)

    if not author_key:
        logger.warning("Author not found.")
        return

    logger.info(f"Author key found: {author_key}")
    logger.info("Fetching works...")

    works = client.get_author_works(author_key)
    books = []

    for work in works:
        if len(books) >= limit:
            break

        work_key = work.get("key")
        title = work.get("title")

        if not work_key or not title:
            continue

        work_id = work_key.split("/")[-1]
        logger.info(f"Checking work: {title}")

        isbn, publish_date = client.get_valid_edition_data(work_id)
        time.sleep(1)

        if isbn and publish_date:
            books.append({
                "title": title,
                "isbn": isbn,
                "publication_date": publish_date,
                "total_copies": 5,
                "available_copies": 5,
                "library_id": 6
            })
            logger.info(f"Added valid book: {title}")

    if len(books) < limit:
        logger.warning(f"Couldn't find {limit} book(s) with valid entries.")

    logger.info(f"Total Valid Books Collected: {len(books)}")
    logger.info("Inserting books into database...")

    for book_data in books:
        try:
            validated_book = BookSchema(**book_data)

            db_book = Book(
                title=validated_book.title,
                isbn=validated_book.isbn,
                publication_date=validated_book.publication_date,
                total_copies=validated_book.total_copies,
                available_copies=validated_book.available_copies,
                library_id=validated_book.library_id
            )

            session.add(db_book)

        except Exception as e:
            logger.error(f"Validation failed for {book_data['title']}:\n{e}")

    try:
        session.commit()
        logger.info("Books inserted successfully.")
    except IntegrityError as e:
        session.rollback()
        logger.error("Database integrity error (possibly duplicate ISBN).")
        logger.error(f"\n{e}")
    finally:
        session.close()
        logger.info("Database session closed.")
        logger.info("Process completed.")


if __name__ == "__main__":
    main()
