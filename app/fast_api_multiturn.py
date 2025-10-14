from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse

import httpx

app = FastAPI()

DIFY_API_KEY = "app-xxxxxxx" # DifyアプリのAPIキー

DIFY_API_URL = "https://dify-engineers.xvps.jp/v1/chat-messages"

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx


app = FastAPI()


DIFY_API_KEY = "app-xxxxxxx"  # DifyアプリのAPIキー
DIFY_API_URL = "https://dify-engineers.xvps.jp/v1/chat-messages"

# ユーザーごとの会話IDを管理（簡易版: メモリ）
user_conversations = {}


@app.post("/chat")
async def chat_with_dify(request: Request):
	data = await request.json()
	user_id = data.get("user_id", "guest")  # 任意: クライアントから送らせる
	query = data.get("query", "")

	# ユーザーに紐づく conversation_id を取得
	conversation_id = user_conversations.get(user_id)

	async with httpx.AsyncClient(timeout=60.0) as client:
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
				"conversation_id": conversation_id,  # ← 既存があれば文脈継続
				"user": user_id,
			},
		)

	result = resp.json()

	# 新しい conversation_id が返ってきたら保存
	if "conversation_id" in result and result["conversation_id"]:
		user_conversations[user_id] = result["conversation_id"]

	return JSONResponse(
		{
			"answer": result.get("answer", ""),
			"conversation_id": result.get("conversation_id"),
		}
	)