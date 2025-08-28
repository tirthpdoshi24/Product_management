from fastapi import FastAPI, Request
from product_operations import create_category_call, create_product_call, delete_product_call, \
search_product_call, update_product_call, get_products_call, create_bulk_product_call
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


app = FastAPI()

key = b'\xf6\x12+\xbd\x04\xa34T&M\t\n7\xb9\xb4c'


@app.get("/ping")
async def health_check():
    return {"message": "ping"}

@app.get("/generate_token")
async def generate_token():
    return {}

@app.post("/create_category")
async def create_category(request: Request):
    response = {"status":402,"message":"Please check your input parameters"}
    event = await request.json()
    category_name = event.get("category_name","")
    if category_name:
        response = create_category_call(category_name)
    encrypted_response = encrypt_aes(response)
    return encrypted_response

@app.post("/create_product")
async def create_product(request: Request):
    event = await request.json()
    response = create_product_call(event)
    encrypted_response = encrypt_aes(response)
    return encrypted_response

@app.post("/delete_product")
async def delete_product(request: Request):
    event = await request.json()
    response = delete_product_call(event)
    encrypted_response = encrypt_aes(response)
    return encrypted_response

@app.post("/search_product")
async def search_product(request: Request):
    event = await request.json()
    response = str(search_product_call(event))
    # key = get_random_bytes(16)  # For AES-128
    encrypted_response = encrypt_aes(response)
    return encrypted_response

@app.post("/update_product")
async def update_product(request: Request):
    event = await request.json()
    response = str(update_product_call(event))
    # key = get_random_bytes(16)  # For AES-128
    encrypted_response = encrypt_aes(response)
    return encrypted_response

@app.get("/get_products")
async def get_products():
    response = str(get_products_call())
    # key = get_random_bytes(16)  # For AES-128
    encrypted_response = encrypt_aes(response)
    return encrypted_response


@app.post("/create_bulk_product")
async def process_data(request: Request):
    event = await request.json()
    product_number = event.get("product_number","")
    task = create_bulk_product_call.delay(product_number)  # Trigger Celery task asynchronously
    return {"message": "Task submitted", "task_id": task.id}


def encrypt_aes(plaintext):
    # Generate a random 16-byte IV (Initialization Vector)
    iv = get_random_bytes(AES.block_size)

    # Create AES cipher object in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the plaintext to be a multiple of the block size
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)

    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)

    # Combine IV and ciphertext, then base64 encode for safe transmission
    return base64.b64encode(iv + ciphertext).decode('utf-8')