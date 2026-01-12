# AI-Powered Video Summarizer & Quiz Generator

This project demonstrates an AI-driven pipeline that transforms long-form video content into concise summaries and interactive quizzes.

The goal is not just compression, but **surfacing signal from noise** — helping people understand and retain meaningful ideas from long videos.

---

## What It Does

1. Takes a long-form video transcript
2. Generates a concise, human-readable summary using Gemini
3. Automatically creates a multiple-choice quiz based on key ideas

This mimics how AI can assist with media understanding, education, and narrative extraction.

---

## Why This Matters

Long videos often contain valuable insights that are hard to revisit or retain.
This tool acts as a creative filter — helping surface what matters most and turning passive content into active understanding.

---

## Tech Stack

- Python
- Google Gemini (LLM)
- Prompt-driven narrative extraction
- JSON-safe AI orchestration

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/myk-francis/ai-video-summarizer-quiz
cd ai-video-summarizer-quiz
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python main.py
```

### Example

This Joe Rogan Experience episode features actor and director Bradley Cooper. The conversation explores the psychological toll of modern media, the evolving culture of stand-up comedy, and the rigorous physical and emotional demands of high-level acting.

### Key Ideas

**The Psychology of Modern Media**

- **Dopamine Hijacking:** Short-form content (like TikTok) acts as a "dopamine drip" that creates low-level anxiety and reduces attention spans, whereas long-form content (documentaries, three-hour films like _Oppenheimer_) fulfills a deeper human need for connection and storytelling.
- **Memory Distortion:** Constant exposure to digital content and VR can blur the lines between real-life experiences and viewed footage, altering how the brain stores memories.
- **Dunbar’s Number:** The human brain is evolutionarily limited to maintaining relationships with roughly 150 to 1,500 people. Modern fame and social media overload this capacity, leading to cognitive strain.

**The Evolution of Comedy Culture**

- **From Competition to Collaboration:** The rise of the internet and podcasts transformed comedy from a zero-sum competition into a collaborative ecosystem.
- **Authenticity in Film:** Cooper emphasizes realism in filmmaking by capturing genuine environments rather than manufactured performances.

**The Craft of “The Method”**

- **Staying in Character:** Remaining in character ensures performances are instinctive rather than calculated.
- **Emotional Utility:** Personal experiences and insecurities are consciously used as tools for authentic acting.

**The Physical Toll of _American Sniper_**

- **Extreme Transformation:** Cooper underwent a dramatic physical transformation, requiring intense training and discipline.
- **Responsibility to the Subject:** Portraying a real person carried a deep emotional and ethical responsibility.

**Inspiration and the “Shadow”**

- **The Catalyst:** Cooper traces his lifelong dedication to storytelling back to watching _The Elephant Man_ at age 11.

Q1: According to the discussion on modern media, how does long-form content like 'Oppenheimer' differ from short-form content like TikTok?

- Long-form content creates a 'dopamine drip' that leads to low-level anxiety.
- Long-form content satisfies a deep human need for connection and storytelling.
- Long-form content is primarily responsible for reducing human attention spans.
- Long-form content causes more significant memory distortion than short-form content.
  ✔ Answer: Long-form content satisfies a deep human need for connection and storytelling.

Q2: How does the concept of 'Dunbar’s Number' explain the difficulties of modern fame and social media?

- It suggests that social media improves the brain's capacity to store names.
- It proves that humans are evolutionarily designed to interact with thousands of people daily.
- It indicates that the brain's capacity for relationships is limited, leading to an inability to manage high-volume social exposure.
- It explains why digital content is more memorable than real-life experiences.
  ✔ Answer: It indicates that the brain's capacity for relationships is limited, leading to an inability to manage high-volume social exposure.

Q3: What primary factor changed the comedy scene from a 'cutthroat' competition to a collaborative environment?

- The decline of open mic nights.
- The transition to canned laughter.
- The rise of the internet and podcasts.
- A renewed focus on late-night television.
  ✔ Answer: The rise of the internet and podcasts.

Q4: Why does Bradley Cooper stay in his character’s voice throughout filming?

- To intimidate other actors.
- To follow rigid acting rules.
- To make the performance instinctive rather than calculated.
- To avoid emotional vulnerability.
  ✔ Answer: To make the performance instinctive rather than calculated.

Q5: Why did Cooper adopt personal rituals while preparing for _American Sniper_?

- To improve his diet efficiency.
- To distract from physical strain.
- To fulfill a responsibility to merge with the real-life subject.
- To emulate other actors.
  ✔ Answer: To fulfill a responsibility to merge with the real-life subject.
