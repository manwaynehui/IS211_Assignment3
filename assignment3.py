import argparse
# other imports go here
import csv
import re
import io
import sys
import urllib.request
import logging
from datetime import datetime

logging.basicConfig(
    filename='errors.log',
    level=logging.ERROR,
    format='%(messages)s'
)

def download_data(url):
    #downloads the file from web and returns as readable text
    try:
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')
    except Exception as e:
        #If website is down
        logging.error(f"Error downloading from {url}: {e}")
        sys.exit()

def process_data(file_content):
    logger = logging.getLogger('assignment3')

    # using string io for text as file
    csv_reader = io.StringIO(file_content)
    reader = csv.reader(csv_reader)

    total_hits = 0
    image_hits = 0
    browsers = {"Firefox":0,
                "Chrome":0,
                "Internet Explorer":0,
                "Safari":0}
    hourly_counts = {}

    for row in reader:
        if not row:
            continue

        total_hits += 1
        path        = row[0]
        timestamp   = row[1]
        user        = row[2]

        if re.search(r"\.(jpg|gif|png)$", path, re.IGNORECASE):
            image_hits += 1

        if re.search("Firefox", user, re.IGNORECASE):
            browsers["Firefox"] += 1
        elif re.search("Chrome", user, re.IGNORECASE):
            browsers["Chrome"] += 1
        elif re.search("Internet Explorer", user, re.IGNORECASE):
            browsers["Internet Explorer"] += 1
        elif re.search("Safari", user, re.IGNORECASE):
            browsers["Safari"] += 1

        try:
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            hour = timestamp.strftime("%H")

            if hour in hourly_counts:
                hourly_counts[hour] += 1
            else:
                hourly_counts[hour] = 1
        except Exception as e:
            logger.error(f"Error processing line # {total_hits}: {e}")

    return total_hits, image_hits, browsers, hourly_counts



def main(url):
    print(f"Running main with URL = {url}...")

    csv_text = download_data(url)

    total, img_count, browser_results, hour_results = process_data(csv_text)

    print("\n====Stats====")

    if total > 0:
        img_percent = (img_count / total) * 100
        print(f"\nImage requests account for {img_percent:.1f}% of all requests")

    popular_browser = max(browser_results, key=browser_results.get)
    print(f"Most popular browser is: {popular_browser}")

    print("Hourly Hits:")
    for h in sorted(hour_results.keys()):
        print(f"Hour{h} has {hour_results[h]} hits")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    
