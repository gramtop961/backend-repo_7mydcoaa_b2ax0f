import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Shopping AI Assistant Backend"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# -------- Shopping Assistant endpoints --------
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class RetailerOption(BaseModel):
    name: str
    price: float
    url: Optional[str] = None
    is_best: bool = False

class ProductCard(BaseModel):
    id: str
    title: str
    price: float
    rating: float
    image: Optional[str] = None
    specs: List[str] = []
    retailers: List[RetailerOption] = []
    why: Optional[str] = None

class ChatResponse(BaseModel):
    summary: str
    recommendations: List[ProductCard]
    tips: List[str] = []

@app.post("/api/assist", response_model=ChatResponse)
async def assist(req: ChatRequest):
    """Mock AI assistant that returns structured shopping suggestions.
    In real usage, connect to an LLM provider and your product catalog.
    """
    q = req.message.lower()
    # Simple mocked logic
    if "headphones" in q or "earbuds" in q:
        recs = [
            ProductCard(
                id="p1",
                title="Sony WH-1000XM5",
                price=348.00,
                rating=4.8,
                image="https://images.unsplash.com/photo-1585386959984-a41552231665?q=80&w=1200&auto=format&fit=crop",
                specs=["ANC", "30h battery", "Multipoint"],
                retailers=[
                    RetailerOption(name="Amazon", price=348.0, url="https://amazon.com", is_best=True),
                    RetailerOption(name="BestBuy", price=349.0, url="https://bestbuy.com"),
                ],
                why="Best-in-class ANC with balanced tuning and comfort.",
            ),
            ProductCard(
                id="p2",
                title="Bose QuietComfort Ultra",
                price=379.00,
                rating=4.7,
                image="https://images.unsplash.com/photo-1518444028785-8cdc4e4458f0?q=80&w=1200&auto=format&fit=crop",
                specs=["Immersive Audio", "Great comfort", "Clear calls"],
                retailers=[
                    RetailerOption(name="Bose", price=379.0, url="https://bose.com"),
                    RetailerOption(name="Target", price=369.0, url="https://target.com", is_best=True),
                ],
                why="Superb comfort, lush sound, strong ANC.",
            ),
        ]
        summary = "I compared top noise-canceling headphones prioritizing comfort, ANC strength, and value. Here are your best picks."
        tips = [
            "If you commute, prioritize ANC and comfort.",
            "Multipoint is useful if you switch between laptop and phone.",
            "Consider refurbished to save 15-25%.",
        ]
    else:
        recs = [
            ProductCard(
                id="g1",
                title="Apple AirTag (4-pack)",
                price=79.00,
                rating=4.9,
                image="https://images.unsplash.com/photo-1617957743090-4f7fc5ad83b5?q=80&w=1200&auto=format&fit=crop",
                specs=["Find My network", "Replaceable battery"],
                retailers=[
                    RetailerOption(name="Apple", price=99.0, url="https://apple.com"),
                    RetailerOption(name="Amazon", price=79.0, url="https://amazon.com", is_best=True),
                ],
                why="Effortless tracking within Apple ecosystem.",
            )
        ]
        summary = "Here’s a smart everyday pick with excellent value and ecosystem benefits."
        tips = ["Bundle with a keyring holder."]

    return ChatResponse(summary=summary, recommendations=recs, tips=tips)

class TrendItem(BaseModel):
    title: str
    category: str
    product_id: Optional[str] = None

@app.get("/api/trending", response_model=List[TrendItem])
async def trending():
    # Mocked trending items; replace with DB query later
    return [
        TrendItem(title="Ultra ANC Headphones", category="Audio"),
        TrendItem(title="AI-ready Laptops", category="Computers"),
        TrendItem(title="Smart Home Essentials", category="Home"),
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
