from flask import Flask, render_template, request, redirect
from encryption_module import generate_key, encrypt_message, decrypt_message
from otp_sender import send_sms_otp
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def encrypt_ui():
    if request.method == 'POST':
        message = request.form['message']
        phone = request.form['phone']
        key = generate_key()
        encrypted = encrypt_message(key, message)

        # Convert to Base64
        key_b64 = base64.b64encode(key).decode()
        cipher_b64 = base64.b64encode(encrypted).decode()

        # Send key via SMS
        send_sms_otp(phone, key_b64)

        return render_template('encrypt.html', message=message, cipher=cipher_b64)
    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_ui():
    result = None
    if request.method == 'POST':
        try:
            cipher = base64.b64decode(request.form['cipher'])
            key = base64.b64decode(request.form['otp'])
            plaintext = decrypt_message(key, cipher)
            result = f"Decrypted Message: {plaintext}"
        except:
            result = "❌ Decryption failed. Check OTP or message."
    return render_template('decrypt.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
