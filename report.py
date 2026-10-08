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

