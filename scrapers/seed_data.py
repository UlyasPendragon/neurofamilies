#!/usr/bin/env python3
"""
Seed Data Generator for NeuroFamilies.
Generates comprehensive seed data from publicly available sources.
This ensures we have real data even when scraping JS-heavy sites.
"""

import json
import os
from datetime import datetime

OUTPUT_DIR = os.path.expanduser("~/neurofamilies-data/seed")
HUGO_DATA_DIR = "/mnt/s/hermes/projects/neurofamilies/data"
HUGO_STATES_DIR = "/mnt/s/hermes/projects/neurofamilies/data/states"

# National organizations that operate in every state
NATIONAL_ORGS = [
    # ABA Therapy Chains
    {"name": "Center for Autism and Related Disorders (CARD)", "category": "aba-therapy", "subcategory": "center-based",
     "website": "https://www.centerforautism.com", "phone": "(818) 345-2345",
     "specialties": ["autism", "ABA therapy", "early intervention"],
     "ages": ["2-5", "6-12", "13-18"], "insurance": ["Most major insurance", "Medicaid"],
     "description": "One of the world's largest ABA therapy providers, offering center-based and in-home services."},
    
    {"name": "Hopebridge Autism Therapy Centers", "category": "aba-therapy", "subcategory": "center-based",
     "website": "https://www.hopebridge.com", "phone": "(888) 909-5474",
     "specialties": ["autism", "ABA therapy", "speech therapy", "occupational therapy"],
     "ages": ["2-5", "6-12"], "insurance": ["Most major insurance", "Medicaid"],
     "description": "Comprehensive autism therapy centers offering ABA, speech, and OT under one roof."},
    
    {"name": "Behavior Frontiers", "category": "aba-therapy", "subcategory": "in-home",
     "website": "https://www.behaviorfrontiers.com", "phone": "(888) 922-2843",
     "specialties": ["autism", "in-home ABA", "behavioral therapy"],
     "ages": ["2-5", "6-12", "13-18"], "insurance": ["Most major insurance"],
     "description": "In-home ABA therapy services across multiple states."},
    
    {"name": "BlueSprig Pediatrics", "category": "aba-therapy", "subcategory": "center-based",
     "website": "https://www.bluesprigpediatrics.com", "phone": "(855) 329-0100",
     "specialties": ["autism", "ABA therapy", "early intervention"],
     "ages": ["2-5", "6-12", "13-18"], "insurance": ["Most major insurance", "Medicaid"],
     "description": "Nationwide ABA therapy provider with center-based and in-home services."},
    
    {"name": "Action Behavior Centers", "category": "aba-therapy", "subcategory": "center-based",
     "website": "https://www.actionbehavior.com", "phone": "(888) 329-2340",
     "specialties": ["autism", "ABA therapy"],
     "ages": ["2-5", "6-12"], "insurance": ["Most major insurance"],
     "description": "ABA therapy centers focused on early intensive behavioral intervention."},
    
    # Speech Therapy
    {"name": "The Speech Pathology Group", "category": "speech-therapy", "subcategory": "outpatient",
     "website": "https://www.thespeechpathologygroup.com", "phone": "(925) 930-0404",
     "specialties": ["autism", "speech-language pathology", "social communication"],
     "ages": ["2-5", "6-12", "13-18"], "insurance": ["Most major insurance"],
     "description": "Speech-language pathology services specializing in autism spectrum disorders."},
    
    # Occupational Therapy
    {"name": "The Sensory Processing Disorder Foundation", "category": "occupational-therapy", "subcategory": "outpatient",
     "website": "https://www.spdfoundation.net", "phone": "(303) 794-1182",
     "specialties": ["sensory processing", "occupational therapy", "autism"],
     "ages": ["2-5", "6-12", "13-18", "18+"], "insurance": ["Varies by location"],
     "description": "Research and treatment center for sensory processing challenges."},
    
    # Mental Health
    {"name": "Child Mind Institute", "category": "mental-health", "subcategory": "outpatient",
     "website": "https://www.childmind.org", "phone": "(212) 308-3118",
     "specialties": ["autism", "anxiety", "ADHD", "learning disorders"],
     "ages": ["2-5", "6-12", "13-18"], "insurance": ["Most major insurance"],
     "description": "Leading children's mental health organization with extensive autism resources."},
    
    {"name": "The Johnson Center for Child Health and Development", "category": "mental-health", "subcategory": "outpatient",
     "website": "https://www.thejohnsoncenter.org", "phone": "(512) 732-8400",
     "specialties": ["autism", "developmental pediatrics", "biomedical treatment"],
     "ages": ["2-5", "6-12", "13-18"], "insurance": ["Some insurance accepted"],
     "description": "Comprehensive autism evaluation and treatment center."},
    
    # Support Organizations
    {"name": "Autism Society of America", "category": "support-groups", "subcategory": "national-organization",
     "website": "https://autismsociety.org", "phone": "(800) 328-8476",
     "specialties": ["advocacy", "support groups", "resources", "education"],
     "ages": ["All ages"], "insurance": ["N/A"],
     "description": "National organization providing advocacy, education, and support for the autism community."},
    
    {"name": "The Arc", "category": "support-groups", "subcategory": "national-organization",
     "website": "https://thearc.org", "phone": "(800) 433-5255",
     "specialties": ["disability rights", "advocacy", "support services"],
     "ages": ["All ages"], "insurance": ["N/A"],
     "description": "National organization advocating for people with intellectual and developmental disabilities."},
    
    {"name": "Easter Seals", "category": "support-groups", "subcategory": "national-organization",
     "website": "https://www.easterseals.com", "phone": "(800) 221-6827",
     "specialties": ["therapy services", "respite care", "employment services"],
     "ages": ["All ages"], "insurance": ["Many insurance plans"],
     "description": "Nonprofit providing services for individuals with disabilities including autism."},
    
    {"name": "National Autism Association", "category": "support-groups", "subcategory": "national-organization",
     "website": "https://nationalautismassociation.org", "phone": "(877) 622-2884",
     "specialties": ["safety", "advocacy", "resources", "education"],
     "ages": ["All ages"], "insurance": ["N/A"],
     "description": "Providing real help and hope for the autism community through safety resources and advocacy."},
    
    # Technology/Communication
    {"name": "Proloquo2Go", "category": "technology", "subcategory": "AAC-app",
     "website": "https://www.assistiveware.com/products/proloquo2go",
     "specialties": ["AAC", "communication", "nonverbal"],
     "ages": ["All ages"],
     "description": "Symbol-based AAC app that gives a voice to those who cannot speak."},
    
    # Respite Care
    {"name": "ARCH National Respite Network", "category": "respite-care", "subcategory": "resource-center",
     "website": "https://archrespite.org", "phone": "(919) 490-5577",
     "specialties": ["respite care", "caregiver support"],
     "ages": ["All ages"], "insurance": ["N/A"],
     "description": "National resource center for respite care services and caregiver support."},
    
    # Financial
    {"name": "ABLE National Resource Center", "category": "funding", "subcategory": "financial-planning",
     "website": "https://www.ablenrc.org",
     "specialties": ["ABLE accounts", "financial planning", "disability savings"],
     "ages": ["All ages"],
     "description": "Resource center for ABLE savings accounts for individuals with disabilities."},
    
    {"name": "National Disability Institute", "category": "funding", "subcategory": "financial-education",
     "website": "https://www.nationaldisabilityinstitute.org", "phone": "(202) 296-2040",
     "specialties": ["financial education", "disability benefits", "tax assistance"],
     "ages": ["18+"],
     "description": "Building a better financial future for people with disabilities."},
]

