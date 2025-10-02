4. Add product functionality added:


## ** Adding a Product Without Pydantic**

If you **don’t use Pydantic**, you need to manually read the request body JSON.
It can be done in the following two ways:

### **A) Using async/await (recommended for I/O operations)**
# POST endpoint without Pydantic, using async/await
@app.post("/products")
async def add_product(request: Request):
    data = await request.json()  # manually read JSON from request body
    products.append(data)         # store as-is
    return {"message": "Product added successfully", "product": data}


* `request.json()` is **asynchronous**, so we use `await`.
* This allows FastAPI to **pause while reading the request body** without blocking the server.
* The endpoint can now handle multiple concurrent requests efficiently.
Understand that request.json() is reading the request body and it takes time, so we are using await.

### **B) Without async/await (blocking)**
# POST endpoint without Pydantic, synchronous
@app.post("/products")
def add_product(request: Request):
    body_bytes = request.body()          # returns bytes
    data = json.loads(body_bytes)        # parse JSON manually
    products.append(data)
    return {"message": "Product added successfully", "product": data}

Understand that this blocks the server as we are not using await.
* `request.body()` blocks the server while reading the request — not scalable.
* You still have **no type validation**, so any malformed JSON may crash the app.

Now understand how Pydantic is able to solve the above problems:
## **2️⃣ Adding a Product With Pydantic**

Pydantic automatically parses JSON and validates it. You **don’t need async/await** in the route because FastAPI handles the I/O internally.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

products = []

# Pydantic model
class Product(BaseModel):
    id: int
    name: str
    price: str

# POST endpoint with Pydantic
@app.post("/products")
def add_product(product: Product):
    # convert Pydantic object to dict for storage
    products.append(product.dict())
    return {"message": "Product added successfully", "product": product}
```

Advantages:

1. **Automatic parsing of JSON** — no need to call `request.json()` manually.
2. **Validation** — ensures `id` is int, `name` is str, `price` is str, etc.
3. **Auto-generated docs** (`/docs`) show exactly what JSON to send.
4. **No async/await needed in your function**, even though FastAPI handles async I/O under the hood.
5. **Easier to maintain** — less manual code, less chance of errors.



* **Use Pydantic** whenever possible — it simplifies code, validates data, and integrates with FastAPI docs.
* Use **async/await** if manually reading request body JSON or doing I/O-bound work.
* Without Pydantic, you can still work, but you need **more code** and it’s **less safe and scalable**.


Do you want me to do that?
