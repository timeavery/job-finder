import os
import json
import requests

MAX_RESULTS = 10
SEEN_JOBS_FILE = "seen_jobs.json"

KEYWORDS = [
    "business analyst",
    "technical consultant",
    "implementation consultant",
    "solutions consultant",
    "product owner"
]

def write_html_report(jobs):

    html = """
    <html>
    <head>
        <title>Job Report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }

            .job {
                border: 1px solid #cccccc;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 5px;
            }

            .title {
                font-size: 18px;
                font-weight: bold;
            }

            .company {
                color: #444444;
            }

            a {
                color: blue;
            }
        </style>
    </head>
    <body>

        <h1>Daily Job Report</h1>

    """

    for job in jobs:

        html += f"""
        <div class="job">
            <div class="title">{job['title']}</div>
            <div class="company">{job['company']}</div>
            <div>{job['location']}</div>
            <div>{job['source']}</div>

            <p>
                {job['url']}
                    View Job
                </a>
            </p>
        </div>
        """

    html += """
    </body>
    </html>
    """

    with open("jobs_report.html", "w", encoding="utf-8") as f:
        f.write(html)

def load_seen_jobs():

    try:
        with open(SEEN_JOBS_FILE, "r") as f:
            return set(json.load(f))

    except FileNotFoundError:
        return set()


def save_seen_jobs(seen_jobs):

    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump(
            sorted(list(seen_jobs)),
            f,
            indent=2
        )


def get_reed_jobs():

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

    seen_jobs = load_seen_jobs()

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

    new_jobs = []
    updated_seen_jobs = set(seen_jobs)

    for job in unique_jobs:

        job_id = "|".join([
            (job["title"] or "").lower().strip(),
            (job["company"] or "").lower().strip(),
            (job["location"] or "").lower().strip()
        ])

        if job_id not in seen_jobs:
            new_jobs.append(job)

        updated_seen_jobs.add(job_id)

    save_seen_jobs(updated_seen_jobs)

    write_html_report(new_jobs)
    print("HTML report written to jobs_report.html")
    
    print()
    print(f"Jobs before dedupe : {len(all_jobs)}")
    print(f"Jobs after dedupe  : {len(unique_jobs)}")
    print(f"Previously seen    : {len(seen_jobs)}")
    print(f"New jobs found     : {len(new_jobs)}")

    for job in new_jobs:

        print()
        print("----------------------------------------")
        print(f"Title    : {job['title']}")
        print(f"Company  : {job['company']}")
        print(f"Location : {job['location']}")
        print(f"URL      : {job['url']}")


if __name__ == "__main__":
    main()
