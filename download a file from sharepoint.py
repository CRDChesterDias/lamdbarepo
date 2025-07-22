from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
import os

# SharePoint site and app credentials
site_url = "https://yourtenant.sharepoint.com/sites/yoursite"
client_id = "your-client-id"
client_secret = "your-client-secret"

# Path of file in document library
sharepoint_file_url = "/sites/yoursite/Shared Documents/yourfile.pdf"

# Local path to save the file
download_path = os.path.join(os.getcwd(), "yourfile.pdf")

# Authenticate
ctx = ClientContext(site_url).with_credentials(ClientCredential(client_id, client_secret))

# Load and download the file
response = ctx.web.get_file_by_server_relative_url(sharepoint_file_url).download(download_path).execute_query()

print(f"File downloaded successfully to {download_path}")
