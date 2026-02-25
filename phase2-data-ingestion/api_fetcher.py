import argparse
import json
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Book, Author
from schemas import BookSchema
from api_client import OpenLibraryClient


# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Fetch books from Open Library API"
    )

    parser.add_argument("--author", required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--db", "--database-url",
                        dest="database_url", required=True)
    parser.add_argument("--output",
                        help="Optional JSON file to save raw API data")

    return parser.parse_args()


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Main Logic
# ---------------------------------------------------------

def main():
    args = parse_arguments()

    engine = create_engine(args.database_url, future=True)
    Session = sessionmaker(bind=engine)

    client = OpenLibraryClient()

    logger.info(f"Searching author: {args.author}")

    author_data = client.search_author(args.author)
    author_key = author_data["key"]

    works = client.get_author_works(author_key, args.limit)

    raw_output = []

    with Session() as session:

        for work in works:

            work_details = client.get_work_details(work["key"])
            raw_output.append(work_details)

            title = work_details.get("title")
            description = work_details.get("description")

            if isinstance(description, dict):
                description = description.get("value")

            # ISBN extraction
            isbn_list = work_details.get("isbn_13", []) or \
                        work_details.get("isbn_10", [])

            if not isbn_list:
                logger.warning(f"Skipping '{title}' (no ISBN)")
                continue

            isbn = isbn_list[0]

            try:
                validated = BookSchema(
                    title=title,
                    isbn=isbn,
                    publication_date=None,
                    total_copies=1,
                    available_copies=1,
                    library_id=1  # Default library for API imports
                )

            except Exception as e:
                logger.error(f"Validation failed for '{title}': {e}")
                continue

            # Duplicate check
            existing = session.query(Book).filter_by(
                isbn=validated.isbn
            ).first()

            if existing:
                logger.info(f"Duplicate skipped: {title}")
                continue

            book = Book(
                title=validated.title,
                isbn=validated.isbn,
                total_copies=1,
                available_copies=1,
                library_id=1
            )

            session.add(book)
            logger.info(f"Inserted: {title}")

        session.commit()

    # Optional JSON dump
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(raw_output, f, indent=2)

    logger.info("API fetch completed.")


if __name__ == "__main__":
    main()