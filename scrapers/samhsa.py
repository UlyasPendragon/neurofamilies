#!/usr/bin/env python3
"""
SAMHSA Treatment Locator Scraper.
Uses the FindTreatment.gov website to find mental health and substance abuse treatment.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
from datetime import datetime

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
OUTPUT_DIR = os.path.expanduser("~/neurofamilies-data/samhsa")

# Major cities to search by (geocode coordinates)
SEARCH_LOCATIONS = {
    "TX": [("Austin", 30.2672, -97.7431), ("Dallas", 32.7767, -96.7970), ("Houston", 29.7604, -95.3698)],
    "CA": [("Los Angeles", 34.0522, -118.2437), ("San Francisco", 37.7749, -122.4194), ("San Diego", 32.7157, -117.1611)],
    "NY": [("New York", 40.7128, -74.0060), ("Buffalo", 42.8864, -78.8784)],
    "FL": [("Miami", 25.7617, -80.1918), ("Tampa", 27.9506, -82.4572), ("Orlando", 28.5383, -81.3792)],
    "IL": [("Chicago", 41.8781, -87.6298)],
    "OH": [("Columbus", 39.9612, -82.9988), ("Cleveland", 41.4993, -81.6944)],
    "PA": [("Philadelphia", 39.9526, -75.1652), ("Pittsburgh", 40.4406, -79.9959)],
    "MI": [("Detroit", 42.3314, -83.0458)],
    "GA": [("Atlanta", 33.7490, -84.3880)],
    "NC": [("Charlotte", 35.2271, -80.8431), ("Raleigh", 35.7796, -78.6382)],
}


def scrape_samhsa_city(city, state, lat, lng, radius=25):
    """Scrape SAMHSA treatment facilities near a city."""
    results = []
    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    
    # SAMHSA uses a JS app, but we can try the search page and look for data
    url = f"https://findtreatment.gov/locator?sType=MH&sAddr={city}%2C+{state}&page=1"
    
    try:
        resp = session.get(url, timeout=20)
        if resp.status_code != 200:
            return results
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Look for facility data in the page
        # SAMHSA often embeds data in script tags
        for script in soup.find_all('script'):
            if script.string and 'facility' in script.string.lower():
                # Try to find JSON data
                json_matches = re.findall(r'\{[^{}]*"name"[^{}]*\}', script.string)
                for jm in json_matches[:5]:
                    try:
                        data = json.loads(jm)
                        results.append(data)
                    except:
                        pass
        
        # Also look for structured data
        for script in soup.find_all('script', type='application/ld+json'):
            if script.string:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, list):
                        results.extend(data)
                    else:
                        results.append(data)
                except:
                    pass
        
        print(f"    {city}, {state}: {len(results)} facilities")
        
    except Exception as e:
        print(f"    ERROR: {e}")
    
    return results


def generate_samhsa_data():
    """
    Since SAMHSA's site is a JS-heavy SPA, we'll generate known SAMHSA-funded
    program data from publicly available sources. This is more reliable than 
    scraping their SPA.
    """
    # SAMHSA publishes grant data and treatment episode data
    # We'll create entries based on known SAMHSA-funded programs
    facilities = []
    
    # Known SAMHSA program types for autism-relevant services
    program_types = [
        {"name": "Community Mental Health Center", "category": "mental-health", "services": ["outpatient therapy", "crisis intervention"]},
        {"name": "Certified Community Behavioral Health Clinic", "category": "mental-health", "services": ["outpatient therapy", "substance use", "crisis services"]},
        {"name": "Children's Mental Health Program", "category": "mental-health", "services": ["child therapy", "family therapy", "behavioral health"]},
    ]
    
    return facilities


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_data = {}
    total = 0
    
    for state, locations in SEARCH_LOCATIONS.items():
        print(f"\nScraping SAMHSA for {state}...")
        state_results = []
        
        for city, lat, lng in locations:
            results = scrape_samhsa_city(city, state, lat, lng)
            state_results.extend(results)
            time.sleep(2)
        
        if state_results:
            all_data[state] = state_results
            total += len(state_results)
    
    # Save
    output_file = os.path.join(OUTPUT_DIR, "samhsa_facilities.json")
    with open(output_file, 'w') as f:
        json.dump(all_data, f, indent=2, default=str)
    
    print(f"\n{'='*50}")
    print(f"Total facilities: {total}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
