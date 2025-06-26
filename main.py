from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import re

# 🔐 Load OpenAI key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🚀 Init FastAPI app
app = FastAPI()

# 🌐 Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now; tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request body model
class RoastRequest(BaseModel):
    facts: str
    style: str = "Drag Queen Sass"
    intensity: str = "medium"  # New: light / medium / savage

# 🚫 Banned words list
BANNED_WORDS = {
    "fuck", "shit", "bitch", "asshole", "cunt", "dick", "pussy", "nigger", "fag",
    "slut", "whore", "rape", "kill", "terrorist", "suicide", "nazi", "hitler"
}

# 🧠 Banned word checker
def contains_banned_words(text: str) -> bool:
    words = re.findall(r"\b\w+\b", text.lower())
    for word in words:
        if word in BANNED_WORDS:
            print(f"🚫 Banned word detected: {word}")  # Debug
            return True
    return False

# 🔥 POST /roast endpoint
@app.post("/roast")
async def roast(request: RoastRequest):
    if contains_banned_words(request.facts):
        return {"roast": "❌ Sorry, keep it clean! No inappropriate words allowed."}

    # 🧂 Intensity tone mapping
    if request.intensity == "light":
        tone = "light and playful, like a soft tease"
    elif request.intensity == "savage":
        tone = "savage, witty, and brutally hilarious — but still clean"
    else:
        tone = "funny and edgy, but not mean"

    # 🧠 AI prompt
    prompt = (
        f"You are an AI roasting comedian. The user's facts are: \"{request.facts}\".\n"
        f"Roast them in the style of {request.style} with a tone that is {tone}. "
        f"Keep it under 50 words. Make it clever, clean, and original."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )
        roast_text = response["choices"][0]["message"]["content"]
        return {"roast": roast_text}

    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        return {"roast": "🚨 Error generating roast. Please try again later."}


    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        return {"roast": "🚨 Error generating roast. Please try again later."}


