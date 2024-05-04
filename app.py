from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

import uvicorn, random, string

app = FastAPI()

from pydantic import BaseModel
from orm import User, Session, session

@app.get("/generate/token/tg")
async def generate_auth_token(hash: str) -> str:

    token = ''.join(random.choice(string.ascii_letters + string.digits) for i in range (128))

    return token

app.mount("/", StaticFiles(directory="www", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7742, reload=True)
