from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, youtube

app = FastAPI(
    title="YT Recommender",
    description="YouTube recommendation engine via OAuth",
    version="0.1.0"
)

# ── Middleware ────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(youtube.router)


@app.get("/")
def root():
    return {"message": "YT Recommender API — visit /docs"}