# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from checker import check_status, load_urls
import json
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def get_status():
    try:
        urls = load_urls("../urls.txt")
        status = check_status(urls)
        return status
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
