from ldap3 import Server, Connection, ALL, SUBTREE
import csv

# LDAP server settings
LDAP_SERVER = 'ldap://your.domain.controller'  # e.g., ldap://dc01.yourdomain.com
USERNAME = 'YOUR_DOMAIN\\your_username'        # Domain credentials
PASSWORD = 'your_password'
BASE_DN = 'DC=yourdomain,DC=com'               # Your AD base DN

# Connect to server
server = Server(LDAP_SERVER, get_info=ALL)
conn = Connection(server, user=USERNAME, password=PASSWORD, auto_bind=True)

# LDAP filter to get all user objects
search_filter = '(&(objectClass=user)(objectCategory=person))'
attributes = ['cn', 'sAMAccountName', 'mail', 'userPrincipalName', 'distinguishedName']

# Perform the search
conn.search(search_base=BASE_DN,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=attributes)

# Export to CSV
with open('ad_users.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(attributes)  # Header

    for entry in conn.entries:
        row = [entry[attr].value if attr in entry else '' for attr in attributes]
        writer.writerow(row)

print(f"✅ Exported {len(conn.entries)} AD users to 'ad_users.csv'.")

# Unbind connection
conn.unbind()
