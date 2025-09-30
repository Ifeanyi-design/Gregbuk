import requests

# Replace with your credentials
TERMI_API_KEY = "YOUR_TERMI_KEY"
TERMI_SENDER_ID = "YOUR_TERMI_SENDER"
AT_USERNAME = "YOUR_AT_USERNAME"
AT_API_KEY = "YOUR_AT_KEY"
AT_SENDER_ID = "YOUR_AT_SENDER"

def send_sms_termii(phone_numbers, message):
    url = "https://termii.com/api/sms/send"
    payload = {
        "to": ",".join(phone_numbers),
        "from": TERMI_SENDER_ID,
        "sms": message,
        "type": "plain",
        "api_key": TERMI_API_KEY
    }
    try:
        r = requests.post(url, json=payload)
        return [{"phone": n, "response": r.json()} for n in phone_numbers]
    except Exception as e:
        return [{"phone": n, "response": {"status": "failed", "error": str(e)}} for n in phone_numbers]


def send_sms_africastalking(phone_numbers, message):
    url = "https://api.africastalking.com/version1/messaging"
    headers = {
        "apikey": AT_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "username": AT_USERNAME,
        "to": ",".join(phone_numbers),
        "message": message,
        "from": AT_SENDER_ID,
        "enqueue": "true"
    }
    try:
        r = requests.post(url, data=data, headers=headers)
        return [{"phone": n, "response": r.json()} for n in phone_numbers]
    except Exception as e:
        return [{"phone": n, "response": {"status": "failed", "error": str(e)}} for n in phone_numbers]


def send_bulk_simultaneously(phone_numbers, message):
    """
    Split numbers in half: first half → Termii, second half → AT.
    Returns combined results.
    """
    mid = len(phone_numbers) // 2
    termii_numbers = phone_numbers[:mid]
    at_numbers = phone_numbers[mid:]

    results = []
    if termii_numbers:
        results.extend(send_sms_termii(termii_numbers, message))
    if at_numbers:
        results.extend(send_sms_africastalking(at_numbers, message))
    return results
