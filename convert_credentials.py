import json

with open("credentials.json", "r") as f:
    cred = json.load(f)

cred["private_key"] = cred["private_key"].replace("\n", "\\n")

print("[gsheets]")
for key, value in cred.items():
    print(f'{key} = "{value}"')
