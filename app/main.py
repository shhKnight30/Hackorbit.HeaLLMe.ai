from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, auth, dashboard, chat
import uvicorn

app = FastAPI(
    title="HeaLLMe.ai API",
    description="24×7 Medical Guidance powered by AI",
    version="1.0.0"
)

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
def read_root():
    return {"message": "🚀 HeaLLMe.ai API is running!"}

# Register routers
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(chat.router, prefix="/chat", tags=["AI Chat"])

# Optional: For direct run
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
