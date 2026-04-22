#!/usr/bin/env python3
"""
Master runner for all NeuroFamilies scrapers.
Runs all scrapers and generates Hugo-compatible data files.
"""

import subprocess
import json
import os
import sys
from datetime import datetime
from collections import defaultdict

DATA_DIR = os.path.expanduser("~/neurofamilies-data")
HUGO_DATA_DIR = "/mnt/s/hermes/projects/neurofamilies/data"
HUGO_STATES_DIR = "/mnt/s/hermes/projects/neurofamilies/data/states"

# State info
STATE_INFO = {
    "AL": {"name": "Alabama", "slug": "alabama"}, "AK": {"name": "Alaska", "slug": "alaska"},
    "AZ": {"name": "Arizona", "slug": "arizona"}, "AR": {"name": "Arkansas", "slug": "arkansas"},
    "CA": {"name": "California", "slug": "california"}, "CO": {"name": "Colorado", "slug": "colorado"},
    "CT": {"name": "Connecticut", "slug": "connecticut"}, "DE": {"name": "Delaware", "slug": "delaware"},
    "FL": {"name": "Florida", "slug": "florida"}, "GA": {"name": "Georgia", "slug": "georgia"},
    "HI": {"name": "Hawaii", "slug": "hawaii"}, "ID": {"name": "Idaho", "slug": "idaho"},
    "IL": {"name": "Illinois", "slug": "illinois"}, "IN": {"name": "Indiana", "slug": "indiana"},
    "IA": {"name": "Iowa", "slug": "iowa"}, "KS": {"name": "Kansas", "slug": "kansas"},
    "KY": {"name": "Kentucky", "slug": "kentucky"}, "LA": {"name": "Louisiana", "slug": "louisiana"},
    "ME": {"name": "Maine", "slug": "maine"}, "MD": {"name": "Maryland", "slug": "maryland"},
    "MA": {"name": "Massachusetts", "slug": "massachusetts"}, "MI": {"name": "Michigan", "slug": "michigan"},
    "MN": {"name": "Minnesota", "slug": "minnesota"}, "MS": {"name": "Mississippi", "slug": "mississippi"},
    "MO": {"name": "Missouri", "slug": "missouri"}, "MT": {"name": "Montana", "slug": "montana"},
    "NE": {"name": "Nebraska", "slug": "nebraska"}, "NV": {"name": "Nevada", "slug": "nevada"},
    "NH": {"name": "New Hampshire", "slug": "new-hampshire"}, "NJ": {"name": "New Jersey", "slug": "new-jersey"},
    "NM": {"name": "New Mexico", "slug": "new-mexico"}, "NY": {"name": "New York", "slug": "new-york"},
    "NC": {"name": "North Carolina", "slug": "north-carolina"}, "ND": {"name": "North Dakota", "slug": "north-dakota"},
    "OH": {"name": "Ohio", "slug": "ohio"}, "OK": {"name": "Oklahoma", "slug": "oklahoma"},
    "OR": {"name": "Oregon", "slug": "oregon"}, "PA": {"name": "Pennsylvania", "slug": "pennsylvania"},
    "RI": {"name": "Rhode Island", "slug": "rhode-island"}, "SC": {"name": "South Carolina", "slug": "south-carolina"},
    "SD": {"name": "South Dakota", "slug": "south-dakota"}, "TN": {"name": "Tennessee", "slug": "tennessee"},
    "TX": {"name": "Texas", "slug": "texas"}, "UT": {"name": "Utah", "slug": "utah"},
    "VT": {"name": "Vermont", "slug": "vermont"}, "VA": {"name": "Virginia", "slug": "virginia"},
    "WA": {"name": "Washington", "slug": "washington"}, "WV": {"name": "West Virginia", "slug": "west-virginia"},
    "WI": {"name": "Wisconsin", "slug": "wisconsin"}, "WY": {"name": "Wyoming", "slug": "wyoming"},
    # Canada
    "AB": {"name": "Alberta", "slug": "alberta"}, "BC": {"name": "British Columbia", "slug": "british-columbia"},
    "ON": {"name": "Ontario", "slug": "ontario"}, "QC": {"name": "Quebec", "slug": "quebec"},
}


