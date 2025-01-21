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

# Ensure required variables are set
if not URI or not USERNAME or not PASSWORD:
    print("Error: Missing required environment variables in .env file.")
    exit(1)

# Build argument parser
parser = argparse.ArgumentParser(description="Query terms catalog with a selection term.")
parser.add_argument("-s", "--selection", type=str, required=True, help="Term to search for in the terms catalog.")
parser.add_argument(
    "-d", "--display", action="store_true", help="Display the resulting list of hits (default: False)."
)
args = parser.parse_args()

# Define the request parameters
FORM_REQUEST = {
    "username": USERNAME,
    "password": PASSWORD,
    "selection": args.selection,
    "pagelength": "100",
    "language": "en",
}

# Define the endpoint
URI_TERMS = f"{URI}/catalogue/terms"

# Perform the GET request
try:
    response = requests.get(URI_TERMS, params=FORM_REQUEST)
    response.raise_for_status()  # Raise exception for HTTP errors

    # Parse and handle the response
    result = response.json()
    hits = len(result.get("List", []))  # Safely handle missing "List" key
    print(f'Response: {hits} hits for the term "{FORM_REQUEST["selection"]}"')
    
    # Display results if requested
    if args.display:
        if "List" in result:
            print(json.dumps(result["List"], indent=4))
        else:
            print("No results found to display.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred during the request: {e}")
except json.JSONDecodeError:
    print("Failed to decode JSON from the response.")
except KeyError as e:
    print(f"Missing expected key in the response: {e}")
