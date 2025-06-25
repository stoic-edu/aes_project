import africastalking

# Initialize SDK
username = "sandbox"  # Change to your actual username for production
api_key = "atsk_25300a72fdb618d6c3a0c45cdd90562c56860afa9df35891be053c200c01cc95e25f03f7"

# Initialize the SDK
africastalking.initialize(username, api_key)

# Get SMS service
sms = africastalking.SMS

# Sandbox test numbers that actually work
SANDBOX_TEST_NUMBERS = [
    "+254711082300",
    "+254733000001", 
    "+254711000000"
   
]

def send_sms_otp(phone_number, key_b64, use_sandbox_number=True):
    """
    Send SMS with AES key
    
    Args:
        phone_number: Original phone number (for logging/reference)
        key_b64: Base64 encoded AES key
        use_sandbox_number: If True, uses test number for sandbox mode
    """
    try:
        # For sandbox mode, use test number instead of real number
        if username == "sandbox" and use_sandbox_number:
            actual_phone = SANDBOX_TEST_NUMBERS[0]  # Use first test number
            print(f"📱 Sandbox Mode: Using test number {actual_phone} instead of {phone_number}")
        else:
            actual_phone = phone_number
            if not actual_phone.startswith("+"):
                actual_phone = "+" + actual_phone
        
        message = f"Your AES OTP key: {key_b64}"
        
        # Send SMS
        response = sms.send(message, [actual_phone])
        
        # Check response
        if response['SMSMessageData']['Recipients']:
            recipient = response['SMSMessageData']['Recipients'][0]
            if recipient['status'] == 'Success':
                print(f"✅ SMS sent successfully to {actual_phone}")
                print(f"💰 Cost: {recipient.get('cost', 'N/A')}")
                return {
                    'success': True,
                    'message': f'SMS sent to {actual_phone}',
                    'response': response
                }
            else:
                print(f"❌ SMS failed: {recipient['status']}")
                return {
                    'success': False,
                    'message': f'SMS failed: {recipient["status"]}',
                    'response': response
                }
        else:
            return {
                'success': False,
                'message': 'No recipients in response',
                'response': response
            }
            
    except Exception as e:
        print(f"SMS Error: {e}")
        return {
            'success': False,
            'message': f'SMS Error: {str(e)}',
            'response': None
        }

def get_sandbox_numbers():
    """Return list of valid sandbox test numbers"""
    return SANDBOX_TEST_NUMBERS.copy()

# Test function
if __name__ == "__main__":
    test_key = "E0coe7hYWEyxENclgPqFT6T8tEss1hGkHvTbEVTtAH8="
    result = send_sms_otp("+254728915387", test_key)
    print("Result:", result)