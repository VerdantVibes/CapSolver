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

def create_captcha_task():
    task_data = {
        'clientKey': CAPSOLVER_API_KEY,
        'task': {
            'type': 'RecaptchaV3EnterpriseTask',
            'websiteURL': SITE_URL,
            'websiteKey': SITE_KEY,
            'proxyType': proxy_scheme,
            'proxyAddress': proxy_host,
            'proxyPort': int(proxy_port),
            'proxyLogin': proxy_username,
            'proxyPassword': proxy_password,
        }
    }

    response = requests.post('https://api.capsolver.com/createTask', json=task_data)
    response_data = response.json()

    if response.status_code == 200 and response_data.get("errorId") == 0:
        return response_data.get("taskId")
    else:
        print("Error creating task:", response.text)
        return None
    
def get_captcha_token(task_id):
    task_result_url = 'https://api.capsolver.com/getTaskResult'
    result_data = {'clientKey': CAPSOLVER_API_KEY, 'taskId': task_id}

    while True:
        result_response = requests.post(task_result_url, json=result_data)
        result_data = result_response.json()

        if result_response.status_code == 200 and result_data.get("status") == 'ready':
            return result_data.get('solution', {}).get('gRecaptchaResponse')
        elif result_response.status_code != 200 or result_data.get("status") == 'failed':
            print("Error retrieving task result:", result_response.text)
            return None