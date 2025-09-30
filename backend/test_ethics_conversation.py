"""Test conversation with ethics reading content"""
from dotenv import load_dotenv
load_dotenv()  # Load environment variables first

from ai_service import AITutorService
import json
import os

def run_test_conversation():
    print("=" * 80)
    print("TESTING AI TUTOR WITH ETHICS READING")
    print("=" * 80)

    # Initialize AI service
    ai_service = AITutorService()

    # Create a test session with assignment_id=1 (which has the ethics PDF content)
    session_id = "test_ethics_session_1_1"

    # Initialize session - this will use the database content
    result = ai_service.initialize_session(
        session_id,
        ["week1/ethricsreading.pdf"],
        assignment_id=1
    )

    print(f"\n✅ Session initialized: {result}")

    # Simulate a conversation
    conversation_flow = [
        "Hi! I read the chapter about ethics in technology. Can we discuss the Bow Wow example that was mentioned at the beginning?",
        "That's interesting. What are some of the main ethical frameworks the reading discusses for evaluating technology decisions?",
        "Can you help me understand the difference between consequentialism and deontological ethics in the context of AI development?",
        "How does the reading suggest we should approach privacy concerns in social media platforms?",
        "I'm struggling to understand the concept of 'algorithmic bias' mentioned in the reading. Can you explain it?"
    ]

    print("\n" + "=" * 80)
    print("STARTING CONVERSATION")
    print("=" * 80)

    for i, student_message in enumerate(conversation_flow, 1):
        print(f"\n{'─' * 60}")
        print(f"Turn {i}")
        print(f"{'─' * 60}")

        print(f"\n🧑 STUDENT: {student_message}")

        # Get AI response
        ai_response, metadata = ai_service.get_ai_response(session_id, student_message)

        print(f"\n🤖 AI TUTOR: {ai_response}")

        # Show metadata if interesting
        if metadata.get('topic_transition'):
            print(f"\n📊 Metadata: Topic transition detected")

        # Continue for all 5 turns
        # if i >= 3:
        #     print("\n[Stopping after 3 turns for brevity...]")
        #     break

    # Get final evaluation
    print("\n" + "=" * 80)
    print("GETTING FINAL EVALUATION")
    print("=" * 80)

    # Evaluate the conversation
    evaluation = ai_service.evaluate_session(session_id)

    print(f"\n📊 EVALUATION RESULTS:")
    print(f"Score: {evaluation['score']}/100")
    print(f"Category: {evaluation['category']}")
    print(f"\nFeedback: {evaluation['feedback']}")

    # Show conversation summary
    if session_id in ai_service.sessions:
        conv_history = ai_service.sessions[session_id]['conversation_history']
        print(f"\n📝 Total conversation turns: {len(conv_history)}")

if __name__ == "__main__":
    run_test_conversation()