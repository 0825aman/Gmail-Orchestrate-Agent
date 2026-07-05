import os

creds = os.getenv("credentials")
if creds:
    with open("credentials.json", "w") as f:
        f.write(creds)

token = os.getenv("token")
if token:
    with open("token.json", "w") as f:
        f.write(token)
