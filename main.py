from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 Load your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Input model
class RoastRequest(BaseModel):
    facts: str
    style: str = "Drag Queen Sass"

# 🚫 Profanity Filter
BANNED_WORDS = {
    "fuck", "shit", "bitch", "asshole", "cunt", "dick", "pussy", "nigger", "fag",
    "slut", "whore", "rape", "kill", "terrorist", "suicide", "nazi", "hitler"
}

def contains_banned_words(text: str) -> bool:
    words = re.findall(r"\b\w+\b", text.lower())
    return any(word in BANNED_WORDS for word in words)

# 🔥 Roast Endpoint
@app.post("/roast")
async def roast(request: RoastRequest):
    if contains_banned_words(request.facts):
        return {"roast": "❌ Sorry, keep it clean! No inappropriate words allowed."}

    prompt = f"Roast this person in the style of {request.style}: {request.facts}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )
        roast_text = response["choices"][0]["message"]["content"]
        return {"roast": roast_text}

    except Exception as e:
        return {"roast": "🚨 Error generating roast. Please try again later."}



