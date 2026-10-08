def get_adzuna_jobs(KEYWORDS, MAX_RESULTS):

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
