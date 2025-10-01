from fastapi import FastAPI

app = FastAPI()

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