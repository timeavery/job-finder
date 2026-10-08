import urllib.request
import json
import os
import base64

api_key = os.environ["REED_API_KEY"]

credentials = base64.b64encode(
    f"{api_key}:".encode()
).decode()

request = urllib.request.Request(
    "https://www.reed.co.uk/api/1.0/search?keywords=business%20analyst",
    headers={
        "Authorization": f"Basic {credentials}"
    }
)

response = urllib.request.urlopen(request)

jobs = json.loads(response.read())

print("Jobs found:", len(jobs["results"]))

for job in jobs["results"][:5\]:
    print(job["jobTitle"])
