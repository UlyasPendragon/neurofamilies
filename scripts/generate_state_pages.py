#!/usr/bin/env python3
"""
Generate Hugo content pages for each state from JSON data files.
Creates markdown files with YAML frontmatter.
"""

import json
import os

DATA_STATES_DIR = "/mnt/s/hermes/projects/neurofamilies/data/states"
CONTENT_STATES_DIR = "/mnt/s/hermes/projects/neurofamilies/content/states"
DATA_DIR = "/mnt/s/hermes/projects/neurofamilies/data"

# Category definitions
CATEGORIES = {
    "aba-therapy": {"name": "ABA Therapy", "icon": "🧩"},
    "speech-therapy": {"name": "Speech Therapy", "icon": "🗣️"},
    "occupational-therapy": {"name": "Occupational Therapy", "icon": "🖐️"},
    "mental-health": {"name": "Mental Health", "icon": "💚"},
    "schools": {"name": "Schools & Education", "icon": "🏫"},
    "respite-care": {"name": "Respite Care", "icon": "🏠"},
    "support-groups": {"name": "Support Groups", "icon": "👥"},
    "funding": {"name": "Grants & Funding", "icon": "💰"},
    "government": {"name": "Government Programs", "icon": "🏛️"},
    "sensory-products": {"name": "Sensory Products", "icon": "🎯"},
    "camps": {"name": "Camps & Recreation", "icon": "⛺"},
    "legal": {"name": "Legal & Advocacy", "icon": "⚖️"},
    "adult-services": {"name": "Adult Services", "icon": "🧑"},
    "technology": {"name": "Technology & Apps", "icon": "📱"},
}


def yaml_escape(s):
    """Escape a string for YAML."""
    if not s:
        return '""'
    s = str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    return f'"{s}"'


def generate_state_page(state_data):
    """Generate a Hugo content markdown file for a state."""
    slug = state_data["slug"]
    state_name = state_data["state"]
    state_abbr = state_data["state_abbr"]
    resources = state_data.get("resources", [])
    count = len(resources)
    
    # Count resources per category
    category_counts = {}
    for resource in resources:
        cat = resource.get("category", "other")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Build lines
    lines = []
    lines.append("---")
    lines.append(f'title: "{state_name}"')
    lines.append(f'description: "Find autism, ADHD, and neurodiverse resources in {state_name}. {count} verified providers, therapists, schools, and support services."')
    lines.append("layout: state")
    lines.append(f'state_abbr: "{state_abbr}"')
    lines.append(f'state_slug: "{slug}"')
    lines.append(f"resource_count: {count}")
    lines.append("categories:")
    
    # Sort categories by count
    sorted_cats = sorted(
        [(k, v) for k, v in CATEGORIES.items() if category_counts.get(k, 0) > 0],
        key=lambda x: category_counts.get(x[0], 0),
        reverse=True
    )
    
    for cat_key, cat_info in sorted_cats:
        cat_count = category_counts.get(cat_key, 0)
        lines.append(f"  - slug: {cat_key}")
        lines.append(f"    name: \"{cat_info['name']}\"")
        lines.append(f"    icon: \"{cat_info['icon']}\"")
        lines.append(f"    count: {cat_count}")
    
    lines.append("resources:")
    
    for r in resources[:30]:
        lines.append(f"  - name: {yaml_escape(r.get('name', ''))}")
        lines.append(f"    category: {yaml_escape(r.get('category', ''))}")
        lines.append(f"    description: {yaml_escape(r.get('description', ''))}")
        
        contact = r.get('contact', {})
        if contact:
            lines.append(f"    contact:")
            if contact.get('phone'):
                lines.append(f"      phone: {yaml_escape(contact['phone'])}")
            if contact.get('website'):
                lines.append(f"      website: {yaml_escape(contact['website'])}")
        
        address = r.get('address', {})
        if address:
            lines.append(f"    address:")
            if address.get('city'):
                lines.append(f"      city: {yaml_escape(address['city'])}")
            if address.get('state'):
                lines.append(f"      state: {yaml_escape(address['state'])}")
            if address.get('zip'):
                lines.append(f"      zip: {yaml_escape(address['zip'])}")
        
        details = r.get('details', {})
        if details.get('specialties'):
            specs = ", ".join(details['specialties'])
            lines.append(f"    specialties: [{specs}]")
        
        meta = r.get('meta', {})
        if meta.get('last_verified'):
            lines.append(f"    last_verified: \"{meta['last_verified']}\"")
    
    lines.append("---")
    lines.append("")
    lines.append(f"Find autism, ADHD, sensory processing, and neurodiverse resources in {state_name}.")
    lines.append("")
    lines.append(f"## {count} Verified Resources")
    lines.append("")
    lines.append(f"Browse {count} providers, programs, and services including ABA therapy, speech therapy, schools, respite care, support groups, funding programs, and more.")
    lines.append("")
    lines.append(f"[Search all {state_name} resources →](/search/?state={state_abbr})")
    lines.append("")
    
    return "\n".join(lines)


def main():
    os.makedirs(CONTENT_STATES_DIR, exist_ok=True)
    
    with open(os.path.join(DATA_DIR, "states_list.json")) as f:
        states_list = json.load(f)
    
    generated = 0
    
    for state_info in states_list:
        slug = state_info["slug"]
        state_file = os.path.join(DATA_STATES_DIR, f"{slug}.json")
        
        if not os.path.exists(state_file):
            continue
        
        with open(state_file) as f:
            state_data = json.load(f)
        
        content = generate_state_page(state_data)
        
        output_file = os.path.join(CONTENT_STATES_DIR, f"{slug}.md")
        with open(output_file, 'w') as f:
            f.write(content)
        
        generated += 1
    
    print(f"Generated {generated} state pages")


if __name__ == "__main__":
    main()
