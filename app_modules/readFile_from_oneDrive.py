import os
import json
import requests
from msal import ConfidentialClientApplication
from urllib.parse import quote
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
FILE_LINK = os.getenv("FILE_LINK")

# Step 1: Setup MS Graph API authentication
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ['https://graph.microsoft.com/.default']
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

# Step 2: Get access token using MSAL
app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY
)

token_response = app.acquire_token_for_client(scopes=SCOPE)
if "access_token" not in token_response:
    raise Exception("Could not obtain access token")

access_token = token_response["access_token"]

# Step 3: Convert shared URL to encoded form and get drive item
# Remove query parameters for clean encoding
base_url = FILE_LINK.split('?')[0]
encoded_url = quote(base_url, safe='')

response = requests.get(
    f"{GRAPH_API_ENDPOINT}/shares/u!{encoded_url}/driveItem",
    headers={"Authorization": f"Bearer {access_token}"}
)

if response.status_code != 200:
    raise Exception(f"Failed to get metadata: {response.text}")

item_data = response.json()
download_url = item_data.get('@microsoft.graph.downloadUrl')

if not download_url:
    raise Exception("Download URL not found in response.")

# Step 4: Download and parse the JSON file
file_response = requests.get(download_url)
json_data = file_response.json()

# Output the parsed JSON
print(json.dumps(json_data, indent=2))
