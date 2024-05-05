from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn
from tools.routers import include_routers

app = FastAPI()
include_routers(app, "handlers")

app.mount("/", StaticFiles(directory="www", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7742, reload=True)