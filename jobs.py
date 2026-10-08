import urllib.request
import json

url = "https://remoteok.com/api"

request = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

response = urllib.request.urlopen(request)

jobs = json.loads(response.read())

print("Latest jobs:")

keywords = [
    "business",
    "consultant",
    "analyst",
    "technical",
    "product"
]

print("Matching jobs:")

for job in jobs[1:]:
    title = job.get("position", "")

    if any(word in title.lower() for word in keywords):
        print(title)
