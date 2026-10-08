import os
import requests

from get_reed_jobs import get_reed_jobs
from get_adzuna_jobs import get_adzuna_jobs

from report import write_html_report

MAX_RESULTS = 10

KEYWORDS = [
    "business analyst",
    "technical consultant",
    "implementation consultant",
    "solutions consultant",
    "product owner"
]


def main():

    all_jobs = []

    try:
        all_jobs.extend(get_reed_jobs(KEYWORDS, MAX_RESULTS))
    except Exception as ex:
        print(f"Reed failed: {ex}")

    try:
        all_jobs.extend(get_adzuna_jobs(KEYWORDS, MAX_RESULTS))
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
