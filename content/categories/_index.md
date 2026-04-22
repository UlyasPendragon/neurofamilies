---
title: "Browse by Category"
description: "Find neurodiverse resources by type of service or support."
layout: page
---

## Browse Resources by Category

What kind of help are you looking for?

<div class="category-grid" role="list">
{{ range $.Site.Data.categories }}
  <a href="/categories/{{ .slug }}/" class="category-card" role="listitem">
    <span class="category-icon" aria-hidden="true">{{ .icon }}</span>
    <span class="category-name">{{ .name }}</span>
    <span class="category-count">{{ .count }}+ resources</span>
  </a>
{{ end }}
</div>

---

*Each category includes providers, programs, and services across all 50 US states and Canada.*
