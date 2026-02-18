## Imports


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import Library
from models import Book
from datetime import date

DATABASE_URL = "postgresql://postgres:jupiter@localhost:5432/Library Management System"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

lib = Library(
    name="Westside Library",
    campus_location="wesside",
    contact_email="wesside@library.com",
    phone_number="1030567890"
)
#
# session.add(lib)
# session.commit()



book = Book(
    title="1984",
    isbn="9780451524935",
    publication_date=date(1949, 6, 8),  # ✅ REQUIRED
    total_copies=5,
    available_copies=5,
    library=lib
)

session.add(book)
# session.commit()

from models import Author

author = Author(
    first_name="George",
    last_name="Orwell"
)

book.authors.append(author)
session.commit()
