from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


# FastAPI app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client
client = OpenAI(
    api_key=os.getenv("NEXUS_API_KEY"),
    base_url="https://apidev.navigatelabsai.com"
)

# Request model
class PromptRequest(BaseModel):
    user_prompt: str

# Health check
@app.get("/")
def read_root():
    return {"message": "NexusAI is working"}

@app.get("/welcome")
def welcome():
    return {"message": "Welcome to Navi Chat"}

# AI endpoint
@app.post("/run_task")
async def run_task(req: PromptRequest):
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a personal AI tutor. "
                        "Explain everything in simple layman terms. "
                        "Keep responses short, precise, and factual."
                    )
                },
                {
                    "role": "user",
                    "content": req.user_prompt
                }
            ]
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}