#!/usr/bin/env python3
"""
Autism Speaks Resource Guide Scraper.
Scrapes autism service provider listings by state.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
from datetime import datetime

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
BASE_URL = "https://www.autismspeaks.org"
OUTPUT_DIR = os.path.expanduser("~/neurofamilies-data/autism-speaks")

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


def scrape_state(state_slug, state_abbr):
    """Scrape Autism Speaks resource guide for a state."""
    results = []
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    
    # Try the resource guide page for this state
    url = f"{BASE_URL}/resource-guide/{state_slug}"
    print(f"  Fetching: {url}")
    
    try:
        resp = session.get(url, timeout=20)
        if resp.status_code != 200:
            # Try alternate URL patterns
            url2 = f"{BASE_URL}/resource-guide?state={state_abbr}"
            resp = session.get(url2, timeout=20)
            if resp.status_code != 200:
                print(f"  Status: {resp.status_code}")
                return results
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Look for provider/listing elements
        # Autism Speaks uses various patterns
        listings = soup.select('[class*="resource"], [class*="listing"], [class*="provider"], [class*="result"]')
        print(f"  Found {len(listings)} listing elements")
        
        # Extract links to individual providers
        provider_links = soup.find_all('a', href=re.compile(r'/resource/(?:provider|listing|entry)'))
        if not provider_links:
            provider_links = soup.find_all('a', href=re.compile(r'/resource-guide/\w+'))
        
        print(f"  Provider links: {len(provider_links)}")
        
        for link in provider_links[:50]:
            href = link.get('href', '')
            name = link.get_text(strip=True)
            
            if not name or len(name) < 3 or len(name) > 150:
                continue
            
            # Skip navigation/category links
            if any(skip in name.lower() for skip in ['search', 'filter', 'category', 'state', 'page', 'next', 'previous']):
                continue
            
            results.append({
                "name": name,
                "url": BASE_URL + href if href.startswith('/') else href,
                "state": state_abbr,
                "state_full": state_slug.replace('-', ' ').title(),
                "source": "autismspeaks.org",
                "scraped_at": datetime.utcnow().isoformat()
            })
        
        # Also try to extract from JSON-LD or embedded data
        for script in soup.find_all('script', type='application/ld+json'):
            if script.string:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and data.get('@type') in ['LocalBusiness', 'MedicalBusiness']:
                        results.append({
                            "name": data.get('name', ''),
                            "url": data.get('url', ''),
                            "phone": data.get('telephone', ''),
                            "address": data.get('address', {}),
                            "state": state_abbr,
                            "source": "autismspeaks.org",
                            "scraped_at": datetime.utcnow().isoformat()
                        })
                except:
                    pass
        
        print(f"  Extracted {len(results)} resources")
        
    except Exception as e:
        print(f"  ERROR: {e}")
    
    return results


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_data = {}
    total = 0
    
    # Start with priority states
    priority = ["texas", "california", "new-york", "florida", "illinois",
                "ohio", "pennsylvania", "michigan", "georgia", "north-carolina"]
    
    # Process priority first, then rest
    states_to_scrape = priority + [s for s in US_STATES if s not in priority]
    
    for state_slug in states_to_scrape:
        state_abbr = US_STATES[state_slug]
        print(f"\nScraping Autism Speaks: {state_slug} ({state_abbr})...")
        
        results = scrape_state(state_slug, state_abbr)
        if results:
            all_data[state_abbr] = results
            total += len(results)
        
        time.sleep(2)
    
    # Save results
    output_file = os.path.join(OUTPUT_DIR, "all_resources.json")
    with open(output_file, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    # Save per-state
    for state_abbr, data in all_data.items():
        state_file = os.path.join(OUTPUT_DIR, f"{state_abbr.lower()}.json")
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Total resources: {total}")
    print(f"States with data: {len(all_data)}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
