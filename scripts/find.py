import os
import requests
import json
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
URI = os.getenv("BASE_URL")
USERNAME = os.getenv("GENESISUSER")
PASSWORD = os.getenv("PASSWORD")
LANGUAGE = os.getenv("LANGUAGE")

# Build URI
URI_FIND = f"{URI}/find/find"

# Ensure required variables are set
if not URI or not USERNAME or not PASSWORD:
    print("Error: Missing required environment variables in .env file.")
    exit(1)

# Load payload
try:
    with open("payload.json", "r") as file:
        payload = json.load(file)
except FileNotFoundError:
    print(f"Error: File 'payload.json' not found.")
    exit(1)

# Define the request parameters
FORM_REQUEST = {
    "username": USERNAME,
    "password": PASSWORD,
    "language": LANGUAGE
}

FORM_REQUEST.update(payload)

# Mask password for printout
FORM_REQUEST_print = FORM_REQUEST.copy()
FORM_REQUEST_print["password"] = FORM_REQUEST["password"][0] + (len(FORM_REQUEST["password"]) - 1) * "*"

print("--- SEARCHING ITEMS --- ")
print(f"URL:\t{URI_FIND}")
print("payload:")
print(json.dumps(FORM_REQUEST_print, indent=4))

print(f'\n --- searching ---\n')

# Perform the GET request
try:
    response = requests.get(URI_FIND, params=FORM_REQUEST)
    response.raise_for_status()  # Raise exception for HTTP errors

    # Print the response in a readable JSON format
    result = response.json()
    
    # Iterate through the keys and handle values
    for key, value in result.items():
        if value is None:  # Check if the value is null
            print(f"{key}: null")
        elif isinstance(value, list):  # Check if the value is a list and print its length
            print(f"{key}: {len(value)} items found.")
            
            # Prompt user to save the list
            save_choice = input(f"Do you want to save the contents of '{key}' to a file? (y/n): ").strip().lower()
            if save_choice in ["yes", "y"]:
                # Check for find directory
                os.makedirs("find", exist_ok=True)
                # Construct the file name
                file_name = f"find/find_{payload['term']}_{key}.json"
                try:
                    # Save the list to the JSON file
                    with open(file_name, "w") as file:
                        json.dump(value, file, indent=4)
                    print(f"{key} saved to {file_name}.")
                except Exception as e:
                    print(f"Error saving {key} to {file_name}: {e}")
            else:
                print(f"{key} was not saved.")
        else:  # For non-list and non-null values, print them directly
            print(f"{key}: {value}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
