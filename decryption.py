from Crypto.Cipher import AES
from Crypto.Util.Padding import  unpad
import base64


def decrypt_aes(encrypted_text, key):
    # Base64 decode the encrypted text
    decoded_text = base64.b64decode(encrypted_text)

    # Extract IV and ciphertext
    iv = decoded_text[:AES.block_size]
    ciphertext = decoded_text[AES.block_size:]

    # Create AES cipher object for decryption
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext
    decrypted_padded_plaintext = cipher.decrypt(ciphertext)

    # Unpad the decrypted plaintext and decode to string
    return unpad(decrypted_padded_plaintext, AES.block_size).decode('utf-8')


encrypted_response= """HCmKaz9GOP6adZeJf/iT1LMcJYRQgaEFEGdAJvh2daDN53LVf9T2Z9ucvfufbwooJR0jVGWs5Bkycfjlt8xiGkeYS6+fTaYqNqkanys8UJKLh/HGJQ8sBA9CGNo03iXGWcP8UJkvnAhhfugGbfcBdNStDRZT+pn7/ndGvZD4StYMRtOYIdo4
i9cyJ0l40ISGL58n3e3G+9C58AbsPxdKWcortFKz5aREbj0kuTmqJK72yChXcELnNLNkudbdSGKdeRKJS2RPwdaVGvdxkS7fjHrxWiMDd1HQwWPm4SFDtqm0s39CDAhls/lxdFuLKl7NAuO2T+AI45hNfOpMwaCVu4B64NRFTtgEhTvRJO8Ul4U0XJMdrRzC3dO8l2ICYWUa
"""
# Decrypt the response (for verification)
decrypted_response = decrypt_aes(encrypted_response, key)
print(f"Decrypted Response: {decrypted_response}")