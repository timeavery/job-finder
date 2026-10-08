import urllib.request
import json

url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

request = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

response = urllib.request.urlopen(request)

jobs = json.loads(response.read())

print("Latest jobs:")

keywords = [
    "analyst",
    "business analyst",
    "consultant",
    "technical consultant",
    "product owner",
    "implementation",
    "integration",
    "solution",
    "pre sales",
    "presales"
]

print("Matching jobs:")

for job in jobs[1:]:
    title = job.get("position", "")

    if any(word in title.lower() for word in keywords):

        print(title)

        print(job.get("location", "Remote"))

        print(job.get("url", ""))

        print("--------------------------------")
