#!/usr/bin/env python3
"""
Scrape Psychology Today for autism-specialized therapists.
Output: JSON data files per state.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
from datetime import datetime

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
BASE_URL = "https://www.psychologytoday.com"
OUTPUT_DIR = os.path.expanduser("~/neurofamilies-data/psychology-today")

# US states with abbreviations
US_STATES = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new-hampshire": "NH", "new-jersey": "NJ", "new-mexico": "NM", "new-york": "NY",
    "north-carolina": "NC", "north-dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode-island": "RI", "south-carolina": "SC",
    "south-dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA", "west-virginia": "WV",
    "wisconsin": "WI", "wyoming": "WY"
}

# Major cities per state (for multi-city scraping)
STATE_CITIES = {
    "texas": ["austin", "dallas", "houston", "san-antonio", "fort-worth", "el-paso"],
    "california": ["los-angeles", "san-francisco", "san-diego", "san-jose", "sacramento"],
    "new-york": ["new-york-city", "buffalo", "albany", "rochester", "syracuse"],
    "florida": ["miami", "tampa", "orlando", "jacksonville", "fort-lauderdale"],
    "illinois": ["chicago", "naperville", "springfield", "rockford"],
}


def scrape_state(state_slug, state_abbr, max_pages=3):
    """Scrape therapist listings for a state."""
    results = []
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    
    url = f"{BASE_URL}/us/therapists/autism/{state_slug}"
    print(f"  Fetching: {url}")
    
    try:
        resp = session.get(url, timeout=20)
        if resp.status_code != 200:
            print(f"  ERROR: Status {resp.status_code}")
            return results
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Find therapist profile links and extract info
        # PT uses specific patterns in their HTML
        profile_links = soup.find_all('a', href=re.compile(r'/us/therapists/[^/]+/[^/]+/'))
        
        seen_urls = set()
        for link in profile_links:
            href = link.get('href', '')
            if href in seen_urls or '/autism' in href or not re.match(r'/us/therapists/[a-z-]+/[a-z-]+/[a-z-]+-\w+', href):
                continue
            seen_urls.add(href)
            
            # Extract name and location from link text or parent
            name = link.get_text(strip=True)
            if not name or len(name) < 3 or len(name) > 100:
                continue
            
            # Try to get city from URL
            parts = href.split('/')
            city = parts[4] if len(parts) > 4 else ""
            city_name = city.replace('-', ' ').title() if city else ""
            
            results.append({
                "name": name,
                "url": BASE_URL + href,
                "city_slug": city,
                "city": city_name,
                "state": state_abbr,
                "state_full": state_slug.replace('-', ' ').title(),
                "source": "psychologytoday.com",
                "category": "mental-health",
                "subcategory": "therapist",
                "specialties": ["autism"],
                "scraped_at": datetime.utcnow().isoformat()
            })
        
        print(f"  Found {len(results)} therapists")
        
    except Exception as e:
        print(f"  ERROR: {e}")
    
    return results


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_data = {}
    total = 0
    
    # Start with priority states
    priority_states = ["texas", "california", "new-york", "florida", "illinois",
                       "ohio", "pennsylvania", "michigan", "georgia", "north-carolina"]
    
    # Scrape all states
    for state_slug in US_STATES:
        state_abbr = US_STATES[state_slug]
        print(f"\nScraping {state_slug} ({state_abbr})...")
        
        results = scrape_state(state_slug, state_abbr)
        if results:
            all_data[state_abbr] = results
            total += len(results)
        
        time.sleep(2)  # Be polite
    
    # Save results
    output_file = os.path.join(OUTPUT_DIR, "all_therapists.json")
    with open(output_file, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    # Save per-state files
    for state_abbr, data in all_data.items():
        state_file = os.path.join(OUTPUT_DIR, f"{state_abbr.lower()}.json")
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Total therapists scraped: {total}")
    print(f"States with data: {len(all_data)}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
