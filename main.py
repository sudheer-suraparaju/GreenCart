from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    id: int
    name: str
    price: str


products = [
    {"id":5347, "name":"Garcinea plant", "price":"$5"},
    {"id":5322, "name":"Chamelia plant", "price":"$4"},
]

@app.get("/")
def read_root():
    return {"message":"GreenCart API is running"}

@app.get("/health")
def read_health():
    return {"status":"OK"}

@app.get("/products")
def fetch_products():
    return {"products":products}


@app.get("/products/{product_id}")
def fetch_product(product_id: int):
    product = products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product": product}

@app.post("/products")
def add_product(product: Product):
    products.append(product.dict())
    return {"message": "Product added successfully", "product": product}