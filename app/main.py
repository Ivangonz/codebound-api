from fastapi import FastAPI
from app.core.config import settings
from app.core.cors import add_cors

app = FastAPI(title=settings.APP_NAME)
add_cors(app)

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello(name: str = "world"):
    return {"message": f"hello, {name}"}
