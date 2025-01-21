import os
import requests
import json
from dotenv import load_dotenv

# Initiation
print("--- init CHECK CONNECTION ---")

# Load environment variables from .env file
load_dotenv()

# Get base URI from .env
URI = os.getenv("BASE_URL")

# Ensure the BASE_URL is present
if not URI:
    print("Error: BASE_URL not found in .env file.")
    exit(1)

# 1. WHOAMI: Check connection
print(f"\n### WHOAMI CHECK ###")
URI_whoami = f"{URI}/helloworld/whoami"

try:
    # Perform the GET request
    response = requests.get(URI_whoami)
    if response.status_code == 200:
        print("WHOAMI Connection successful:")
        print(print(json.dumps(response.json(), indent=4))) # Print the raw JSON response
    else:
        print(f"WHOAMI Error: {response.status_code} - {response.reason}")
except requests.exceptions.RequestException as e:
    print(f"WHOAMI Request failed: {e}")

print("")

# 2. Login Check
print(f"### LOGIN CHECK ###")
URI_logincheck = f"{URI}/helloworld/logincheck"

# Create the login payload
FORM_LOGINCHECK = {
    "username": os.getenv("GENESISUSER"),
    "password": os.getenv("PASSWORD"),
    "language": os.getenv("LANGUAGE", "en"),  # Default to "en" if not provided
}

#to hide the password in the printed statement
FORM_LOGINCHECK_print = {
    "username": os.getenv("GENESISUSER"),
    "password": f"{os.getenv('PASSWORD')[0]}{(len(os.getenv('PASSWORD'))-1)*'*'}",
    "language": os.getenv("LANGUAGE", "en"),  # Default to "en" if not provided
}

print(json.dumps(FORM_LOGINCHECK_print, indent=4))

# Ensure username and password are present
if not FORM_LOGINCHECK["username"] or not FORM_LOGINCHECK["password"]:
    print("Error: USERNAME or PASSWORD not found in .env file.")
    exit(1)

try:
    # Perform the POST request with form-encoded data
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(URI_logincheck, data=FORM_LOGINCHECK, headers=headers)
    if response.status_code == 200:
        print("Login check successful:")
        print(print(json.dumps(response.json(), indent=4)))  # Print the raw JSON response
    elif response.status_code == 401:
        print("Unauthorized: Check your username and password.")
    elif response.status_code == 400:
        print("Bad Request: Verify the payload.")
    else:
        print(f"Login Check Error: {response.status_code} - {response.reason}")
except requests.exceptions.RequestException as e:
    print(f"Login Check Request failed: {e}")

print("--- end CHECK CONNECTION ---")
