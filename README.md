# Job Listing Scraper (Practice Version)

HR managers at mid-size Nairobi companies want to track competitor job postings: which skills are in demand and what salaries are offered. Doing this by hand means opening pages one by one. This script automates the collection and saves the results to a CSV file.

The practice target is [quotes.toscrape.com](https://quotes.toscrape.com/), a site built for scraping practice. Each quote stands in for a job listing.

## What it does

1. Visits all 10 pages of the site, with a 1-second pause between pages.
2. Extracts 6 fields from each listing and saves them to `quotes.csv`.
3. Validates the CSV automatically: at least 4 columns, no empty or duplicate rows, full URLs.

| Field | Stands in for (jobs board) |
|---|---|
| `quote_text` | Job title / description |
| `author` | Company name |
| `tags` | Required skills |
| `author_url` | Link to the listing |
| `page` | Which page it came from |
| `scraped_at` | When it was collected |

## How to run

```
pip install requests beautifulsoup4
python scraping.py
```

Expected result: about 100 rows saved to `quotes.csv`, then `VALIDATION PASSED`.

## Adapting this for a live jobs board

1. **Get written permission** from the client and confirm they are allowed to collect this data.
2. **Check for an official API or export first.** It is more stable and safer than scraping.
3. **Change the selectors** in `parse_page()` to match the board's HTML. Collect: job title, company, location, posted date, salary, skills and listing URL.
4. **Handle logins** using the credentials the client provides, kept outside the code (environment variables). If the board loads listings with JavaScript, use a tool like Playwright.
5. **Clean the data.** Salaries appear as "KES 80k-100k" or "negotiable", so convert them to numbers and flag what can't be read. Standardise skill names, for example "MS Excel" and "Excel".
6. **Track changes week to week** so the report shows what is new or removed.
7. **Schedule it weekly** and get an alert if a run returns far fewer rows than usual.

## Ethical and legal checks before starting

I am not a lawyer, so a real project needs a legal review.

- **Terms of Service:** many job boards forbid automated access. Check first.
- **robots.txt:** read it and respect it.
- **Computer Misuse and Cybercrimes Act, 2018 (Kenya):** no accessing areas I'm not authorised to use, and no bypassing logins or CAPTCHAs.
- **Data Protection Act, 2019 (Kenya):** postings may contain personal data such as recruiter names, emails and phone numbers. Collect only what the report needs and drop the rest.
- **Copyright:** report insights (counts, salary ranges) instead of copying full job ads.
- **Server load:** identify the bot with a contact email, pause between requests, and stop if asked.
- **Honest reporting:** advertised salary is not paid salary. Show how many listings had no pay information.

## Pricing note (for an HR consultancy)

Prices are in Kenyan shillings, excluding VAT. This is a starting proposal, to be adjusted after scoping.

| | Amount | What it covers |
|---|---|---|
| **Setup fee (one-off)** | **KES 60,000** | Scoping, legal check, building and testing the scraper for up to 3 sources, data cleaning rules, report template, first report |
| **Monthly retainer** | **KES 30,000 / month** | Weekly runs, validation, clean CSV plus a 2-page summary report, fixes when a site changes, email support |

Extra sources cost KES 15,000 to set up and KES 5,000 a month to maintain. I'd suggest a 3-month minimum term, since scrapers need regular upkeep when sites change.

## Limitations

- The selectors only work for the practice site and must be rewritten for any real jobs board.