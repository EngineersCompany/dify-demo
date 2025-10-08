from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os

app = FastAPI()

# ====== 静的ファイル (HTML/JS/CSS) の公開設定 ======
BASE_DIR = os.path.dirname(__file__)
app.mount("/", StaticFiles(directory=BASE_DIR, html=True), name="static")

# ====== Dify API 呼び出しエンドポイント ======
DIFY_API_KEY = "app-OdQuKp1wWB2ff9PVhdVltuUi"  # ← 実際のキー
DIFY_API_URL = "https://dify-engineers.xvps.jp/v1/chat-messages"

@app.post("/ask")
async def ask_dify(request: Request):
    data = await request.json()
    user_query = data.get("query", "")

    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(
            DIFY_API_URL,
            headers={
                "Authorization": f"Bearer {DIFY_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "inputs": {},
                "query": user_query,
                "response_mode": "blocking",
                "conversation_id": None,
                "user": "fastapi_demo_user"
            }
        )

    result = resp.json()
    return JSONResponse({"answer": result.get("answer", "No response")})
