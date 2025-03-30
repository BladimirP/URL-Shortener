from dotenv import load_dotenv
load_dotenv()
from app.routes import router
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    host = os.getenv("API_HOST")
    port = int(os.getenv("API_PORT"))
    uvicorn.run(app, host=host, port=port)