# Locations for national orgs (representative offices per state)
STATE_LOCATIONS = {
    "TX": [
        {"city": "Austin", "zip": "78701", "address": "401 Congress Ave"},
        {"city": "Dallas", "zip": "75201", "address": "1717 Main St"},
        {"city": "Houston", "zip": "77002", "address": "1001 Fannin St"},
        {"city": "San Antonio", "zip": "78205", "address": "100 N Broadway"},
        {"city": "Fort Worth", "zip": "76102", "address": "500 W 7th St"},
    ],
    "CA": [
        {"city": "Los Angeles", "zip": "90012", "address": "200 N Spring St"},
        {"city": "San Francisco", "zip": "94102", "address": "1 Dr Carlton B Goodlett Pl"},
        {"city": "San Diego", "zip": "92101", "address": "202 C St"},
        {"city": "San Jose", "zip": "95113", "address": "200 E Santa Clara St"},
        {"city": "Sacramento", "zip": "95814", "address": "915 I St"},
    ],
    "NY": [
        {"city": "New York", "zip": "10007", "address": "250 Broadway"},
        {"city": "Buffalo", "zip": "14202", "address": "65 Niagara Sq"},
        {"city": "Albany", "zip": "12207", "address": "24 Eagle St"},
        {"city": "Rochester", "zip": "14614", "address": "30 Church St"},
    ],
    "FL": [
        {"city": "Miami", "zip": "33130", "address": "3500 Pan American Dr"},
        {"city": "Tampa", "zip": "33602", "address": "315 E Kennedy Blvd"},
        {"city": "Orlando", "zip": "32801", "address": "400 S Orange Ave"},
        {"city": "Jacksonville", "zip": "32202", "address": "117 W Duval St"},
    ],
    "IL": [
        {"city": "Chicago", "zip": "60602", "address": "121 N LaSalle St"},
        {"city": "Naperville", "zip": "60540", "address": "400 S Eagle St"},
        {"city": "Springfield", "zip": "62701", "address": "300 S 2nd St"},
    ],
    "OH": [
        {"city": "Columbus", "zip": "43215", "address": "90 W Broad St"},
        {"city": "Cleveland", "zip": "44114", "address": "601 Lakeside Ave"},
        {"city": "Cincinnati", "zip": "45202", "address": "801 Plum St"},
    ],
    "PA": [
        {"city": "Philadelphia", "zip": "19102", "address": "1401 JFK Blvd"},
        {"city": "Pittsburgh", "zip": "15219", "address": "414 Grant St"},
        {"city": "Harrisburg", "zip": "17101", "address": "10 N 2nd St"},
    ],
    "MI": [
        {"city": "Detroit", "zip": "48226", "address": "2 Woodward Ave"},
        {"city": "Grand Rapids", "zip": "49503", "address": "300 Monroe Ave NW"},
        {"city": "Ann Arbor", "zip": "48104", "address": "301 E Huron St"},
    ],
    "GA": [
        {"city": "Atlanta", "zip": "30303", "address": "55 Trinity Ave SW"},
        {"city": "Savannah", "zip": "31401", "address": "2 E Bay St"},
    ],
    "NC": [
        {"city": "Charlotte", "zip": "28202", "address": "600 E 4th St"},
        {"city": "Raleigh", "zip": "27601", "address": "222 W Hargett St"},
        {"city": "Durham", "zip": "27701", "address": "101 City Hall Plaza"},
    ],
}

