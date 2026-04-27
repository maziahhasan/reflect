from mem0 import MemoryClient
from groq import Groq
import os
from dotenv import load_dotenv
from datetime import datetime
import random

load_dotenv()

# Initialize clients
mem0 = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

USER_ID = "reflect_user"

# ── AFFIRMATIONS ──
AFFIRMATIONS = [
    "You are doing better than you think. 🌿",
    "Every feeling you have is valid. Be gentle with yourself.",
    "You've made it through every hard day so far. That's 100%.",
    "Small steps still move you forward.",
    "You don't have to have it all together right now.",
    "Healing isn't linear — and that's okay.",
    "You are worthy of rest, care, and kindness.",
    "It's okay to not be okay. You're not alone.",
    "Your feelings are messengers, not enemies.",
    "One breath at a time. You've got this.",
]

# ── JOURNAL PROMPTS ──
JOURNAL_PROMPTS = [
    "What's one thing that felt heavy today, and one thing that felt light?",
    "What emotion showed up most today? Where did you feel it in your body?",
    "If your feelings today had a color, what would it be and why?",
    "What's something you need that you haven't given yourself lately?",
    "What's one small thing you're proud of yourself for this week?",
    "What would you tell a close friend if they were feeling exactly how you feel right now?",
    "What does your ideal tomorrow look, feel, and sound like?",
    "What's something you've been avoiding? What's the feeling underneath it?",
    "Who or what brought you a moment of calm or joy today, even briefly?",
    "What does your body need right now — rest, movement, nourishment, or stillness?",
]

# ── GROUNDING TECHNIQUES ──
GROUNDING = {
    "5-4-3-2-1": {
        "title": "5-4-3-2-1 Grounding",
        "steps": [
            "👁️ Name **5 things** you can see around you.",
            "✋ Notice **4 things** you can physically feel (floor, clothes, air).",
            "👂 Listen for **3 sounds** in your environment.",
            "👃 Find **2 things** you can smell (or like the smell of).",
            "👅 Notice **1 thing** you can taste right now.",
        ]
    },
    "box-breathing": {
        "title": "Box Breathing",
        "steps": [
            "Breathe **in** slowly for 4 counts.",
            "**Hold** your breath for 4 counts.",
            "Breathe **out** slowly for 4 counts.",
            "**Hold** for 4 counts.",
            "Repeat 4 times. Let your shoulders drop on each exhale. 🌿",
        ]
    },
    "body-scan": {
        "title": "Quick Body Scan",
        "steps": [
            "Close your eyes and take one slow breath.",
            "Start at the top of your head — notice any tension.",
            "Move down to your shoulders and jaw — consciously soften them.",
            "Check in with your chest and belly — is your breath shallow or deep?",
            "Feel your feet on the floor. You are here. You are grounded. 🌿",
        ]
    }
}

def chat(user_message: str):
    """Main chat function — returns (reply, memories, flags)."""
    # Save user message to memory
    mem0.add([
        {"role": "user", "content": user_message}
    ], user_id=USER_ID, metadata={"timestamp": datetime.now().isoformat()})

    # Retrieve relevant memories
    memories = mem0.search(user_message, filters={"user_id": USER_ID}, limit=5)
    memory_text = "\n".join([m.get("memory", "") for m in memories.get("results", memories)])

    # Detect crisis keywords
    crisis_keywords = ["suicide", "kill myself", "end it", "don't want to be here", "self harm", "hurt myself", "give up on life"]
    is_crisis = any(kw in user_message.lower() for kw in crisis_keywords)

    # Detect if user might benefit from grounding
    anxiety_keywords = ["panic", "anxious", "anxiety", "overwhelmed", "can't breathe", "heart racing", "spiraling", "stressed"]
    needs_grounding = any(kw in user_message.lower() for kw in anxiety_keywords)

    system_prompt = f"""You are Reflect, a warm, deeply empathetic AI mental wellness companion.
You hold space for people's emotions with gentleness and no judgment.
You remember this person's journey and reference it naturally when helpful.

What you remember about them:
{memory_text if memory_text else "This is early in your journey together — learn about them with curiosity."}

Guidelines:
- Speak softly, warmly, and conversationally. No bullet points or lists.
- Validate emotions before offering perspective.
- Reference memories gently and naturally ("I remember you mentioned...")
- If someone seems to be in crisis, respond with compassion and gently point to professional help.
- Never diagnose or prescribe. Never minimize feelings.
- End with ONE soft open question to invite them to share more.
- Keep responses to 3–5 sentences unless more depth is clearly needed.
- Today is {datetime.now().strftime("%A, %B %d, %Y")}.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content

    # Save reply to memory
    mem0.add([
        {"role": "assistant", "content": reply}
    ], user_id=USER_ID)

    return reply, memories, {"is_crisis": is_crisis, "needs_grounding": needs_grounding}


def save_note(heading: str, content: str):
    """Save a user note as a memory."""
    note_text = f"Note titled '{heading}': {content}"
    mem0.add([
        {"role": "user", "content": note_text}
    ], user_id=USER_ID, metadata={
        "timestamp": datetime.now().isoformat(),
        "type": "note",
        "heading": heading
    })
    return True


def log_mood(mood: str):
    """Log the user's current mood as a memory."""
    mem0.add([
        {"role": "user", "content": f"My mood right now is: {mood}"}
    ], user_id=USER_ID, metadata={
        "timestamp": datetime.now().isoformat(),
        "type": "mood",
        "mood": mood
    })


def get_affirmation() -> str:
    """Return a random daily affirmation."""
    return random.choice(AFFIRMATIONS)


def get_journal_prompt() -> str:
    """Return a random reflective journal prompt."""
    return random.choice(JOURNAL_PROMPTS)


def get_grounding_exercise(kind: str = "box-breathing") -> dict:
    """Return a grounding exercise by type."""
    return GROUNDING.get(kind, GROUNDING["box-breathing"])