import os
import requests

MAX_RESULTS = 10

KEYWORDS = [
    "business analyst",
    "technical consultant",
    "implementation consultant",
    "solutions consultant",
    "product owner"
]

def get_reed_jobs():
    api_key = os.environ["REED_API_KEY"]
    URL =  "https://www.reed.co.uk/api/1.0/search"
  
    jobs = []

    for keyword in KEYWORDS:

        print(f"Searching Reed for: {keyword}")

        response = requests.get(
            URL,
            params={
                "keywords": keyword,
                "resultsToTake": MAX_RESULTS
            },
            auth=(api_key, "")
        )

        print(f"Status: {response.status_code}")

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


def get_adzuna_jobs():
    app_id = os.environ["ADZUNA_APP_ID"]
    app_key = os.environ["ADZUNA_APP_KEY"]
    URL = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

    jobs = []

    for keyword in KEYWORDS:

        print(f"Searching Adzuna for: {keyword}")
        
        response = requests.get(
            URL,
            params={
                "app_id": app_id,
                "app_key": app_key,
                "what": keyword,
                "results_per_page": MAX_RESULTS
            }
        )
    
        print(f"Adzuna status: {response.status_code}")
    
        data = response.json()
    
        for job in data.get("results", []):
            jobs.append({
                "source": "Adzuna",
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "url": job.get("redirect_url")
            })

    return jobs


def main():

    all_jobs = []

    try:
        all_jobs.extend(get_reed_jobs())
    except Exception as ex:
        print(f"Reed failed: {ex}")

    try:
        all_jobs.extend(get_adzuna_jobs())
    except Exception as ex:
        print(f"Adzuna failed: {ex}")

    print()
    print(f"Total jobs found: {len(all_jobs)}")
    
    unique_jobs = []
    seen = set()

    for job in all_jobs:
        
        key = (
            (job["title"] or "").lower().strip(),
            (job["company"] or "").lower().strip(),
            (job["location"] or "").lower().strip()
        )
        
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    print(f"Jobs before dedupe: {len(all_jobs)}")
    print(f"Jobs after dedupe : {len(unique_jobs)}")
    
    for job in unique_jobs:
        print()
        print("----------------------------------------")
        # print(f"Source   : {job['source']}")
        print(f"Title    : {job['title']}")
        print(f"Company  : {job['company']}")
        print(f"Location : {job['location']}")
        print(f"URL      : {job['url']}")


if __name__ == "__main__":
    main()
