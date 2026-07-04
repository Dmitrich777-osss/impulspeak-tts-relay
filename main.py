from fastapi import FastAPI, Response
from pydantic import BaseModel
import edge_tts

app = FastAPI()


class TTSRequest(BaseModel):
    text: str
    voice: str = "ru-RU-SvetlanaNeural"
    rate: str = "+0%"


@app.get("/")
async def health():
    return {"status": "ok"}


@app.post("/tts")
async def tts(req: TTSRequest):
    communicate = edge_tts.Communicate(req.text, req.voice, rate=req.rate)
    audio = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
    return Response(content=audio, media_type="audio/mpeg")
