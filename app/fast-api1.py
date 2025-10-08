from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

DIFY_API_KEY = "app-OdQuKp1wWB2ff9PVhdVltuUi"  # DifyのAPIキー
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

    # answerだけを返したい場合
    return JSONResponse({"answer": result.get("answer", "No response")})
