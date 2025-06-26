from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Enable CORS so frontend can access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can tighten this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/roast")
async def roast(request: Request):
    body = await request.json()
    facts = body.get("facts", "")
    style = body.get("style", "Drag Queen Sass")

    prompt = f"You are an AI roast comic. Roast this person in the style of {style}. Here are their facts: {facts}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
    )

    roast_text = response["choices"][0]["message"]["content"]
    return {"roast": roast_text}


