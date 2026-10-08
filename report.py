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
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

    </style>

</head>

<body>

<h1>Job Search Report</h1>

<p>Total Jobs Found: {len(jobs)}</p>

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

    with open("docs/index.html", "w", encoding="utf-8") as f:
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
