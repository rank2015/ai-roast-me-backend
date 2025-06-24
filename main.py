import openai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace * with your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/roast")
async def roast(request: Request):
    data = await request.json()
    user_input = data.get("facts")
    style = data.get("style")

    prompts = {
        "Brutally Honest": f"You are a brutally honest AI roast comedian. A user has submitted the following personal facts:\n{user_input}\n\nGenerate a short roast in a brutally honest tone. Use sarcasm, clever burns, and light mockery, but avoid being mean or offensive. Keep it under 50 words. End with a savage punchline. Output only the roast.",
        "Shakespearean": f"You are William Shakespeare reincarnated as a roast comedian. A user has submitted the following personal facts:\n{user_input}\n\nCraft a clever insult in Shakespearean English. Use flowery language, archaic insults, and poetic phrasing. Keep it under 60 words. It should be insulting but witty and theatrical. Output only the roast.",
        "Drag Queen Sass": f"You are a drag queen roasting someone on stage. A user has submitted the following personal facts:\n{user_input}\n\nDeliver a sassy, fabulous roast full of wit, flair, and style. Keep it playful, fierce, and full of personality. No profanity. Keep it under 50 words. Output only the roast, darling."
    }

    prompt = prompts.get(style, prompts["Brutally Honest"])

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )

    return {"roast": response["choices"][0]["message"]["content"]}
