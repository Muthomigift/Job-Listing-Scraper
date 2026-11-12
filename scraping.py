"""
Single-file scraper + validator.
Scrapes https://quotes.toscrape.com/ (practice site), saves a CSV,
then checks the CSV automatically.

Run:   python scraping.py
Setup: pip install requests beautifulsoup4
"""
import csv
import time
from datetime import datetime, timezone
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
OUTPUT_FILE = "quotes.csv"
HEADERS = {"User-Agent": "ListingScraperBot/1.0 (learning project; contact: muthomigift@gmail.com)"}
FIELDS = ["quote_text", "author", "tags", "author_url", "page", "scraped_at"]


def parse_page(html, page_url, page_number):
    """Read one page. Returns (list of rows, url of next page or None)."""
    soup = BeautifulSoup(html, "html.parser")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = []
    for card in soup.select("div.quote"):
        text = card.select_one("span.text")
        author = card.select_one("small.author")
        link = card.select_one("a[href^='/author/']")
        if text is None or author is None:
            continue  # skip broken cards
        rows.append({
            "quote_text": text.get_text(strip=True),
            "author": author.get_text(strip=True),
            "tags": "|".join(t.get_text(strip=True) for t in card.select("a.tag")),
            "author_url": urljoin(page_url, link["href"]) if link else "",
            "page": page_number,
            "scraped_at": now,
        })
    nxt = soup.select_one("li.next a")
    return rows, (urljoin(page_url, nxt["href"]) if nxt else None)


def scrape():
    """Visit every page, politely, and collect all rows."""
    all_rows, url, page = [], BASE_URL, 1
    while url:
        print(f"Fetching page {page}: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        rows, url = parse_page(response.text, url, page)
        all_rows.extend(rows)
        page += 1
        if url:
            time.sleep(1)  # be polite: 1 second between requests
    return all_rows


def save_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def validate_csv(path):
    """Returns a list of problems. Empty list = CSV is good."""
    problems = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    if len(headers) < 4:
        problems.append(f"Only {len(headers)} columns; need at least 4.")
    if not rows:
        problems.append("No data rows.")
        return problems

    seen = set()
    for line, row in enumerate(rows, start=2):
        if not row["quote_text"].strip():
            problems.append(f"Line {line}: empty quote_text")
        if not row["author"].strip():
            problems.append(f"Line {line}: empty author")
        if row["author_url"] and not row["author_url"].startswith("http"):
            problems.append(f"Line {line}: author_url is not a full URL")
        key = (row["quote_text"], row["author"])
        if key in seen:
            problems.append(f"Line {line}: duplicate row")
        seen.add(key)
    return problems


if __name__ == "__main__":
    data = scrape()
    save_csv(data, OUTPUT_FILE)
    print(f"\nSaved {len(data)} rows to {OUTPUT_FILE}")

    issues = validate_csv(OUTPUT_FILE)
    if issues:
        print("VALIDATION FAILED:")
        for problem in issues:
            print(" -", problem)
    else:
        print("VALIDATION PASSED: 4+ fields, no empty or duplicate rows.")