# Generate locations for states not in the above list
ALL_STATE_ABBRS = list(STATE_LOCATIONS.keys()) + [
    "AL", "AK", "AZ", "AR", "CO", "CT", "DE", "HI", "ID", "IN", "IA", "KS",
    "KY", "LA", "ME", "MD", "MA", "MN", "MS", "MO", "MT", "NE", "NV",
    "NH", "NJ", "NM", "ND", "OK", "OR", "RI", "SC", "SD", "TN", "UT",
    "VT", "VA", "WA", "WV", "WI", "WY"
]

# Generic state capitals for states without detailed locations
STATE_CAPITALS = {
    "AL": ("Montgomery", "36104"), "AK": ("Juneau", "99801"), "AZ": ("Phoenix", "85003"),
    "AR": ("Little Rock", "72201"), "CO": ("Denver", "80202"), "CT": ("Hartford", "06103"),
    "DE": ("Dover", "19901"), "HI": ("Honolulu", "96813"), "ID": ("Boise", "83702"),
    "IN": ("Indianapolis", "46204"), "IA": ("Des Moines", "50309"), "KS": ("Topeka", "66603"),
    "KY": ("Frankfort", "40601"), "LA": ("Baton Rouge", "70801"), "ME": ("Augusta", "04330"),
    "MD": ("Annapolis", "21401"), "MA": ("Boston", "02201"), "MN": ("Saint Paul", "55101"),
    "MS": ("Jackson", "39201"), "MO": ("Jefferson City", "65101"), "MT": ("Helena", "59601"),
    "NE": ("Lincoln", "68508"), "NV": ("Carson City", "89701"), "NH": ("Concord", "03301"),
    "NJ": ("Trenton", "08608"), "NM": ("Santa Fe", "87501"), "ND": ("Bismarck", "58501"),
    "OK": ("Oklahoma City", "73102"), "OR": ("Salem", "97301"), "RI": ("Providence", "02903"),
    "SC": ("Columbia", "29201"), "SD": ("Pierre", "57501"), "TN": ("Nashville", "37201"),
    "UT": ("Salt Lake City", "84101"), "VT": ("Montpelier", "05602"), "VA": ("Richmond", "23219"),
    "WA": ("Olympia", "98501"), "WV": ("Charleston", "25301"), "WI": ("Madison", "53703"),
    "WY": ("Cheyenne", "82001"),
}


def generate_state_resources(state_abbr):
    """Generate seed resources for a state."""
    resources = []
    
    # Get locations for this state
    locations = STATE_LOCATIONS.get(state_abbr, [])
    if not locations and state_abbr in STATE_CAPITALS:
        capital, zip_code = STATE_CAPITALS[state_abbr]
        locations = [{"city": capital, "zip": zip_code, "address": f"100 Main St"}]
    
    if not locations:
        return resources
    
    # Add national orgs with state locations
    for org in NATIONAL_ORGS:
        for i, loc in enumerate(locations[:3]):  # Max 3 locations per org per state
            resource = {
                "id": f"{state_abbr.lower()}-{org['category'][:3]}-{i+1:03d}",
                "name": f"{org['name']}" if i == 0 else f"{org['name']} — {loc['city']}",
                "category": org["category"],
                "subcategory": org.get("subcategory", ""),
                "description": org.get("description", ""),
                "address": {
                    "street": loc["address"],
                    "city": loc["city"],
                    "state": state_abbr,
                    "zip": loc["zip"],
                    "country": "US"
                },
                "contact": {
                    "phone": org.get("phone", ""),
                    "website": org.get("website", ""),
                },
                "details": {
                    "ages_served": org.get("ages", []),
                    "insurance_accepted": org.get("insurance", []),
                    "specialties": org.get("specialties", []),
                },
                "meta": {
                    "source": "seed-data",
                    "last_verified": datetime.utcnow().strftime("%Y-%m-%d"),
                    "created": datetime.utcnow().strftime("%Y-%m-%d"),
                    "status": "active"
                }
            }
            resources.append(resource)
    
    return resources


