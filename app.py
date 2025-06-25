from flask import Flask, render_template, request
from encryption_module import generate_key, encrypt_message, decrypt_message
from otp_sender import send_sms_otp
import base64

app = Flask(__name__)

encrypted_messages = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    message = request.form['message']
    phone = request.form['phone']

    key = generate_key()
    encrypted = encrypt_message(key, message)
    encrypted_b64 = base64.b64encode(encrypted).decode()
    key_b64 = base64.b64encode(key).decode()

    result = send_sms_otp(phone, key_b64)
    encrypted_messages[phone] = encrypted_b64

    return f"""
        <h3>Encrypted Message Sent!</h3>
        <p><strong>Encrypted Text:</strong> {encrypted_b64}</p>
        <p><strong>OTP Sent To:</strong> {phone}</p>
        <p><strong>Delivery Status:</strong> {result['message']}</p>
        <br><a href='/'>Go back</a>
    """

@app.route('/decrypt', methods=['POST'])
def decrypt_message_route():
    otp = request.form['otp']
    encrypted_msg = request.form['encrypted']
    try:
        key = base64.b64decode(otp)
        encrypted = base64.b64decode(encrypted_msg)
        plaintext = decrypt_message(key, encrypted)
        return f"""
            <h3>Decrypted Message:</h3>
            <p>{plaintext}</p>
            <br><a href='/'>Go back</a>
        """
    except Exception as e:
        return f"Error decrypting: {str(e)}<br><a href='/'>Go back</a>"

if __name__ == '__main__':
    app.run(debug=True)
