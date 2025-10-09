from fastapi import FastAPI
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
#from fastapi.responses import PlainTextResponse
import json

app = FastAPI()
# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要なら ["https://www.engineers.co.jp"] などに制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ダミー在庫データ
inventory_data = {
    "Aフランジ": {"stock": 120, "next_arrival": "2025-10-15"},
    "Bシャフト": {"stock": 50, "next_arrival": "2025-10-20"},
    "Cプレート": {"stock": 0, "next_arrival": "2025-11-01"},
    "ABC": {"stock": 100, "next_arrival": "2025-12-01"}
}

@app.get("/api/inventory")
def get_inventory(product: Optional[str] = None):
    if product and product in inventory_data:
        return {
            "product": product,
            "stock": inventory_data[product]["stock"],
            "next_arrival": inventory_data[product]["next_arrival"],
            "error": None
        }
    else:
        return {
            "product": product,
            "stock": 0,
            "next_arrival": None,
            "error": "製品が見つかりません"
        }