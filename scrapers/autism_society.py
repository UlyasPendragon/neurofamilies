#!/usr/bin/env python3
"""
Autism Society — Autism Source Scraper.
35,000+ listings of autism service providers.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
from datetime import datetime

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
BASE_URL = "https://source.autismsociety.org"
OUTPUT_DIR = os.path.expanduser("~/neurofamilies-data/autism-society")

US_STATES = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY"
}


def scrape_state(state_name, state_abbr):
    """Scrape Autism Source for a state."""
    results = []
    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    
    # Autism Source search URL
    url = f"{BASE_URL}/autismsource/s/"
    params = {"state": state_name}
    
    print(f"  Fetching: {url}?state={state_name}")
    
    try:
        resp = session.get(url, params=params, timeout=20)
        if resp.status_code != 200:
            print(f"  Status: {resp.status_code}")
            return results
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Look for listing elements
        listings = soup.select('[class*="listing"], [class*="result"], [class*="provider"], tr, .row')
        
        for listing in listings:
            text = listing.get_text(strip=True)
            if len(text) < 20 or len(text) > 2000:
                continue
            
            # Try to extract structured info
            links = listing.find_all('a')
            name = ""
            url = ""
            phone = ""
            
            for link in links:
                href = link.get('href', '')
                link_text = link.get_text(strip=True)
                if 'http' in href and len(link_text) > 3:
                    name = link_text
                    url = href
                    break
            
            # Look for phone numbers
            phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
            if phone_match:
                phone = phone_match.group(1)
            
            if name:
                results.append({
                    "name": name,
                    "url": url,
                    "phone": phone,
                    "state": state_abbr,
                    "state_full": state_name,
                    "source": "autismsociety.org",
                    "scraped_at": datetime.utcnow().isoformat()
                })
        
        print(f"  Found {len(results)} listings")
        
    except Exception as e:
        print(f"  ERROR: {e}")
    
    return results


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_data = {}
    total = 0
    
    # Start with priority states
    priority = ["Texas", "California", "New York", "Florida", "Illinois"]
    
    states_to_scrape = priority + [s for s in US_STATES if s not in priority]
    
    for state_name in states_to_scrape:
        state_abbr = US_STATES[state_name]
        print(f"\nScraping Autism Society: {state_name} ({state_abbr})...")
        
        results = scrape_state(state_name, state_abbr)
        if results:
            all_data[state_abbr] = results
            total += len(results)
        
        time.sleep(2)
    
    # Save
    output_file = os.path.join(OUTPUT_DIR, "all_resources.json")
    with open(output_file, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Total resources: {total}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
