import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3-flash-preview"


# -------------------------
# SETUP
# -------------------------

def setup_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables")

    return genai.Client(api_key=api_key)


# -------------------------
# UTILS
# -------------------------

def safe_json_parse(text: str):
    """
    Extract and parse JSON safely from model output.
    """
    text = text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned by model: {e}")


# -------------------------
# AI FUNCTIONS
# -------------------------

def generate_summary(client, transcript: str) -> str:
    prompt = f"""
You are an expert at summarizing long-form educational or documentary video content.

Summarize the transcript below into:
- A concise explanation
- Key ideas only
- No filler or repetition
- Clear, human-readable language

Transcript:
\"\"\"
{transcript}
\"\"\"
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()


def generate_quiz(client, summary: str, questions: int = 5):
    prompt = f"""
Create a quiz based on the summary below.

Rules:
- {questions} multiple-choice questions
- 4 options per question
- Clearly mark the correct answer
- Test understanding, not trivia

Return ONLY valid JSON in this format:

[
  {{
    "question": "Question text",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Summary:
\"\"\"
{summary}
\"\"\"
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return safe_json_parse(response.text)


# -------------------------
# PIPELINE
# -------------------------

def run_pipeline(transcript: str):
    client = setup_client()

    print("\n🧠 Generating Summary...\n")
    summary = generate_summary(client, transcript)
    print(summary)

    print("\n📝 Generating Quiz...\n")
    quiz = generate_quiz(client, summary)

    for i, q in enumerate(quiz, 1):
        print(f"\nQ{i}: {q['question']}")
        for opt in q["options"]:
            print(f"  - {opt}")
        print(f"✔ Answer: {q['answer']}")

    return {
        "summary": summary,
        "quiz": quiz
    }


# -------------------------
# ENTRY POINT
# -------------------------

if __name__ == "__main__":
    with open("sample_transcript.txt", "r", encoding="utf-8") as f:
        transcript_text = f.read()

    run_pipeline(transcript_text)
