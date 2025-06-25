from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

# Load environment variable (make sure your OpenAI key is set in Render!)
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to generate the roast prompt based on style
def generate_prompt(facts: str, style: str) -> str:
    if style == "Shakespearean":
        return (
            f"Thou must roast this soul in Shakespearean tongue based on the following facts: {facts}"
        )
    elif style == "Drag Queen Sass":
        return (
            f"You are a fabulous drag queen. Roast this person with sass, style, and shade. Be playful, fierce, and over the top. Here are their facts: {facts}"
        )
    else:
        return f"Roast this person brutally but cleverly based on these facts: {facts}"

# Safe Roast endpoint
@app.post("/roast")
async def roast(payload: dict):
    facts = payload.get("facts", "")
    style = payload.get("style", "Brutally Honest")

    # Step 1: Moderate the input
    moderation_response = openai.Moderation.create(input=facts)
    flagged = moderation_response["results"][0]["flagged"]

    if flagged:
        return {
            "roast": "😳 Whoa, your confession was a little too hot for us to handle. Try something cleaner!"
        }

    # Step 2: Create the roast prompt
    prompt = generate_prompt(facts, style)

    # Step 3: Get roast from OpenAI Chat API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
    )

    roast_text = response["choices"][0]["message"]["content"]

    return {"roast": roast_text}


