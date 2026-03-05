from fastapi import FastAPI
from routes.authRoute import router as AuthRouter
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI instance
app = FastAPI()

# CORS ERROR
app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
)

# Routes
app.include_router(AuthRouter)


@app.get("/", tags=["health"])
def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {"msg": "Server is up and running!"}
