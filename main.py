import argparse
import sys
from dotenv import load_dotenv


load_dotenv()


# main.py

import json
import os
import time
from google import genai

from scorer import narrative_liquidity

# ---------------- CONFIG ---------------- #

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3-flash-preview"

client = genai.Client(api_key=GEMINI_API_KEY)

CHUNK_DURATION = 45
STEP = 30

# ---------------- TRANSCRIPT PIPELINE ---------------- #

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use-gemini",
        action="store_true",
        help="Enable optional Gemini studio analysis"
    )
    return parser.parse_args()

def load_transcript(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_transcript(text):
    words = text.split()
    words_per_sec = 2.5

    chunks = []
    start = 0

    while start < len(words):
        end = start + int(CHUNK_DURATION * words_per_sec)
        chunk_words = words[start:end]

        if not chunk_words:
            break

        chunk_text = " ".join(chunk_words)
        start_time = int(start / words_per_sec)
        end_time = int(end / words_per_sec)

        chunks.append({
            "text": chunk_text,
            "start_time": start_time,
            "end_time": end_time,
            "duration": end_time - start_time
        })

        start += int(STEP * words_per_sec)

    return chunks

def score_chunks(chunks):
    scored = []
    for c in chunks:
        score = narrative_liquidity(c["text"], c["duration"])
        scored.append({
            **c,
            "liquidity_score": score
        })

    return sorted(scored, key=lambda x: x["liquidity_score"], reverse=True)

# ---------------- GEMINI ---------------- #

def build_gemini_prompt(spike):
    return f"""
You are an editorial signal analyst operating inside the Mango Magic Protocol.

Transcript Segment:
\"\"\"
{spike['text']}
\"\"\"

Timestamp:
{spike['start_time']}–{spike['end_time']}

Narrative Liquidity Score:
{spike['liquidity_score']}

Your task:

1. Explain WHY this moment works in 3 concise bullet points.
2. Assign 3–5 tags from:
   [resonance, vulnerability, belief-shift, humor, tension, intimacy, contradiction, insight]
3. Explain why this moment is irreplaceably human and resistant to AI imitation.
4. Suggest vertical video cut guidance:
   - Best start frame
   - Best end frame
   - Subtitle density
5. Generate hooks:
   - X (≤140 chars)
   - TikTok opening line
   - Reels emotional opener

Rules:
- No summarizing
- No generic motivation
- Preserve uncertainty
"""

def call_gemini(prompt):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text

# ---------------- PARSING ---------------- #

def parse_gemini_output(text):
    sections = {
        "why_it_hits": [],
        "tags": [],
        "human_provenance": "",
        "vertical_guidance": "",
        "hooks": {}
    }

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    current = None

    for line in lines:
        lower = line.lower()

        if lower.startswith("1."):
            current = "why_it_hits"
            continue
        if lower.startswith("2."):
            current = "tags"
            continue
        if lower.startswith("3."):
            current = "human_provenance"
            continue
        if lower.startswith("4."):
            current = "vertical_guidance"
            continue
        if lower.startswith("5."):
            current = "hooks"
            continue

        if current == "why_it_hits":
            sections["why_it_hits"].append(line.lstrip("-• "))
        elif current == "tags":
            sections["tags"].extend(
                [t.strip() for t in line.replace(",", " ").split()]
            )
        elif current == "human_provenance":
            sections["human_provenance"] += line + " "
        elif current == "vertical_guidance":
            sections["vertical_guidance"] += line + " "
        elif current == "hooks":
            if "x" in lower:
                sections["hooks"]["x"] = line
            elif "tiktok" in lower:
                sections["hooks"]["tiktok"] = line
            elif "reels" in lower:
                sections["hooks"]["reels"] = line

    return sections


def print_header():
    print("\n🍋 CUTLINE — Narrative Liquidity Engine\n")
    print("Select execution mode:\n")
    print("1) Offline Signal Distillation (RECOMMENDED)")
    print("   - Fully compliant")
    print("   - No APIs")
    print("   - Reproducible\n")
    print("2) Studio Enhancement Mode (Gemini)")
    print("   - Optional")
    print("   - Requires GEMINI_API_KEY")
    print("   - Editorial interpretation layer\n")

# ---------------- MAIN ---------------- #


def main():
    print_header()
    choice = input("Enter 1 or 2: ").strip()

    transcript = load_transcript("data/transcript.txt")
    chunks = chunk_transcript(transcript)
    scored = score_chunks(chunks)

    top_spikes = scored[:5]

    if choice == "1":
        # OFFLINE MODE (DEFAULT)
        print("\n▶ Running OFFLINE signal distillation...\n")
        with open("outputs/vibe_spikes_offline.json", "w", encoding="utf-8") as f:
            json.dump(top_spikes, f, indent=2)

        print("✅ Offline spikes written to outputs/vibe_spikes_offline.json")
        return
    elif choice == "2":
        # ---- GEMINI MODE BELOW (OPTIONAL) ----
        enriched = []

        print("🔥 Studio Enhancement Mode enabled\n")

        for spike in top_spikes:
            prompt = build_gemini_prompt(spike)
            analysis_text = call_gemini(prompt)
            parsed = parse_gemini_output(analysis_text)

            enriched.append({
                "timestamp": f"{spike['start_time']}–{spike['end_time']}",
                "liquidity_score": spike["liquidity_score"],
                "text": spike["text"],
                "analysis": parsed
            })

            time.sleep(1)

        with open("outputs/vibe_spikes_gemini.json", "w", encoding="utf-8") as f:
            json.dump(enriched, f, indent=2)

        print("✅ Gemini-enhanced spikes written to outputs/vibe_spikes_gemini.json")
    else:
        print("\n❌ Invalid selection. Exiting.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
