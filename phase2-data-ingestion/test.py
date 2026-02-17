import pandas as pd
from pathlib import Path
from schemas import LibrarySchema, AuthorSchema, BookSchema, MemberSchema
from pydantic import ValidationError

# Base folder where your CSVs are stored
BASE_DIR = Path(r"D:\RR_Quad\Projects\Library Management System\phase2-data-ingestion\sample_data")

# Mapping of CSV filenames to schemas
csv_schema_map = {
    "libraries.csv": LibrarySchema,
    "authors.csv": AuthorSchema,
    "books.csv": BookSchema,
    "members.csv": MemberSchema
}

def validate_csv(file_path: Path, schema):
    """Validate CSV rows against the given Pydantic schema."""
    df = pd.read_csv(file_path)
    validated_rows = []

    for idx, row in df.iterrows():
        try:
            validated = schema(**row.to_dict())
            validated_rows.append(validated.dict())
        except ValidationError as e:
            print(f"Validation error in row {idx} of {file_path.name}: {e}")

    return pd.DataFrame(validated_rows)

def main():
    for csv_file, schema in csv_schema_map.items():
        file_path = BASE_DIR / csv_file
        if file_path.exists():
            validated_df = validate_csv(file_path, schema)
            output_file = BASE_DIR / f"{file_path.stem}_validated.csv"
            validated_df.to_csv(output_file, index=False)
            print(f"Validated CSV saved to {output_file}")
        else:
            print(f"File {file_path} does not exist.")

if __name__ == "__main__":
    main()
