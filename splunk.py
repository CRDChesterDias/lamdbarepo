import ssl
import socket
import json
import requests
from datetime import datetime

# Splunk HEC Configuration
SPLUNK_HEC_URL = "https://your-splunk-server:8088"  # Change this to your Splunk instance
SPLUNK_HEC_TOKEN = "your_hec_token"  # Replace with your actual HEC token
SPLUNK_INDEX = "web_monitor"
SPLUNK_SOURCETYPE = "ssl_monitor"

# List of URLs to monitor (Add your domains here)
URLS = [
    "example.com",
    "yourdomain.com",
    "anotherdomain.com"
]

def get_ssl_details(hostname, port=443):
    """Fetch SSL certificate details and expiry information."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

                # Extract certificate details
                expiry_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                days_left = (expiry_date - datetime.utcnow()).days
                issuer = dict(x[0] for x in cert['issuer'])
                subject = dict(x[0] for x in cert['subject'])

                return {
                    "url": hostname,
                    "ssl_expiry_days": days_left,
                    "ssl_expiry_date": expiry_date.strftime("%Y-%m-%d"),
                    "issuer": issuer.get("organizationName", "Unknown"),
                    "subject": subject.get("commonName", "Unknown"),
                    "status": "valid" if days_left > 0 else "expired"
                }
    except Exception as e:
        return {
            "url": hostname,
            "error": str(e),
            "status": "error"
        }

def send_to_splunk(event_data):
    """Send JSON data to Splunk via HTTP Event Collector (HEC)."""
    headers = {
        "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "event": event_data,
        "sourcetype": SPLUNK_SOURCETYPE,
        "index": SPLUNK_INDEX
    }
    
    try:
        response = requests.post(f"{SPLUNK_HEC_URL}/services/collector", headers=headers, json=payload, verify=False)
        if response.status_code != 200:
            print(f"Error sending to Splunk: {response.text}")
    except Exception as e:
        print(f"HEC Connection Error: {str(e)}")

# Main Execution
if __name__ == "__main__":
    ssl_data = [get_ssl_details(url) for url in URLS]
    
    for event in ssl_data:
        print(json.dumps(event, indent=2))  # Optional: Print output for debugging
        send_to_splunk(event)
