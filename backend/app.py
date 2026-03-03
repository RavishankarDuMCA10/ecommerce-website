from fastapi import FastAPI
from routes.authRoute import router as AuthRouter

# Create a FastAPI instance
app = FastAPI()

# Routes
app.include_router(AuthRouter)


@app.get("/", tags=["health"])
def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {"msg": "Server is up and running!"}
