"""Script to extract PDF text and store it in the database"""
import os
from PyPDF2 import PdfReader
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Assignment

def extract_pdf_text(pdf_path):
    """Extract all text from a PDF file"""
    print(f"Extracting text from: {pdf_path}")

    reader = PdfReader(pdf_path)
    text_content = []

    for page_num, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        if text:
            text_content.append(f"[Page {page_num}]\n{text}")
            print(f"  Extracted page {page_num}")

    full_text = "\n\n".join(text_content)
    print(f"  Total extracted: {len(full_text)} characters")
    return full_text

def main():
    # Path to your PDF
    pdf_path = "static/assignments/week1/ethricsreading.pdf"

    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        return

    # Extract text
    pdf_text = extract_pdf_text(pdf_path)

    # Connect to database
    db = SessionLocal()

    try:
        # Check if assignment exists, if not create it
        assignment = db.query(Assignment).filter_by(id=1).first()

        if not assignment:
            # Create new assignment
            assignment = Assignment(
                id=1,
                title="Ethics in Technology",
                description="Reading assignment on ethics in technology and AI",
                week_number=1,
                pdf_paths=["week1/ethricsreading.pdf"],
                pdf_content=pdf_text
            )
            db.add(assignment)
            print("Created new assignment with PDF content")
        else:
            # Update existing assignment
            assignment.pdf_content = pdf_text
            assignment.pdf_paths = ["week1/ethricsreading.pdf"]
            print("Updated existing assignment with PDF content")

        db.commit()
        print(f"Successfully stored {len(pdf_text)} characters of PDF content in database")

        # Verify it was saved
        saved_assignment = db.query(Assignment).filter_by(id=1).first()
        if saved_assignment.pdf_content:
            print(f"Verified: PDF content saved ({len(saved_assignment.pdf_content)} chars)")
            print(f"First 200 chars: {saved_assignment.pdf_content[:200]}...")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()