## Imports


import re
from datetime import date
from typing import Optional

import isbnlib
import phonenumbers
from pydantic import BaseModel, EmailStr, field_validator


## Utility Functions


def normalize_name(name: str) -> str:
    if not name:
        raise ValueError("Entry name cannot be empty")
    return " ".join(part.capitalize() for part in name.strip().split())


def normalize_phone(phone: str) -> str:
    if not phone:
        raise ValueError("Phone Number cannot be empty")

    try:
        parsed = phonenumbers.parse(phone, "IN")
        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("Invalid phone number")

        return phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        )
    except Exception:
        # fallback: extract digits only
        digits = re.sub(r"\D", "", phone)
        if len(digits) == 10:
            return f"+1{digits}"
        elif len(digits) > 10:
            return f"+{digits}"
        raise ValueError("Invalid phone number")


def validate_isbn(isbn: str) -> str:
    if not isbn:
        raise ValueError("ISBN cannot be empty")

    cleaned = re.sub(r"[-\s]", "", isbn)

    if isbnlib.is_isbn10(cleaned) or isbnlib.is_isbn13(cleaned):
        return cleaned
    raise ValueError("Invalid ISBN")


## Classes


class LibrarySchema(BaseModel):
    library_id: Optional[int] = None
    name: str
    campus_location: str
    contact_email: EmailStr
    phone_number: str

    @field_validator("name")
    @classmethod
    def normalize_library_name(cls, v):
        return normalize_name(v)

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        return normalize_phone(v)


class BookSchema(BaseModel):
    book_id: Optional[int] = None
    title: str
    isbn: str
    publication_date: Optional[date] = None
    total_copies: int
    available_copies: int
    library_id: int

    @field_validator("title")
    @classmethod
    def normalize_text(cls, v):
        return normalize_name(v)

    @field_validator("isbn")
    @classmethod
    def validate_book_isbn(cls, v):
        return validate_isbn(v)


class AuthorSchema(BaseModel):
    author_id: Optional[int] = None
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    nationality : Optional[str] = None
    biography: Optional[str] = None

    @field_validator("first_name", "last_name")
    @classmethod
    def normalize_author_name(cls, v):
        return normalize_name(v)


class MemberSchema(BaseModel):
    member_id: Optional[int] = None
    first_name: str
    last_name: str
    contact_email: EmailStr
    phone_number: str
    member_type: str
    registration_date: date

    # Normalize first and last names
    @field_validator("first_name", "last_name")
    @classmethod
    def normalize_member_name(cls, v):
        return normalize_name(v)

    # Validate phone numbers
    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        return normalize_phone(v)

    # Validate Member Type
    @field_validator("member_type")
    @classmethod
    def validate_member_type(cls, v):
        if v.capitalize() not in {'Student', 'Faculty'}:
            raise ValueError("member_type must be Student or Faculty")
        return v.capitalize()


## End