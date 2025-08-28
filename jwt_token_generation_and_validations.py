import secrets

# Generate a random URL-safe text string
# token = secrets.token_urlsafe(32)  # 32 bytes of randomness
# print(f"Generated token: {token}")

import jwt
import datetime

# Define a secret key for signing the token
SECRET_KEY = "abcdefg"
ALGORITHM = "HS256"

# Create a payload with claims
payload = {
    "user_id": 123,
    "username": "example_user",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Expiration time
}

# Encode the token
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print(f"Generated JWT: {token}")

# Assume 'received_token' is the token you received
# Assume 'expected_token' is the token you previously generated and stored
# received_token = "your_received_token_here"
# expected_token = "your_stored_token_here"
#
# if received_token == expected_token:
#     print("Token is valid.")
# else:
#     print("Token is invalid.")
#
import jwt
from jwt.exceptions import InvalidTokenError

# Assume 'received_jwt' is the JWT you received
received_jwt = token#"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiZXhhbXBsZV91c2VyIiwiZXhwIjoxNzU2Mzg0NTM0fQ.sqJtIooIrptvGjLDQ0LMFFM2D-dHNfHqG-rnbL0a1ro"

try:
    # Decode and validate the token
    decoded_payload = jwt.decode(received_jwt, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"JWT is valid. Decoded payload: {decoded_payload}")
except InvalidTokenError as e:
    print(f"JWT validation failed: {e}")
except Exception as e:
    print(f"An unexpected error occurred during JWT validation: {e}")