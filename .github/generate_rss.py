import csv
import datetime

# Define output RSS XML file
rss_file = "reiss_daf_podcast.xml"
csv_file = "reiss_daf_mp3s.csv"

# Podcast metadata
PODCAST_TITLE = "R' Reiss Dayan's Daf Yomi"
PODCAST_LINK = "https://matthewjmiller07.github.io/DayansDaf/reiss_daf_podcast.xml"

rss_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{PODCAST_TITLE}</title>
    <link>{PODCAST_LINK}</link>
'''

with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        pub_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
        rss_content += f'''
    <item>
      <title>{row['shiurtitle']}</title>
      <enclosure url="{row['shiurdownloadurl']}" type="audio/mpeg"/>
      <pubDate>{pub_date}</pubDate>
    </item>
'''

rss_content += '''
  </channel>
</rss>
'''

# Save RSS feed
with open(rss_file, 'w', encoding='utf-8') as f:
    f.write(rss_content)
