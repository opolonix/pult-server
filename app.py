from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

import uvicorn

app = FastAPI()

app.mount("/", StaticFiles(directory="www", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7742, reload=True)
