import os
import requests

MAX_RESULTS = 10


def get_reed_jobs():
    api_key = os.environ["REED_API_KEY"]

    response = requests.get(
        "https://www.reed.co.uk/api/1.0/search",
        params={
            "keywords": "business analyst",
            "resultsToTake": MAX_RESULTS
        },
        auth=(api_key, "")
    )

    print(f"Reed status: {response.status_code}")

    data = response.json()

    jobs = []

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

    response = requests.get(
        "https://api.adzuna.com/v1/api/jobs/gb/search/1",
        params={
            "app_id": app_id,
            "app_key": app_key,
            "what": "business analyst",
            "results_per_page": MAX_RESULTS
        }
    )

    print(f"Adzuna status: {response.status_code}")

    data = response.json()

    jobs = []

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

    for job in all_jobs:
        print()
        print("----------------------------------------")
        print(f"Source   : {job['source']}")
        print(f"Title    : {job['title']}")
        print(f"Company  : {job['company']}")
        print(f"Location : {job['location']}")
        print(f"URL      : {job['url']}")


if __name__ == "__main__":
    main()