def run_scraper(script_name):
    """Run a scraper script and return success status."""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True, text=True, timeout=300
        )
        print(result.stdout[-2000:] if result.stdout else "")
        if result.stderr:
            print(f"STDERR: {result.stderr[-500:]}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("TIMEOUT after 300s")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def collect_data():
    """Collect all scraped data and merge into unified format."""
    all_resources = defaultdict(list)
    
    # Read from all scraper output directories
    for scraper_dir in ["psychology-today", "autism-speaks", "autism-society", "samhsa"]:
        dir_path = os.path.join(DATA_DIR, scraper_dir)
        if not os.path.exists(dir_path):
            print(f"  Skipping {scraper_dir}: directory not found")
            continue
        
        for filename in os.listdir(dir_path):
            if filename.endswith('.json') and filename != 'all_therapists.json' and filename != 'all_resources.json':
                state = filename.replace('.json', '').upper()
                filepath = os.path.join(dir_path, filename)
                
                try:
                    with open(filepath) as f:
                        data = json.load(f)
                    
                    if isinstance(data, list):
                        for item in data:
                            item['source_scraper'] = scraper_dir
                        all_resources[state].extend(data)
                        print(f"  {scraper_dir}/{filename}: {len(data)} resources")
                except Exception as e:
                    print(f"  Error reading {filepath}: {e}")
        
        # Also check the consolidated files
        for consolidated in ['all_therapists.json', 'all_resources.json']:
            filepath = os.path.join(dir_path, consolidated)
            if os.path.exists(filepath):
                try:
                    with open(filepath) as f:
                        data = json.load(f)
                    if isinstance(data, dict):
                        for state, items in data.items():
                            if isinstance(items, list):
                                for item in items:
                                    item['source_scraper'] = scraper_dir
                                all_resources[state].extend(items)
                        print(f"  {scraper_dir}/{consolidated}: {sum(len(v) for v in data.values() if isinstance(v, list))} resources")
                except Exception as e:
                    print(f"  Error reading {filepath}: {e}")
    
    return all_resources


def generate_hugo_data(all_resources):
    """Generate Hugo-compatible data files."""
    os.makedirs(HUGO_STATES_DIR, exist_ok=True)
    
    # Generate per-state JSON files for Hugo
    states_list = []
    total_count = 0
    
    for state_abbr, info in sorted(STATE_INFO.items()):
        resources = all_resources.get(state_abbr, [])
        count = len(resources)
        total_count += count
        
        # Generate state data file
        state_data = {
            "state": info["name"],
            "state_abbr": state_abbr,
            "slug": info["slug"],
            "count": count,
            "last_updated": datetime.utcnow().isoformat(),
            "resources": resources[:100]  # Limit for now
        }
        
        state_file = os.path.join(HUGO_STATES_DIR, f"{info['slug']}.json")
        with open(state_file, 'w') as f:
            json.dump(state_data, f, indent=2)
        
        states_list.append({
            "name": info["name"],
            "abbr": state_abbr,
            "slug": info["slug"],
            "count": count
        })
    
    # Update states_list.json
    states_list_file = os.path.join(HUGO_DATA_DIR, "states_list.json")
    with open(states_list_file, 'w') as f:
        json.dump(states_list, f, indent=2)
    
    print(f"\nGenerated Hugo data:")
    print(f"  States: {len(states_list)}")
    print(f"  Total resources: {total_count}")
    print(f"  Data dir: {HUGO_DATA_DIR}")
    
    return total_count


def main():
    print("NeuroFamilies Scraper Suite")
    print(f"Data directory: {DATA_DIR}")
    print(f"Hugo data directory: {HUGO_DATA_DIR}")
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    
    # Run scrapers
    scrapers = [
        "psychology_today.py",
        "autism_speaks.py",
        "autism_society.py",
    ]
    
    for scraper in scrapers:
        run_scraper(scraper)
    
    # Collect and merge data
    print(f"\n{'='*60}")
    print("Collecting and merging data...")
    print(f"{'='*60}")
    
    all_resources = collect_data()
    
    # Generate Hugo data
    total = generate_hugo_data(all_resources)
    
    print(f"\n{'='*60}")
    print(f"DONE — {total} total resources across {len(all_resources)} states")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
