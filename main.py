import os
from fastapi import FastAPI, Response, Header, HTTPException
from pydantic import BaseModel
import edge_tts

app = FastAPI()

RELAY_SECRET = os.environ.get("RELAY_SECRET", "")


class TTSRequest(BaseModel):
    text: str
    voice: str = "ru-RU-SvetlanaNeural"
    rate: str = "+0%"


@app.get("/")
async def health():
    return {"status": "ok"}


@app.post("/tts")
async def tts(req: TTSRequest, x_api_key: str = Header(default="")):
    if not RELAY_SECRET or x_api_key != RELAY_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    communicate = edge_tts.Communicate(req.text, req.voice, rate=req.rate)
    audio = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
    return Response(content=audio, media_type="audio/mpeg")
