import os
import json 

# Check for the relevant directories and make them if necessary
for directory in ["load", "data"]:
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' was created.")

# load all load files
load_files = os.listdir("load")

#extract opening code for all 
for lf in load_files:
     if ".json" in lf:
        with open(os.path.join("load", lf), "r") as file:
            dict_lf = json.load(file)
        print(dict_lf)
    