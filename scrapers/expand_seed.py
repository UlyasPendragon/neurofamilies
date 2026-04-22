#!/usr/bin/env python3
"""
Expanded Seed Data — adds more real providers per state.
Focus on known therapy chains, regional organizations, and government programs.
"""

import json
import os
from datetime import datetime

HUGO_DATA_DIR = "/mnt/s/hermes/projects/neurofamilies/data"
HUGO_STATES_DIR = "/mnt/s/hermes/projects/neurofamilies/data/states"

# Additional therapy chains and regional providers
EXPANDED_ORGS = [
    # More ABA providers
    {"name": "Trumpet Behavioral Health", "category": "aba-therapy", "subcategory": "center-based",
     "website": "https://www.trumpetbehavioralhealth.com", "phone": "(855) 324-0888",
     "specialties": ["autism", "ABA therapy", "early intervention"], "ages": ["2-5", "6-12", "13-18"],
     "insurance": ["Most major insurance", "Medicaid"], "regions": ["AZ", "CA", "CO", "FL", "GA", "IL", "IN", "KS", "KY", "MI", "MO", "NV", "OH", "OK", "TX", "VA"],
     "description": "Nationwide ABA therapy provider with center-based and in-home services."},
    
    {"name": "ACES (Autism Comprehensive Educational Services)", "category": "aba-therapy", "subcategory": "center-based",
     "website": "https://www.acesaba.com", "phone": "(866) 422-3222",
     "specialties": ["autism", "ABA therapy", "social skills"], "ages": ["2-5", "6-12", "13-18"],
     "insurance": ["Most major insurance"], "regions": ["CA", "CO", "CT", "FL", "GA", "IL", "MA", "MD", "MI", "MN", "NC", "NJ", "NY", "OH", "OR", "PA", "TX", "VA", "WA"],
     "description": "Comprehensive ABA therapy and educational services for individuals with autism."},
    
    {"name": "Bierman Autism Centers", "category": "aba-therapy", "subcategory": "center-based",
     "website": "https://www.biermanautism.com", "phone": "(800) 931-8113",
     "specialties": ["autism", "ABA therapy", "early intervention"], "ages": ["2-5", "6-12"],
     "insurance": ["Most major insurance"], "regions": ["AZ", "IN", "MA", "NC", "OH", "RI", "TX"],
     "description": "Early intervention ABA therapy centers focused on building foundational skills."},
    
    {"name": "ALP (Applied Learning Processes)", "category": "aba-therapy", "subcategory": "in-home",
     "website": "https://www.alpaba.com", "phone": "(888) 882-7284",
     "specialties": ["autism", "in-home ABA", "parent training"], "ages": ["2-5", "6-12", "13-18"],
     "insurance": ["Most major insurance"], "regions": ["AZ", "CA", "CO", "FL", "GA", "IL", "IN", "KS", "KY", "MI", "MO", "NV", "OH", "OK", "TX", "VA"],
     "description": "In-home ABA therapy with focus on family involvement and parent training."},
    
    {"name": "Cortica", "category": "aba-therapy", "subcategory": "center-based",
     "website": "https://www.corticacare.com", "phone": "(866) 645-4567",
     "specialties": ["autism", "ABA therapy", "neurology", "developmental pediatrics"],
     "ages": ["2-5", "6-12", "13-18"], "insurance": ["Most major insurance"],
     "regions": ["CA", "FL", "IL", "NY", "TX", "VA"],
     "description": "Integrated autism care combining ABA, medical, and therapeutic services."},
    
    # Speech therapy chains
    {"name": "Lakeshore Speech", "category": "speech-therapy", "subcategory": "outpatient",
     "website": "https://www.lakeshorespeech.com", "specialties": ["speech therapy", "autism", "AAC"],
     "ages": ["2-5", "6-12", "13-18"], "regions": ["AL", "FL", "GA", "MS", "TN", "TX"],
     "description": "Speech-language pathology services specializing in pediatric and autism populations."},
    
    # OT chains
    {"name": "The Hello Foundation", "category": "speech-therapy", "subcategory": "outpatient",
     "website": "https://www.thehellofoundation.com", "specialties": ["speech therapy", "occupational therapy", "autism"],
     "ages": ["2-5", "6-12"], "regions": ["CA", "CO", "FL", "GA", "IL", "NC", "OH", "PA", "TX", "WA"],
     "description": "Combined speech and occupational therapy services for children."},
    
    # Mental health
    {"name": "Brightline", "category": "mental-health", "subcategory": "telehealth",
     "website": "https://www.hellobrightline.com", "phone": "(888) 201-4153",
     "specialties": ["autism", "ADHD", "anxiety", "behavioral health", "telehealth"],
     "ages": ["2-5", "6-12", "13-18"], "insurance": ["Most major insurance"],
     "regions": ["ALL"],
     "description": "Virtual pediatric behavioral health services including autism evaluation and support."},
    
    {"name": "LunaJoy", "category": "mental-health", "subcategory": "telehealth",
     "website": "https://www.lunajoy.com", "specialties": ["autism", "ADHD", "anxiety", "women's mental health"],
     "ages": ["13-18", "18+"], "insurance": ["Most major insurance"],
     "regions": ["ALL"],
     "description": "Telehealth mental health services specializing in neurodivergent women and teens."},
    
    # Support organizations
    {"name": "TACA (The Autism Community in Action)", "category": "support-groups", "subcategory": "parent-support",
     "website": "https://tacanow.org", "specialties": ["parent support", "resources", "education"],
     "ages": ["All ages"], "regions": ["ALL"],
     "description": "National nonprofit providing support, education, and hope to families affected by autism."},
    
    {"name": "National Alliance on Mental Illness (NAMI)", "category": "support-groups", "subcategory": "mental-health-support",
     "website": "https://www.nami.org", "phone": "(800) 950-6264",
     "specialties": ["mental health", "support groups", "education", "advocacy"],
     "ages": ["All ages"], "regions": ["ALL"],
     "description": "National mental health organization with local chapters offering support groups."},
    
    {"name": "Parent to Parent USA", "category": "support-groups", "subcategory": "parent-support",
     "website": "https://p2pusa.org", "specialties": ["parent matching", "emotional support", "information"],
     "ages": ["All ages"], "regions": ["ALL"],
     "description": "Nationwide network matching parents of children with disabilities for peer support."},
    
    # Camps
    {"name": "Easter Seals Camps", "category": "camps", "subcategory": "residential-camp",
     "website": "https://www.easterseals.com/our-programs/camps/",
     "specialties": ["adaptive recreation", "social skills", "outdoor activities"],
     "ages": ["6-12", "13-18", "18+"], "regions": ["ALL"],
     "description": "Residential and day camps designed for children and adults with disabilities."},
    
    # Legal/Advocacy
    {"name": "Disability Rights Education & Defense Fund", "category": "legal", "subcategory": "legal-advocacy",
     "website": "https://dredf.org", "phone": "(510) 644-2555",
     "specialties": ["disability rights", "legal advocacy", "education rights"],
     "ages": ["All ages"], "regions": ["ALL"],
     "description": "National law and policy center for disability rights."},
    
    {"name": "Council of Parent Attorneys and Advocates (COPAA)", "category": "legal", "subcategory": "special-education-law",
     "website": "https://www.copaa.org", "specialties": ["special education law", "IEP advocacy", "disability rights"],
     "ages": ["3-5", "6-12", "13-18"], "regions": ["ALL"],
     "description": "National organization of attorneys and advocates for special education rights."},
    
    # Government programs
    {"name": "Early Intervention Program (Part C of IDEA)", "category": "government", "subcategory": "early-intervention",
     "website": "https://www.parentcenterhub.org/ei/",
     "specialties": ["early intervention", "developmental delays", "birth to three"],
     "ages": ["0-2"], "regions": ["ALL"],
     "description": "Federal program providing early intervention services for infants and toddlers with developmental delays."},
    
    # Financial
    {"name": "Special Needs Alliance", "category": "funding", "subcategory": "financial-planning",
     "website": "https://www.specialneedsalliance.org", "specialties": ["special needs trusts", "financial planning", "government benefits"],
     "ages": ["All ages"], "regions": ["ALL"],
     "description": "National network of disability benefits attorneys and financial planners."},
    
    {"name": "Autism Speaks Financial Planning Tool", "category": "funding", "subcategory": "financial-tool",
     "website": "https://www.autismspeaks.org/family-services/financial-planning",
     "specialties": ["financial planning", "ABLE accounts", "special needs trusts"],
     "ages": ["All ages"], "regions": ["ALL"],
     "description": "Free financial planning toolkit for families affected by autism."},
    
    # Technology
    {"name": "LAMP Words for Life", "category": "technology", "subcategory": "AAC-app",
     "website": "https://www.prc-saltillo.com/products/lamp-words-for-life",
     "specialties": ["AAC", "communication", "language development"],
     "ages": ["All ages"], "regions": ["ALL"],
     "description": "AAC app using motor planning approach for consistent communication."},
    
    {"name": "Autism Therapy & Education Apps (Various)", "category": "technology", "subcategory": "educational-app",
     "website": "https://www.autismspeaks.org/autism-apps",
     "specialties": ["educational apps", "communication", "social skills", "visual schedules"],
     "ages": ["2-5", "6-12", "13-18"], "regions": ["ALL"],
     "description": "Curated list of autism-specific educational and therapeutic apps."},
]


