import requests
import certifi
from typing import List, Union, Dict, Any
from flask import current_app
from db import Gateway

REQUEST_TIMEOUT = 10  # seconds
MIN_BALANCE = 500  # Minimum gateway balance in Naira
GATEWAY_LIMITS = {
    "termii": 1000,
    "africastalking": 100,
}


def normalize_number(number: str) -> str:
    """Normalize phone number to international format used by gateways."""
    if not number:
        return number
    n = number.strip()
    if n.startswith("0"):
        return "234" + n[1:]
    if n.startswith("+"):
        return n[1:]
    return n


def chunk_list(data: List[str], size: int) -> List[List[str]]:
    """Split a list into chunks of given size."""
    return [data[i:i + size] for i in range(0, len(data), size)]


def get_gateway_balance(gateway: Gateway) -> float:
    """Check current balance of the gateway in Naira."""
    try:
        name = gateway.name.lower()
        if name == "termii":
            url = f"https://v3.api.termii.com/api/sms/balance?api_key={gateway.api_key}"
            resp = requests.get(url, timeout=REQUEST_TIMEOUT, verify=certifi.where())
            data = resp.json()
            return float(data.get("balance", 0))
        elif name == "africastalking":
            url = "https://api.africastalking.com/version1/user"
            headers = {"apikey": gateway.api_key}
            resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            data = resp.json()
            # Africastalking balance sometimes comes like "KES 1200"
            balance_str = data.get("UserData", {}).get("balance", "0").split()[-1]
            return float(balance_str)
        else:
            current_app.logger.warning(f"Unknown gateway '{gateway.name}' for balance check.")
            return 0
    except Exception as e:
        current_app.logger.error(f"Error fetching balance for {gateway.name}: {e}")
        return 0


def send_sms_via_gateway(
    phone_numbers: Union[str, List[str]],
    message: str,
    gateway: Gateway
) -> Dict[str, Any]:
    """
    Send SMS via a specific gateway and return detailed results.
    Returns:
        {
            "status": "completed"/"failed",
            "results": [ {number, status, raw_status, message_id, error, gateway_name} ],
            "error": None or str,
            "should_retry": True/False
        }
    """
    results: List[Dict[str, Any]] = []
    should_retry = False  # default

    if isinstance(phone_numbers, str):
        phone_numbers = [phone_numbers]

    phone_numbers = [normalize_number(p) for p in phone_numbers]
    gw_name = (gateway.name or "").lower()
    batch_limit = GATEWAY_LIMITS.get(gw_name, 100)

    # 🔹 1. Check gateway balance first
    balance = get_gateway_balance(gateway)
    if balance < MIN_BALANCE:
        current_app.logger.warning(
            f"[{gateway.name}] Insufficient balance ({balance}). Marking all as pending."
        )
        for num in phone_numbers:
            results.append({
                "number": num,
                "status": "pending",
                "raw_status": "insufficient_balance",
                "message_id": None,
                "error": f"Gateway balance too low ({balance})",
                "gateway_name": gateway.name
            })
        return {
            "status": "failed",
            "results": results,
            "error": "Insufficient gateway balance",
            "should_retry": True  # ✅ will retry later when balance is enough
        }

    # 🔹 2. Send in batches
    for batch in chunk_list(phone_numbers, batch_limit):
        try:
            if gw_name == "termii":
                url = "https://v3.api.termii.com/api/sms/send/bulk"
                payload = {
                    "to": ",".join(batch),
                    "from": gateway.sender_id,
                    "sms": message,
                    "type": "plain",
                    "channel": "generic",
                    "api_key": gateway.api_key,
                }
                resp = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT, verify=certifi.where())
                data = resp.json()

                recs = data.get("data", {}).get("message", [])
                if not isinstance(recs, list):
                    recs = [{"to": n, "message_id": data.get("message_id"), "status": data.get("status")} for n in batch]

                for rec in recs:
                    number = normalize_number(rec.get("to", ""))
                    raw_status = str(rec.get("status", "")).lower()
                    status = "sent" if raw_status in ("success", "sent", "queued", "ok") else "failed"
                    results.append({
                        "number": number,
                        "status": status,
                        "raw_status": raw_status,
                        "message_id": rec.get("message_id"),
                        "error": None if status == "sent" else "Gateway error",
                        "gateway_name": gateway.name
                    })

            elif gw_name == "africastalking":
                url = "https://api.africastalking.com/version1/messaging"
                headers = {"apikey": gateway.api_key, "Content-Type": "application/x-www-form-urlencoded"}
                payload = {
                    "username": gateway.username,
                    "to": ",".join(batch),
                    "message": message,
                    "from": gateway.sender_id,
                    "enqueue": "true",
                }
                resp = requests.post(url, data=payload, headers=headers, timeout=REQUEST_TIMEOUT)
                data = resp.json()
                recipients = data.get("SMSMessageData", {}).get("Recipients", [])

                if not recipients:
                    for num in batch:
                        results.append({
                            "number": num,
                            "status": "failed",
                            "raw_status": "no_response",
                            "message_id": None,
                            "error": "No recipients in response",
                            "gateway_name": gateway.name
                        })
                else:
                    for rec in recipients:
                        number = normalize_number(rec.get("number", ""))
                        raw_status = str(rec.get("status", "")).lower()
                        status = "sent" if raw_status in ("success", "sent", "queued", "ok") else "failed"
                        results.append({
                            "number": number,
                            "status": status,
                            "raw_status": raw_status,
                            "message_id": rec.get("messageId"),
                            "error": None if status == "sent" else "Gateway error",
                            "gateway_name": gateway.name
                        })
            else:
                for num in batch:
                    results.append({
                        "number": num,
                        "status": "failed",
                        "raw_status": "unknown_gateway",
                        "message_id": None,
                        "error": f"Unknown gateway '{gateway.name}'",
                        "gateway_name": gateway.name
                    })

        except requests.exceptions.Timeout:
            current_app.logger.warning(f"[{gateway.name}] Timeout occurred. Retrying later...")
            should_retry = True
            for num in batch:
                results.append({
                    "number": num,
                    "status": "retrying",
                    "raw_status": "timeout",
                    "message_id": None,
                    "error": "Request timed out",
                    "gateway_name": gateway.name
                })

        except Exception as e:
            current_app.logger.error(f"[{gateway.name}] Error during send: {e}")
            should_retry = True  # retry only for network/gateway failure
            for num in batch:
                results.append({
                    "number": num,
                    "status": "retrying",
                    "raw_status": "error",
                    "message_id": None,
                    "error": str(e),
                    "gateway_name": gateway.name
                })

    overall_status = "completed" if all(r["status"] == "sent" for r in results) else "failed"
    return {
        "status": overall_status,
        "results": results,
        "error": None,
        "should_retry": should_retry
    }