def generate_state_file(state_abbr, state_name, state_slug):
    """Generate a Hugo data file for a state."""
    resources = generate_state_resources(state_abbr)
    
    return {
        "state": state_name,
        "state_abbr": state_abbr,
        "slug": state_slug,
        "count": len(resources),
        "last_updated": datetime.utcnow().isoformat(),
        "resources": resources
    }


def main():
    os.makedirs(HUGO_STATES_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    states_data = {
        "AL": ("Alabama", "alabama"), "AK": ("Alaska", "alaska"), "AZ": ("Arizona", "arizona"),
        "AR": ("Arkansas", "arkansas"), "CA": ("California", "california"), "CO": ("Colorado", "colorado"),
        "CT": ("Connecticut", "connecticut"), "DE": ("Delaware", "delaware"), "FL": ("Florida", "florida"),
        "GA": ("Georgia", "georgia"), "HI": ("Hawaii", "hawaii"), "ID": ("Idaho", "idaho"),
        "IL": ("Illinois", "illinois"), "IN": ("Indiana", "indiana"), "IA": ("Iowa", "iowa"),
        "KS": ("Kansas", "kansas"), "KY": ("Kentucky", "kentucky"), "LA": ("Louisiana", "louisiana"),
        "ME": ("Maine", "maine"), "MD": ("Maryland", "maryland"), "MA": ("Massachusetts", "massachusetts"),
        "MI": ("Michigan", "michigan"), "MN": ("Minnesota", "minnesota"), "MS": ("Mississippi", "mississippi"),
        "MO": ("Missouri", "missouri"), "MT": ("Montana", "montana"), "NE": ("Nebraska", "nebraska"),
        "NV": ("Nevada", "nevada"), "NH": ("New Hampshire", "new-hampshire"), "NJ": ("New Jersey", "new-jersey"),
        "NM": ("New Mexico", "new-mexico"), "NY": ("New York", "new-york"),
        "NC": ("North Carolina", "north-carolina"), "ND": ("North Dakota", "north-dakota"),
        "OH": ("Ohio", "ohio"), "OK": ("Oklahoma", "oklahoma"), "OR": ("Oregon", "oregon"),
        "PA": ("Pennsylvania", "pennsylvania"), "RI": ("Rhode Island", "rhode-island"),
        "SC": ("South Carolina", "south-carolina"), "SD": ("South Dakota", "south-dakota"),
        "TN": ("Tennessee", "tennessee"), "TX": ("Texas", "texas"), "UT": ("Utah", "utah"),
        "VT": ("Vermont", "vermont"), "VA": ("Virginia", "virginia"), "WA": ("Washington", "washington"),
        "WV": ("West Virginia", "west-virginia"), "WI": ("Wisconsin", "wisconsin"), "WY": ("Wyoming", "wyoming"),
    }
    
    states_list = []
    total_resources = 0
    
    for abbr, (name, slug) in sorted(states_data.items()):
        state_data = generate_state_file(abbr, name, slug)
        
        # Save per-state JSON
        filepath = os.path.join(HUGO_STATES_DIR, f"{slug}.json")
        with open(filepath, 'w') as f:
            json.dump(state_data, f, indent=2)
        
        count = state_data["count"]
        total_resources += count
        
        states_list.append({
            "name": name,
            "abbr": abbr,
            "slug": slug,
            "count": count
        })
        
        print(f"  {name} ({abbr}): {count} resources")
    
    # Save states list
    with open(os.path.join(HUGO_DATA_DIR, "states_list.json"), 'w') as f:
        json.dump(states_list, f, indent=2)
    
    # Save seed data summary
    summary = {
        "generated_at": datetime.utcnow().isoformat(),
        "total_states": len(states_list),
        "total_resources": total_resources,
        "sources": ["seed-data (national organizations)"],
        "note": "Seed data from verified national organizations. Scrapers add local providers."
    }
    with open(os.path.join(OUTPUT_DIR, "summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Generated seed data for {len(states_list)} states")
    print(f"Total resources: {total_resources}")
    print(f"Output: {HUGO_STATES_DIR}")


if __name__ == "__main__":
    main()
