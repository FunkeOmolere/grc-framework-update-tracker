import requests
import feedparser
import csv
import json
from datetime import datetime
import os

feeds = {
    # Cyber intelligence
    "CISA News": "https://www.cisa.gov/news.xml",
    "Krebs on Security": "https://krebsonsecurity.com/feed/",

    # NCSC UK
    "NCSC UK": "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml",

    # Cyber Essentials / IASME
    "IASME Cyber Essentials": "https://iasme.co.uk/feed/",

    # TISAX
    "ENX / TISAX Updates": "https://news.google.com/rss/search?q=TISAX+cybersecurity",

    # Spain ENS
    "Spain ENS Updates": "https://news.google.com/rss/search?q=Spain+ENS+cybersecurity",

    # DORA
    "DORA Updates": "https://news.google.com/rss/search?q=DORA+Digital+Operational+Resilience+Act+financial",

    # NIS2
    "NIS2 Updates": "https://news.google.com/rss/search?q=NIS2+directive+cybersecurity+compliance",

    # BSI C5
    "BSI C5 Updates": "https://news.google.com/rss/search?q=BSI+C5+cloud+security+criteria",

    # EU AI Act
    "EU AI Act Updates": "https://news.google.com/rss/search?q=EU+AI+Act+compliance+cybersecurity",

    # Vulnerabilities
    "CISA KEV": "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.xml",
    "NVD CVE Feed": "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml",
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

keywords = {
    "Cyber Essentials": ["cyber essentials", "iasme", "ce+", "cyber essentials plus"],
    "NCSC Guidance": ["ncsc", "national cyber security centre", "security advisory"],
    "TISAX": ["tisax", "enx", "vda isa", "automotive cybersecurity"],
    "Spain ENS": ["ens", "esquema nacional", "ccn", "ccn-cert", "spain ens"],
    "DORA": ["dora", "digital operational resilience", "financial resilience regulation", "ict risk financial"],
    "NIS2": ["nis2", "nis 2", "network information security directive", "nis directive"],
    "BSI C5": ["bsi c5", "c5 criteria", "cloud computing compliance", "bsi cloud"],
    "EU AI Act": ["eu ai act", "ai act", "artificial intelligence act", "high-risk ai", "gpai"],
    "Vulnerability Management": ["vulnerability", "patch", "cve", "exploit", "zero-day", "zero day"],
    "Operational Resilience": ["resilience", "incident response", "business continuity", "disaster recovery"],
}

results = []

for name, url in feeds.items():
    print(f"\nChecking updates from {name}...\n")

    try:
        response = requests.get(url, headers=headers, timeout=10)
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
            print("Tags:", ", ".join(matched_tags) if matched_tags else "General Cybersecurity")
            print("-" * 50)

    except Exception as e:
        print(f"Error fetching {name}: {e}")
        continue

# Save CSV
with open("grc_security_updates.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Source", "Title", "Link", "Tags"])
    writer.writeheader()
    writer.writerows(results)

print("\nSaved results to grc_security_updates.csv")

