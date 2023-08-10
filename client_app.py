import msal
import logging
from urllib.parse import urlencode

# Configuration
AZURE_AD_AUTHORITY = "https://login.microsoftonline.com/<tenant-id>"
AZURE_AD_CLIENT_ID = ""
AZURE_AD_CLIENT_SECRET = ""
AZURE_AD_REDIRECT_URI = "http://localhost:8000/get_token/"
AZURE_AD_SCOPE = ["User.Read"]  # Adjust scope as needed



# Logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    username = ""  # Replace with actual email
    password = ""  # Replace with actual password

    # Acquire token using MSAL
    msal_app = msal.ConfidentialClientApplication(
        AZURE_AD_CLIENT_ID,
        client_credential=AZURE_AD_CLIENT_SECRET,
        authority=AZURE_AD_AUTHORITY
    )
    
    result = msal_app.acquire_token_by_username_password(
        username,
        password,
        scopes=AZURE_AD_SCOPE
    )

    logger.debug("Token acquisition result:", result)

    if 'error' in result:
        logger.error(f"Token acquisition error: {result.get('error_description', 'Unknown error')}")
        print("Token acquisition error:", result.get('error_description', 'Unknown error'))
        return

    if 'access_token' in result:
        access_token = result['access_token']
        print("Access token:", access_token)

if __name__ == "__main__":
    main()











