from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

import uvicorn, random, string, subprocess, hashlib, hmac

app = FastAPI()

from pydantic import BaseModel
from orm import User, Session, session
from config import GIT_SECRET

@app.get("/generate/token/tg")
async def generate_auth_token(hash: str) -> str:

    token = ''.join(random.choice(string.ascii_letters + string.digits) for i in range (128))

    return token


@app.get("/git/{secret}")
async def update_git(secret: str, pull: str = None, restart: str = None) -> str:

    if secret != GIT_SECRET:
        raise HTTPException(404)
    
    if pull == '':
        result = subprocess.run("git pull", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout + result.stderr
    
    if restart == '':
        result = subprocess.run("systemctl restart pult", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="cp866")
        text = result.stdout + result.stderr
        return text
    
    return HTMLResponse(open('secret.html', encoding='utf-8').read())

@app.get("/git")
async def github_webhook(request: Request):
    signature = request.headers.get("X-Hub-Signature")
    print(request.headers)
    if signature is None:
        raise HTTPException(status_code=403, detail="Signature header required")

    body = await request.body()
    hash_algorithm, signature_hash = signature.split("=", 1)

    if hash_algorithm != "sha1":
        raise HTTPException(status_code=501, detail="Unsupported hash algorithm")

    hmac_hash = hmac.new(GIT_SECRET.encode(), body, hashlib.sha1).hexdigest()
    if not hmac.compare_digest(signature_hash, hmac_hash):
        raise HTTPException(status_code=403, detail="Invalid signature")

    subprocess.run("git pull", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    return True

app.mount("/", StaticFiles(directory="www", html=True), name="static")



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7742, reload=True)