# Build HTML
results_json = json.dumps(results)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GRC Intelligence Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #f7f5f2;
    --surface: #ffffff;
    --surface-2: #f0ede8;
    --border: #e2ddd6;
    --text-primary: #1a1612;
    --text-secondary: #6b6560;
    --text-muted: #9e9890;
    --accent: #c84b2f;
    --accent-light: #fdf0ed;
    --tag-dora: #1d4e89;
    --tag-nis2: #2d6a4f;
    --tag-bsi: #7b3f9e;
    --tag-tisax: #c84b2f;
    --tag-ens: #b5620a;
    --tag-ce: #1a6b5c;
    --tag-ncsc: #3d5a80;
    --tag-vuln: #6b2d2d;
    --tag-general: #4a4a4a;
    --tag-ai: #5a2d82;
    --tag-ops: #8a5200;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
  }}

  .header {{
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 0 48px;
    position: sticky;
    top: 0;
    z-index: 100;
  }}

  .header-inner {{
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 68px;
  }}

  .logo-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: var(--text-primary);
    letter-spacing: -0.3px;
  }}

  .logo-dot {{
    display: inline-block;
    width: 8px;
    height: 8px;
    background: var(--accent);
    border-radius: 50%;
    margin-left: 6px;
    margin-bottom: 3px;
    animation: pulse 2s infinite;
    vertical-align: middle;
  }}

  @keyframes pulse {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.6; transform: scale(0.85); }}
  }}

  .header-meta {{
    font-size: 12px;
    color: var(--text-muted);
    letter-spacing: 0.5px;
  }}

  .hero {{
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 48px 48px 40px;
  }}

  .hero-inner {{
    max-width: 1200px;
    margin: 0 auto;
  }}

  .hero-eyebrow {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 12px;
  }}

  .hero-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 42px;
    line-height: 1.1;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    margin-bottom: 12px;
  }}

  .hero-sub {{
    font-size: 15px;
    color: var(--text-secondary);
    font-weight: 300;
    max-width: 600px;
    line-height: 1.6;
  }}

  .stats-bar {{
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    gap: 32px;
    padding: 24px 48px 0;
    flex-wrap: wrap;
  }}

  .stat {{ display: flex; flex-direction: column; gap: 2px; }}

  .stat-num {{
    font-family: 'DM Serif Display', serif;
    font-size: 28px;
    color: var(--text-primary);
  }}

  .stat-label {{
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 500;
  }}

  .stat-divider {{
    width: 1px;
    background: var(--border);
    align-self: stretch;
  }}

  .main {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 48px;
    display: grid;
    grid-template-columns: 240px 1fr;
    gap: 32px;
    align-items: start;
  }}

  .sidebar {{
    position: sticky;
    top: 88px;
  }}

  .sidebar-label {{
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 10px;
    padding-left: 2px;
  }}

  .filter-btn {{
    display: flex;
    align-items: center;
    gap: 10px;
    width: 100%;
    padding: 9px 14px;
    background: transparent;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    font-size: 13.5px;
    font-weight: 400;
    color: var(--text-secondary);
    text-align: left;
    transition: all 0.15s ease;
    margin-bottom: 2px;
  }}

  .filter-btn:hover {{ background: var(--surface-2); color: var(--text-primary); }}

  .filter-btn.active {{
    background: var(--accent-light);
    color: var(--accent);
    font-weight: 500;
  }}

  .filter-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }}

  .filter-count {{
    margin-left: auto;
    font-size: 11px;
    color: var(--text-muted);
    background: var(--surface-2);
    padding: 1px 7px;
    border-radius: 20px;
  }}

  .filter-btn.active .filter-count {{
    background: rgba(200,75,47,0.12);
    color: var(--accent);
  }}

  .content-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }}

  .results-count {{
    font-size: 13px;
    color: var(--text-muted);
  }}

  .results-count span {{
    color: var(--text-primary);
    font-weight: 600;
  }}

  .card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
    animation: fadeUp 0.3s ease forwards;
    opacity: 0;
    transform: translateY(8px);
  }}

  @keyframes fadeUp {{
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  .card:hover {{
    border-color: #ccc8c0;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    transform: translateY(-1px);
  }}

  .card-top {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 10px;
  }}

  .card-title {{
    font-size: 14.5px;
    font-weight: 500;
    line-height: 1.45;
    color: var(--text-primary);
  }}

  .card-title a {{
    color: inherit;
    text-decoration: none;
  }}

  .card-title a:hover {{ color: var(--accent); }}

  .card-arrow {{
    color: var(--text-muted);
    font-size: 16px;
    flex-shrink: 0;
    margin-top: 1px;
    transition: transform 0.15s ease, color 0.15s ease;
  }}

  .card:hover .card-arrow {{
    transform: translate(2px, -2px);
    color: var(--accent);
  }}

  .card-meta {{
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }}

  .card-source {{
    font-size: 12px;
    color: var(--text-muted);
  }}

  .card-source::before {{
    content: '';
    display: inline-block;
    width: 3px;
    height: 3px;
    background: var(--text-muted);
    border-radius: 50%;
    margin-right: 8px;
    vertical-align: middle;
  }}

  .tag {{
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.3px;
  }}

  .tag-dora {{ background: #edf3fc; color: var(--tag-dora); }}
  .tag-nis2 {{ background: #edf7f2; color: var(--tag-nis2); }}
  .tag-bsi {{ background: #f5edfb; color: var(--tag-bsi); }}
  .tag-tisax {{ background: var(--accent-light); color: var(--tag-tisax); }}
  .tag-ens {{ background: #fdf4e7; color: var(--tag-ens); }}
  .tag-ce {{ background: #edf7f4; color: var(--tag-ce); }}
  .tag-ncsc {{ background: #edf2f8; color: var(--tag-ncsc); }}
  .tag-vuln {{ background: #fdf0f0; color: var(--tag-vuln); }}
  .tag-general {{ background: #f2f2f2; color: var(--tag-general); }}
  .tag-ai {{ background: #f4edfb; color: var(--tag-ai); }}
  .tag-ops {{ background: #fff8ed; color: var(--tag-ops); }}

  .empty {{
    text-align: center;
    padding: 80px 40px;
    color: var(--text-muted);
  }}

  .footer {{
    border-top: 1px solid var(--border);
    padding: 24px 48px;
    margin-top: 40px;
  }}

  .footer-inner {{
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    color: var(--text-muted);
  }}

  .footer-link {{
    color: var(--accent);
    text-decoration: none;
    font-weight: 500;
  }}

  .footer-link:hover {{ text-decoration: underline; }}

  @media (max-width: 900px) {{
    .header, .hero, .footer {{ padding-left: 24px; padding-right: 24px; }}
    .main {{ grid-template-columns: 1fr; padding: 24px; }}
    .sidebar {{ position: static; display: flex; flex-wrap: wrap; gap: 8px; }}
    .stats-bar {{ padding: 16px 24px 0; gap: 20px; }}
    .hero-title {{ font-size: 30px; }}
  }}
</style>
</head>
<body>

<header class="header">
  <div class="header-inner">
    <span class="logo-title">GRC Intelligence<span class="logo-dot"></span></span>
    <span class="header-meta">Last updated: {timestamp}</span>
  </div>
</header>

<div class="hero">
  <div class="hero-inner">
    <p class="hero-eyebrow">EMEA Regulatory Intelligence</p>
    <h1 class="hero-title">Framework Update Tracker</h1>
    <p class="hero-sub">Monitoring regulatory changes, framework updates, and cyber intelligence across DORA, NIS2, BSI C5, TISAX, Spain ENS, Cyber Essentials, and NCSC guidance.</p>
  </div>
</div>

<div class="stats-bar">
  <div class="stat">
    <span class="stat-num" id="total-count">—</span>
    <span class="stat-label">Total Items</span>
  </div>
  <div class="stat-divider"></div>
  <div class="stat">
    <span class="stat-num">10</span>
    <span class="stat-label">Frameworks</span>
  </div>
  <div class="stat-divider"></div>
  <div class="stat">
    <span class="stat-num">10</span>
    <span class="stat-label">Sources</span>
  </div>
  <div class="stat-divider"></div>
  <div class="stat">
    <span class="stat-num">{datetime.now().strftime("%b %Y")}</span>
    <span class="stat-label">Current</span>
  </div>
</div>

<div class="main">
  <aside class="sidebar">
    <div class="sidebar-section">
      <p class="sidebar-label">Filter by Framework</p>
      <button class="filter-btn active" onclick="setFilter('all', this)">
        <span class="filter-dot" style="background:#1a1612"></span>
        All Items
        <span class="filter-count" id="count-all">—</span>
      </button>
      <button class="filter-btn" onclick="setFilter('DORA', this)">
        <span class="filter-dot" style="background:#1d4e89"></span>
        DORA
        <span class="filter-count" id="count-dora">—</span>
      </button>
      <button class="filter-btn" onclick="setFilter('NIS2', this)">
        <span class="filter-dot" style="background:#2d6a4f"></span>
        NIS2
        <span class="filter-count" id="count-nis2">—</span>
      </button>
      <button class="filter-btn" onclick="setFilter('BSI C5', this)">
        <span class="filter-dot" style="background:#7b3f9e"></span>
        BSI C5
        <span class="filter-count" id="count-bsi">—</span>
      </button>
      <button class="filter-btn" onclick="setFilter('EU AI Act', this)">
        <span class="filter-dot" style="background:#5a2d82"></span>
        EU AI Act
        <span class="filter-count" id="count-ai">—</span>
      </button>
      <button class="filter-btn" onclick="setFilter('TISAX', this)">
        <span class="filter-dot" style="background:#c84b2f"></span>
        TISAX
        <span class="filter-count" id="count-tisax">—</span>
      </button>
      <button class="filter-btn" onclick="setFilter('Spain ENS', this)">
        <span class="filter-dot" style="background:#b5620a"></span>
        Spain ENS
        <span class="filter-count" id="count-ens">—</span>
      </button>
      <button class="filter-btn" onclick="setFilter('Cyber Essentials', this)">
        <span class="filter-dot" style="background:#1a6b5c"></span>
        Cyber Essentials
        <span class="filter-count" id="count-ce">—</span>
      </button>
      <button class="filter-btn" onclick="setFilter('NCSC Guidance', this)">
        <span class="filter-dot" style="background:#3d5a80"></span>
        NCSC
        <span class="filter-count" id="count-ncsc">—</span>
      </button>
      <button class="filter-btn" onclick="setFilter('Vulnerability Management', this)">
        <span class="filter-dot" style="background:#6b2d2d"></span>
        Vulnerability
        <span class="filter-count" id="count-vuln">—</span>
      </button>
      <button class="filter-btn" onclick="setFilter('General Cybersecurity', this)">
        <span class="filter-dot" style="background:#4a4a4a"></span>
        General Cyber
        <span class="filter-count" id="count-general">—</span>
      </button>
    </div>
  </aside>

  <main>
    <div class="content-header">
      <p class="results-count">Showing <span id="showing-count">—</span> items</p>
    </div>
    <div id="results"></div>
  </main>
</div>

<footer class="footer">
  <div class="footer-inner">
    <span>Built by <a href="https://funkeomolere.github.io" class="footer-link">Funke Omolere</a> · Part of the GRC Engineering Club</span>
    <span>EMEA Practitioner Resource · MIT Licensed</span>
  </div>
</footer>

<script>
const data = {results_json};

function getTagClass(tag) {{
  const map = {{
    'DORA': 'tag-dora',
    'NIS2': 'tag-nis2',
    'BSI C5': 'tag-bsi',
    'EU AI Act': 'tag-ai',
    'TISAX': 'tag-tisax',
    'Spain ENS': 'tag-ens',
    'Cyber Essentials': 'tag-ce',
    'NCSC Guidance': 'tag-ncsc',
    'Vulnerability Management': 'tag-vuln',
    'General Cybersecurity': 'tag-general',
    'Operational Resilience': 'tag-ops',
  }};
  return map[tag.trim()] || 'tag-general';
}}

let currentFilter = 'all';

function setFilter(filter, btn) {{
  currentFilter = filter;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderResults();
}}

function renderResults() {{
  const container = document.getElementById('results');
  const filtered = currentFilter === 'all'
    ? data
    : data.filter(item => item.Tags.includes(currentFilter));

  document.getElementById('showing-count').textContent = filtered.length;

  if (filtered.length === 0) {{
    container.innerHTML = '<div class="empty"><p>No items found for this filter.</p></div>';
    return;
  }}

  container.innerHTML = filtered.map((item, i) => {{
    const tags = item.Tags.split(',').map(t => t.trim());
    const tagHtml = tags.map(t => `<span class="tag ${{getTagClass(t)}}">${{t}}</span>`).join(' ');
    return `
      <div class="card" style="animation-delay:${{i * 0.04}}s">
        <div class="card-top">
          <p class="card-title"><a href="${{item.Link}}" target="_blank" rel="noopener">${{item.Title}}</a></p>
          <span class="card-arrow">↗</span>
        </div>
        <div class="card-meta">
          <span class="card-source">${{item.Source}}</span>
          ${{tagHtml}}
        </div>
      </div>`;
  }}).join('');
}}

function updateCounts() {{
  const countMap = {{}};
  data.forEach(item => {{
    item.Tags.split(',').forEach(t => {{
      const key = t.trim();
      countMap[key] = (countMap[key] || 0) + 1;
    }});
  }});

  document.getElementById('count-all').textContent = data.length;
  document.getElementById('total-count').textContent = data.length;
  document.getElementById('count-dora').textContent = countMap['DORA'] || 0;
  document.getElementById('count-nis2').textContent = countMap['NIS2'] || 0;
  document.getElementById('count-bsi').textContent = countMap['BSI C5'] || 0;
  document.getElementById('count-ai').textContent = countMap['EU AI Act'] || 0;
  document.getElementById('count-tisax').textContent = countMap['TISAX'] || 0;
  document.getElementById('count-ens').textContent = countMap['Spain ENS'] || 0;
  document.getElementById('count-ce').textContent = countMap['Cyber Essentials'] || 0;
  document.getElementById('count-ncsc').textContent = countMap['NCSC Guidance'] || 0;
  document.getElementById('count-vuln').textContent = countMap['Vulnerability Management'] || 0;
  document.getElementById('count-general').textContent = countMap['General Cybersecurity'] || 0;
}}

updateCounts();
renderResults();
</script>
</body>
</html>"""

os.makedirs("docs", exist_ok=True)

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nDashboard created: docs/index.html ({len(results)} items)")
