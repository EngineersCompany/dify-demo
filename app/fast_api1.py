from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os

app = FastAPI()

# ====== 静的ファイルの公開設定 ======
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # 上の階層に static を置く
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# ====== Dify API 呼び出しエンドポイント ======
DIFY_API_KEY = "app-GQxRhEKjX2qItaE733kNMIOH"
DIFY_API_URL = "https://dify-engineers.xvps.jp/v1/chat-messages"

@app.post("/ask")
async def ask_dify(request: Request):
    data = await request.json()
    query = data.get("query", "")

    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(
            DIFY_API_URL,
            headers={
                "Authorization": f"Bearer {DIFY_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "inputs": {},
                "query": query,
                "response_mode": "blocking",
                "conversation_id": None,
                "user": "fastapi_demo_user"
            }
        )

    result = resp.json()
    print(result)
    return JSONResponse({"answer": result.get("answer", "No response")})
