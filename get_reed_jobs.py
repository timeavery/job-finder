import os
import requests

def get_reed_jobs(KEYWORDS, MAX_RESULTS):

    api_key = os.environ["REED_API_KEY"]

    url = "https://www.reed.co.uk/api/1.0/search"

    jobs = []

    for keyword in KEYWORDS:

        print(f"Searching Reed for: {keyword}")

        response = requests.get(
            url,
            params={
                "keywords": keyword,
                "resultsToTake": MAX_RESULTS
            },
            auth=(api_key, "")
        )

        print(f"Reed status: {response.status_code}")

        data = response.json()

        for job in data.get("results", []):

            jobs.append({
                "source": "Reed",
                "title": job.get("jobTitle"),
                "company": job.get("employerName"),
                "location": job.get("locationName"),
                "url": job.get("jobUrl")
            })

    return jobs
