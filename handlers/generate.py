from fastapi import APIRouter
import random, string

router = APIRouter()

@router.post("/generate/token/tg")
async def github_webhook(hash: str) -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(128))