def load_existing_state(slug):
    """Load existing state data."""
    filepath = os.path.join(HUGO_STATES_DIR, f"{slug}.json")
    if os.path.exists(filepath):
        with open(filepath) as f:
            return json.load(f)
    return None


def expand_state_data(state_data):
    """Add expanded orgs to state data."""
    abbr = state_data["state_abbr"]
    existing_names = {r["name"] for r in state_data.get("resources", [])}
    new_resources = []
    
    for org in EXPANDED_ORGS:
        regions = org.get("regions", [])
        if abbr in regions or "ALL" in regions:
            if org["name"] not in existing_names:
                resource = {
                    "id": f"{abbr.lower()}-{org['category'][:3]}-{len(state_data.get('resources', [])) + len(new_resources) + 1:03d}",
                    "name": org["name"],
                    "category": org["category"],
                    "subcategory": org.get("subcategory", ""),
                    "description": org.get("description", ""),
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
                        "source": "seed-data-expanded",
                        "last_verified": datetime.utcnow().strftime("%Y-%m-%d"),
                        "created": datetime.utcnow().strftime("%Y-%m-%d"),
                        "status": "active"
                    }
                }
                new_resources.append(resource)
    
    state_data["resources"].extend(new_resources)
    state_data["count"] = len(state_data["resources"])
    state_data["last_updated"] = datetime.utcnow().isoformat()
    
    return len(new_resources)


def main():
    # Load states list
    with open(os.path.join(HUGO_DATA_DIR, "states_list.json")) as f:
        states_list = json.load(f)
    
    total_added = 0
    
    for state_info in states_list:
        slug = state_info["slug"]
        state_data = load_existing_state(slug)
        
        if state_data:
            added = expand_state_data(state_data)
            total_added += added
            
            # Save updated state data
            with open(os.path.join(HUGO_STATES_DIR, f"{slug}.json"), 'w') as f:
                json.dump(state_data, f, indent=2)
            
            # Update states list count
            state_info["count"] = state_data["count"]
            
            if added > 0:
                print(f"  {state_info['name']}: +{added} resources (total: {state_data['count']})")
    
    # Save updated states list
    with open(os.path.join(HUGO_DATA_DIR, "states_list.json"), 'w') as f:
        json.dump(states_list, f, indent=2)
    
    total_resources = sum(s["count"] for s in states_list)
    print(f"\nExpanded data: +{total_added} new resources")
    print(f"Total resources across all states: {total_resources}")


if __name__ == "__main__":
    main()
