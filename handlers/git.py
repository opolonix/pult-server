from fastapi import APIRouter, Request, HTTPException
import subprocess, hashlib, hmac
from config import GIT_SECRET

router = APIRouter()

@router.post("/git")
async def github_webhook(request: Request):
    signature = request.headers.get("X-Hub-Signature")
    
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