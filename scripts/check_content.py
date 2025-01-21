import json
import os

# Define the directory
directory = "find"

# Check if the directory exists
if not os.path.exists(directory):
    print(f"Error: Directory '{directory}' doesn't exist. Exiting.")
    exit(1)  # Exit the script with a non-zero exit code

# Get the list of files
try:
    files = os.listdir(directory)

    # Filter files: include `.json` but exclude `.png`
    filtered_files = [f for f in files if f.endswith(".json") and not f.endswith(".png")]
except FileNotFoundError:
    print(f"Error: Directory '{directory}' does not exist.")

for f in filtered_files:
    with open(os.path.join(directory, f), "r") as file:
        dict_f = json.load(file)

print(dict_f[1]["Content"])

print("\nWARNING: this script is still under construction\n")