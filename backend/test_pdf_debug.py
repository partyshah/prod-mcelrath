"""Debug script to verify PDF content is being sent to AI"""
from dotenv import load_dotenv
load_dotenv()

from ai_service import AITutorService
from database import SessionLocal
from models import Assignment

def check_pdf_content():
    print("=" * 80)
    print("DEBUGGING PDF CONTENT FLOW")
    print("=" * 80)

    # 1. Check database content
    print("\n1. CHECKING DATABASE:")
    db = SessionLocal()
    assignment = db.query(Assignment).filter_by(id=1).first()
    if assignment and assignment.pdf_content:
        print(f"✅ PDF content in database: {len(assignment.pdf_content)} characters")
        print(f"First 500 chars: {assignment.pdf_content[:500]}...")
    else:
        print("❌ No PDF content in database")
    db.close()

    # 2. Initialize session and check what's stored
    print("\n2. INITIALIZING SESSION:")
    ai_service = AITutorService()
    session_id = "debug_session_1_1"

    result = ai_service.initialize_session(
        session_id,
        ["week1/ethricsreading.pdf"],
        assignment_id=1
    )
    print(f"Initialization result: {result}")

    # 3. Check what's actually in the session
    print("\n3. CHECKING SESSION DATA:")
    if session_id in ai_service.sessions:
        session_data = ai_service.sessions[session_id]
        pdf_context = session_data.get('pdf_context', '')
        print(f"✅ PDF context in session: {len(pdf_context)} characters")
        print(f"First 500 chars of context: {pdf_context[:500]}...")

        # Check if it contains key content from the ethics PDF
        key_terms = ["Bow Wow", "ethics", "technology", "algorithmic bias", "privacy"]
        print("\n4. CHECKING FOR KEY TERMS:")
        for term in key_terms:
            if term.lower() in pdf_context.lower():
                print(f"✅ Found '{term}' in context")
            else:
                print(f"❌ '{term}' NOT found in context")
    else:
        print("❌ Session not found in ai_service.sessions")

    # 4. Test a message to see what system prompt is used
    print("\n5. TESTING AI PROMPT CONSTRUCTION:")

    # Let's peek at what the conversation manager does
    if session_id in ai_service.sessions:
        conv_manager = ai_service.sessions[session_id]['manager']

        # Check the system prompt that will be sent
        from prompts import TUTOR_SYSTEM_PROMPT

        # Format the full system prompt
        full_prompt = TUTOR_SYSTEM_PROMPT.format(
            pdf_context=pdf_context[:2000] + "..." if len(pdf_context) > 2000 else pdf_context
        )

        print(f"System prompt length: {len(full_prompt)} characters")
        print(f"\nFirst 1000 chars of system prompt being sent to AI:")
        print("-" * 60)
        print(full_prompt[:1000])
        print("-" * 60)

if __name__ == "__main__":
    check_pdf_content()