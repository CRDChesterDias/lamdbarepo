import requests
import datetime
import openpyxl

# ==== CONFIGURATION ====
SN_INSTANCE = "your_instance"  # e.g., dev12345
USERNAME = "your_username"
PASSWORD = "your_password"

USER_NAME = "Tim"  # Partial match on opened_by.name
LOCATIONS = ["New York", "San Francisco"]  # Replace with actual location names

BASE_URL = f"https://{SN_INSTANCE}.service-now.com/api/now/table/incident"
HEADERS = {
    "Accept": "application/json"
}

# ==== FILTER: Today + Opened By "Tim" + 2 Locations ====
today = datetime.datetime.utcnow().date().isoformat()
query = (
    f"opened_by.nameLIKE{USER_NAME}^"
    f"sys_created_onON{today}^"
    f"location.nameIN{','.join(LOCATIONS)}"
)

# ==== FETCH INCIDENTS ====
print("[*] Fetching incident data...")
response = requests.get(
    BASE_URL,
    auth=(USERNAME, PASSWORD),
    headers=HEADERS,
    params={"sysparm_query": query, "sysparm_limit": 1000}
)

if response.status_code != 200:
    print(f"[!] Error: {response.status_code} - {response.text}")
    exit()

incidents = response.json()["result"]

if not incidents:
    print("[!] No incidents found.")
    exit()

print(f"[+] Retrieved {len(incidents)} incident(s)")

# ==== CREATE EXCEL FILE ====
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Incidents"

# Write header
headers = list(incidents[0].keys())
ws.append(headers)

# Write data
for record in incidents:
    row = [record.get(key, "") for key in headers]
    ws.append(row)

# Save to file
filename = f"incidents_{today}.xlsx"
wb.save(filename)

print(f"[✓] Data saved to {filename}")
