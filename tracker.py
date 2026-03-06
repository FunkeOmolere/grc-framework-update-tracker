import requests
import feedparser
import csv
import json
from datetime import datetime
import os
feeds = {
    "CISA News": "https://www.cisa.gov/news.xml",
    "Krebs on Security": "https://krebsonsecurity.com/feed/",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

keywords = {
    "DORA": ["dora", "digital operational resilience"],
    "NIS2": ["nis2", "nis 2"],
    "ENS": ["ens", "esquema nacional de seguridad"],
    "Cyber Essentials": ["cyber essentials", "cyber essentials plus"],
    "GDPR": ["gdpr", "data protection", "privacy"],
    "ISO 27001": ["iso 27001", "information security"],
    "Vulnerability Management": ["vulnerability", "cve", "patch", "exploit"],
    "Operational Resilience": ["operational resilience", "resilience", "third party risk"],
}
results = []

for name, url in feeds.items():
    print(f"\nChecking updates from {name}...\n")

    response = requests.get(url, headers=headers)
    print("HTTP Status:", response.status_code)

    if response.status_code != 200:
        print("Feed blocked or unavailable.\n")
        continue

    feed = feedparser.parse(response.text)
    print("Entries found:", len(feed.entries))

    if not feed.entries:
        print("No updates found.\n")
        continue

    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        summary = getattr(entry, "summary", "")

        text_to_check = f"{title} {summary}".lower()

        matched_tags = []

        for tag, terms in keywords.items():
            for term in terms:
                if term in text_to_check:
                    matched_tags.append(tag)
                    break
        results.append({
             "Source": name,
             "Title": title,
             "Link": link,
             "Tags": ", ".join(matched_tags) if matched_tags else "General Cybersecurity" 
        })  

        print(f"Title: {title}")
        print(f"Link: {link}")

        if matched_tags:
            print("Relevant Tags:", ", ".join(matched_tags))
        else:
            print("Relevant Tags: General Cybersecurity")

        print("-" * 50)
        with open("grc_security_updates.csv", "w", newline="") as file:
             writer = csv.DictWriter(file, fieldnames=["Source", "Title", "Link", "Tags"])
             writer.writeheader()
             writer.writerows(results)

        print("Saved results to grc_security_updates.csv")
        results_json = json.dumps(results)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
html = f"""
<html>
<head>
<title>GRC Intelligence Dashboard</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background:#020617;
    color:#e2e8f0;
    padding:40px;
}}

h1 {{
    color:#22c55e;
}}

.card {{
    background:#111827;
    padding:18px;
    border-radius:12px;
    margin-bottom:18px;
    border-left:4px solid #22c55e;
}}

.tag {{
    background:#1d4ed8;
    padding:5px 10px;
    border-radius:20px;
    font-size:12px;
}}

a {{
    color:#38bdf8;
}}
</style>
</head>

<body>

<h1>GRC Intelligence Tracker</h1>
<p>Last updated: {timestamp}</p>

<div id="results"></div>

<script>

const data = {results_json};

let htmlContent = "";

data.forEach(item => {{
    htmlContent += `
        <div class="card">
        <h3><a href="${{item.Link}}" target="_blank">${{item.Title}}</a></h3>
        <p><b>Source:</b> ${{item.Source}}</p>
        <p><span class="tag">${{item.Tags}}</span></p>
        </div>
    `;
}})

document.getElementById("results").innerHTML = htmlContent;

</script>

</body>
</html>
"""
os.makedirs("docs", exist_ok=True)

with open("docs/index.html","w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard created: docs/index.html")