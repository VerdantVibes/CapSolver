import os
from dotenv import load_dotenv

load_dotenv()

# Set Constants
API_URL = os.getenv('API_URL')
SITE_URL = os.getenv('SITE_URL')
SITE_KEY = os.getenv('SITE_KEY')

LICENSE_FILE = os.getenv('LICENSE_FILE')
CAPSOLVER_API_KEY = os.getenv('CAPSOLVER_API_KEY')
PROXY_URL = os.getenv('PROXY_URL')
