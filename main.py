import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Set Constants
API_URL = os.getenv('API_URL')
SITE_URL = os.getenv('SITE_URL')
SITE_KEY = os.getenv('SITE_KEY')

LICENSE_FILE = os.getenv('LICENSE_FILE')
CAPSOLVER_API_KEY = os.getenv('CAPSOLVER_API_KEY')
PROXY_URL = os.getenv('PROXY_URL')

# Extract proxy details
proxy_type = 'http'
proxy_scheme, proxy_address = PROXY_URL.split('://')
proxy_credentials, proxy_host_port = proxy_address.split('@')
proxy_username, proxy_password = proxy_credentials.split(':')
proxy_host, proxy_port = proxy_host_port.split(':')

existing_licenses = set()

# Set inital session
def get_initial_jsessionid():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    proxies = {
        "http": PROXY_URL,
        "https": PROXY_URL
    }
    session = requests.Session()
    try:
        response = session.get(SITE_URL, headers=headers, proxies=proxies)
        response.raise_for_status()
        for cookie in session.cookies:
            if cookie.name == "JSESSIONID":
                return cookie.value
    except requests.RequestException:
        print("Failed to get JSESSIONID")
        pass
    return None