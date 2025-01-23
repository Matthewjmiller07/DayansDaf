import requests
import csv
import os

# Define YU Torah API URL
base_url = "https://www.yutorah.org/Search/GetSearchResults"

# Search parameters for R' Reiss Dayan's Daf
params = {
    "sort_by": "shiurdate desc",
    "organizationID": 301,
    "search_query": "R' Reiss Dayan's Daf",
    "page": 1,
}

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "x-requested-with": "XMLHttpRequest",
}

# Fetch latest episodes
response = requests.get(base_url, headers=headers, params=params)
data = response.json()
new_episodes = data.get("response", {}).get("docs", [])

# Read existing CSV to avoid duplicates
csv_file = "reiss_daf_mp3s.csv"
existing_ids = set()

if os.path.exists(csv_file):
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_ids.add(row["shiurid"])

# Append new episodes to CSV
with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "shiurid", "shiurtitle", "teacherfullname", "categoryname",
        "durationformatted", "shiurdownloadurl", "shiurplayerurl",
        "shiurdateformatted", "location"
    ])

    for shiur in new_episodes:
        if str(shiur.get("shiurid")) not in existing_ids:
            writer.writerow({
                "shiurid": shiur.get("shiurid"),
                "shiurtitle": shiur.get("shiurtitle"),
                "teacherfullname": ", ".join(shiur.get("teacherfullname") or []),
                "categoryname": ", ".join(shiur.get("categoryname") or []),
                "durationformatted": shiur.get("durationformatted"),
                "shiurdownloadurl": shiur.get("shiurdownloadurl"),
                "shiurplayerurl": shiur.get("shiurplayerurl"),
                "shiurdateformatted": shiur.get("shiurdateformatted"),
                "location": shiur.get("location"),
            })
