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


def write_html_report(jobs):

    html = f"""
<html>
<head>
    <title>Job Search Report</title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}

        .job {{
            border: 1px solid #cccccc;
            border-radius: 5px;
            padding: 12px;
            margin-bottom: 12px;
        }}

        .title {{
            font-size: 18px;
            font-weight: bold;
        }}

        .company {{
            color: #555555;
        }}

        .source {{
            color: #777777;
            font-size: 12px;
        }}

        a {{
            color: #0066cc;
        }}

    </style>

</head>

<body>

<h1>Job Search Report</h1>

<p>
    Total Jobs Found: {len(jobs)}
</p>

"""

    for job in jobs:
        
        html += f"""
        <div class="job">
        
            <div class="title">
                {job["title"]}
            </div>
        
            <div class="company">
                {job["company"]}
            </div>
        
            <div>
                {job["location"]}
            </div>
        
            <div class="source">
                Source: {job["source"]}
            </div>
        
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
