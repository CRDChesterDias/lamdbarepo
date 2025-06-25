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

# ==== DATE FILTER (UTC today) ====
today = datetime.datetime.utcnow().date()
start_time = f"{today} 00:00:00"
end_time = f"{today + datetime.timedelta(days=1)} 00:00:00"

# ==== QUERY: Remove location filter ====
query = (
    f"opened_by.nameLIKE{USER_NAME}^"
    f"opened_at>={start_time}^"
    f"opened_at<{end_time}"
)

# ==== FIELDS TO FETCH ====
fields = [
    "number",
    "short_description",
    "description",
    "cmdb_ci",
    "subcategory",
    "priority",
    "impact",
    "urgency",
    "assignment_group",
    "state",
    "opened_at",
    "opened_by"
]

# ==== FETCH INCIDENTS ====
print("[*] Fetching incident data...")
response = requests.get(
    BASE_URL,
    auth=(USERNAME, PASSWORD),
    headers=HEADERS,
    params={
        "sysparm_query": query,
        "sysparm_fields": ",".join(fields),
        "sysparm_limit": 1000,
        "sysparm_display_value": "true"
    }
)

if response.status_code != 200:
    print(f"[!] Error: {response.status_code} - {response.text}")
    exit()

incidents = response.json().get("result", [])

if not incidents:
    print("[!] No incidents found.")
    exit()

print(f"[+] Retrieved {len(incidents)} incident(s)")

# ==== WRITE TO EXCEL ====
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Incidents"

# Write header row
ws.append(fields)

# Helper to extract readable values
def clean(value):
    if isinstance(value, dict):
        return value.get("display_value") or value.get("value") or ""
    return str(value)

# Write each row of data
for incident in incidents:
    row = [clean(incident.get(field, "")) for field in fields]
    ws.append(row)

# Save the file
filename = f"incidents_opened_{today}.xlsx"
wb.save(filename)
print(f"[✓] Data saved to {filename}")
