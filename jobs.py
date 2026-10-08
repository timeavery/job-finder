import os
import requests

def get_reed_jobs():
    api_key = os.environ["REED_API_KEY"]

    response = requests.get(
        "https://www.reed.co.uk/api/1.0/search",
        params={
            "keywords": "business analyst",
            "resultsToTake": 10
        },
        auth=(api_key, "")
    )

    data = response.json()

    jobs = []

    for job in data.get("results", []):
        jobs.append({
            "source": "Reed",
            "title": job["jobTitle"],
            "company": job["employerName"],
            "location": job["locationName"],
            "salary_min": job.get("minimumSalary"),
            "salary_max": job.get("maximumSalary"),
            "url": job["jobUrl"]
        })

    return jobs


def main():
    jobs = []

    jobs.extend(get_reed_jobs())

    print(f"Found {len(jobs)} jobs")

    for job in jobs:
        print()
        print(job["title"])
        print(job["company"])
        print(job["location"])


if __name__ == "__main__":
    main()
