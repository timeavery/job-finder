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

for job in jobs[1:6\]:
    print(job.get("position", "Unknown"))
