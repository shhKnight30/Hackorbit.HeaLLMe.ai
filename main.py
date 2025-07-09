from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="HeaLLMe.ai API",
    description="24×7 Medical Guidance powered by AI",
    version="1.0.0"
)

# Simple CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    print("hello world")
    return {"message": "HeaLLMe.ai API - Initial setup done"}