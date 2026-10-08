import os
import requests

from report import write_html_report

MAX_RESULTS = 10

KEYWORDS = [
    "business analyst",
    "technical consultant",
    "implementation consultant",
    "solutions consultant",
    "product owner"
]

def get_adzuna_jobs():

    app_id = os.environ["ADZUNA_APP_ID"]
    app_key = os.environ["ADZUNA_APP_KEY"]

    url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

    jobs = []

    for keyword in KEYWORDS:

        print(f"Searching Adzuna for: {keyword}")

        response = requests.get(
            url,
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

    unique_jobs = []
    dedupe_keys = set()

    for job in all_jobs:

        key = (
            (job["title"] or "").lower().strip(),
            (job["company"] or "").lower().strip(),
            (job["location"] or "").lower().strip()
        )

        if key not in dedupe_keys:
            dedupe_keys.add(key)
            unique_jobs.append(job)

    print()
    print(f"Jobs before dedupe : {len(all_jobs)}")
    print(f"Jobs after dedupe  : {len(unique_jobs)}")

    write_html_report(unique_jobs)

    print("HTML report written to jobs_report.html")


if __name__ == "__main__":
    main()
