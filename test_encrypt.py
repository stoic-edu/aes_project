from encryption_module import generate_key, encrypt_message, decrypt_message
from otp_sender import send_sms_otp
import base64

# Step 1: Generate AES key
key = generate_key()

# Step 2: Define the message
plaintext = "Hello, this is a test message."

# Step 3: Encrypt
cipher = encrypt_message(key, plaintext)

# Step 4: Decrypt
decrypted = decrypt_message(key, cipher)

# Step 5: Convert key to base64 (so it's safe for SMS)
key_b64 = base64.b64encode(key).decode()

# Step 6: Send AES key via SMS
send_sms_otp("+2547XXXXXXXX", key_b64)

# Step 7: Output results
print("Original Message:", plaintext)
print("Encrypted (Base64):", base64.b64encode(cipher).decode())
print("Decrypted Message:", decrypted)
