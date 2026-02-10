#!/usr/bin/env python3
"""Upgrade the beauty blog: homepage improvements + batch post updates."""

import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# PART 1: Upgrade index.html
# ============================================================
idx_path = os.path.join(BASE, 'index.html')
with open(idx_path, 'r') as f:
    html = f.read()

# 1a. Add Open Graph meta tags after existing meta tags
og_tags = '''  <meta property="og:title" content="Shelzy's Beauty Blog | Honest Reviews & Beauty Finds">
  <meta property="og:description" content="Expert-tested skincare, makeup, and haircare recommendations for every skin type and budget.">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Shelzy's Beauty Blog">
  <link rel="canonical" href="https://shelzysbeauty.com/">'''

html = html.replace(
    '  <title>Shelzy\'s Beauty Blog | Honest Reviews &amp; Beauty Finds</title>',
    '  <title>Shelzy\'s Beauty Blog | Honest Reviews &amp; Beauty Finds</title>\n' + og_tags
)

# 1b. Add search bar after the category bar
search_html = '''
  <!-- Search -->
  <div class="container">
    <div class="search-bar">
      <input type="text" placeholder="Search posts... (e.g. vitamin C, retinol, budget)" aria-label="Search posts">
    </div>
  </div>
'''
html = html.replace('  <main class="container">', search_html + '\n  <main class="container">')

# 1c. Add data-category attributes to each post card
# Map: post href substring -> category
category_map = {
    'skincare/': 'skincare',
    'haircare/': 'haircare',
    'makeup/': 'makeup',
    'tools-devices/': 'tools-devices',
    'routines-guides/': 'routines-guides',
    'budget-beauty/': 'budget-beauty',
    'comparisons/': 'comparisons',
    'seasonal/': 'seasonal',
}

def add_data_category(m):
    card_html = m.group(0)
    for substr, cat in category_map.items():
        if substr in card_html:
            return card_html.replace('<article class="post-card">',
                                     f'<article class="post-card" data-category="{cat}">')
    return card_html

# Match each post-card article block
html = re.sub(
    r'<article class="post-card">.*?</article>',
    add_data_category,
    html,
    flags=re.DOTALL
)

# 1d. Add load-more button + post count after the posts-grid div
html = html.replace(
    '      </div>\n    </section>\n\n    <!-- Newsletter Signup -->',
    '''      </div>

      <div class="load-more-wrap">
        <button class="load-more-btn">Show More</button>
        <span class="posts-count"></span>
      </div>
      <div class="search-no-results">No posts found. Try a different search term.</div>
    </section>

    <!-- Newsletter Signup -->''')

# 1e. Add scroll-to-top button before closing body
html = html.replace(
    '  <script src="js/main.js"></script>\n</body>',
    '  <button class="scroll-to-top" aria-label="Scroll to top">&#8593;</button>\n  <script src="js/main.js"></script>\n</body>'
)

with open(idx_path, 'w') as f:
    f.write(html)

print("OK: index.html upgraded")

# ============================================================
# PART 2: Batch-update all blog posts
# ============================================================

# Map of all posts by category for related-post linking
posts_dir = os.path.join(BASE, 'posts')
all_posts = {}  # {category: [(filename, title), ...]}

for cat_dir in os.listdir(posts_dir):
    cat_path = os.path.join(posts_dir, cat_dir)
    if not os.path.isdir(cat_path):
        continue
    all_posts[cat_dir] = []
    for fname in sorted(os.listdir(cat_path)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(cat_path, fname)
        with open(fpath, 'r') as f:
            content = f.read()
        # Extract title
        m = re.search(r'<h1>(.*?)</h1>', content)
        title = m.group(1) if m else fname.replace('.html', '').replace('-', ' ').title()
        all_posts[cat_dir].append((fname, title))

# Category display names
cat_names = {
    'skincare': 'Skincare',
    'haircare': 'Haircare',
    'makeup': 'Makeup',
    'tools-devices': 'Tools & Devices',
    'routines-guides': 'Routines & Guides',
    'budget-beauty': 'Budget Beauty',
    'comparisons': 'Comparisons',
    'seasonal': 'Seasonal & Gifts',
}

def get_related_posts(category, current_file, count=3):
    """Get related posts from same category, excluding current."""
    candidates = [(f, t) for f, t in all_posts.get(category, []) if f != current_file]
    # Also pull from related categories
    related_cats = {
        'skincare': ['routines-guides', 'budget-beauty'],
        'haircare': ['tools-devices', 'comparisons'],
        'makeup': ['budget-beauty', 'tools-devices'],
        'tools-devices': ['skincare', 'haircare'],
        'routines-guides': ['skincare', 'budget-beauty'],
        'budget-beauty': ['skincare', 'comparisons'],
        'comparisons': ['skincare', 'haircare'],
        'seasonal': ['budget-beauty', 'skincare'],
    }
    if len(candidates) < count:
        for rc in related_cats.get(category, []):
            for f, t in all_posts.get(rc, []):
                candidates.append((f, t))
                if len(candidates) >= count + 2:
                    break

    return candidates[:count]


def build_related_html(category, current_file):
    related = get_related_posts(category, current_file)
    if not related:
        return ''

    items = ''
    for fname, title in related:
        # Determine which category folder this file is in
        for cat, posts in all_posts.items():
            for pf, pt in posts:
                if pf == fname and pt == title:
                    cat_display = cat_names.get(cat, cat.replace('-', ' ').title())
                    if cat == category:
                        href = fname
                    else:
                        href = f'../{cat}/{fname}'
                    items += f'''      <div class="related-post-card">
        <span class="post-card-category">{cat_display}</span>
        <a href="{href}">{title}</a>
      </div>
'''
                    break
            else:
                continue
            break

    return f'''    <div class="related-posts">
      <h2>You Might Also Like</h2>
      <div class="related-posts-grid">
{items}      </div>
    </div>
'''


def upgrade_post(fpath, category, filename):
    with open(fpath, 'r') as f:
        html = f.read()

    # Skip if already upgraded
    if 'reading-progress' in html:
        return False

    # 1. Add reading progress bar right after <body>
    html = html.replace('<body>', '<body>\n  <div class="reading-progress"></div>')

    # 2. Add breadcrumbs before post-header
    cat_display = cat_names.get(category, category.replace('-', ' ').title())
    breadcrumb = f'''  <nav class="breadcrumbs">
    <a href="../../index.html">Home</a>
    <span>&rsaquo;</span>
    <a href="../../index.html#{category}">{cat_display}</a>
    <span>&rsaquo;</span>
    <span>Current Post</span>
  </nav>'''
    html = html.replace('  <div class="post-header">', breadcrumb + '\n  <div class="post-header">')

    # 3. Add Table of Contents container after affiliate-disclosure
    toc_html = '''    <div class="toc">
      <div class="toc-title">Table of Contents</div>
      <ul class="toc-list"></ul>
    </div>
'''
    # Insert after the affiliate disclosure div
    html = html.replace('</div>\n\n    <p>', '</div>\n\n' + toc_html + '    <p>', 1)

    # 4. Add share bar before the newsletter box
    share_html = '''    <div class="share-bar">
      <span class="share-bar-label">Share</span>
      <a class="share-btn" data-share="pinterest" title="Share on Pinterest">Pin</a>
      <a class="share-btn" data-share="facebook" title="Share on Facebook">FB</a>
      <a class="share-btn" data-share="twitter" title="Share on Twitter">X</a>
      <a class="share-btn" data-share="copy" title="Copy link">Link</a>
    </div>
'''
    html = html.replace('    <div class="newsletter-box">', share_html + '    <div class="newsletter-box">')

    # 5. Add related posts before closing post-content div
    related_html = build_related_html(category, filename)
    if related_html:
        # Insert before the newsletter box (which is already in post-content)
        html = html.replace(share_html, related_html + share_html)

    # 6. Add floating CTA bar - find the first amazon link in the post
    first_amazon = re.search(r'href="(https://www\.amazon\.com/dp/[^"]+)"', html)
    if first_amazon:
        amazon_url = first_amazon.group(1)
        floating_html = f'''  <div class="floating-cta">
    <span class="floating-cta-text">Found something you love?</span>
    <a href="{amazon_url}" target="_blank" rel="nofollow noopener" class="cta-button">Shop Top Pick on Amazon</a>
  </div>'''
        html = html.replace('  <script src="../../js/main.js"></script>',
                           floating_html + '\n  <button class="scroll-to-top" aria-label="Scroll to top">&#8593;</button>\n  <script src="../../js/main.js"></script>')
    else:
        html = html.replace('  <script src="../../js/main.js"></script>',
                           '  <button class="scroll-to-top" aria-label="Scroll to top">&#8593;</button>\n  <script src="../../js/main.js"></script>')

    # 7. Add OG meta tags
    m_title = re.search(r'<title>(.*?)</title>', html)
    m_desc = re.search(r'<meta name="description" content="(.*?)"', html)
    if m_title:
        title_text = m_title.group(1)
        desc_text = m_desc.group(1) if m_desc else ''
        og = f'  <meta property="og:title" content="{title_text}">\n'
        og += f'  <meta property="og:description" content="{desc_text}">\n'
        og += '  <meta property="og:type" content="article">\n'
        og += '  <meta property="og:site_name" content="Shelzy\'s Beauty Blog">'
        html = html.replace('  <link rel="preconnect"', og + '\n  <link rel="preconnect"', 1)

    with open(fpath, 'w') as f:
        f.write(html)
    return True


# Process all posts
count = 0
for cat_dir in sorted(os.listdir(posts_dir)):
    cat_path = os.path.join(posts_dir, cat_dir)
    if not os.path.isdir(cat_path):
        continue
    for fname in sorted(os.listdir(cat_path)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(cat_path, fname)
        if upgrade_post(fpath, cat_dir, fname):
            count += 1
            print(f"  OK: posts/{cat_dir}/{fname}")

print(f"\nUpgraded {count} posts total.")

# Also upgrade about.html and disclosure.html with scroll-to-top
for page in ['about.html', 'disclosure.html']:
    ppath = os.path.join(BASE, page)
    if not os.path.exists(ppath):
        continue
    with open(ppath, 'r') as f:
        h = f.read()
    if 'scroll-to-top' not in h:
        h = h.replace('<script src="js/main.js"></script>',
                      '<button class="scroll-to-top" aria-label="Scroll to top">&#8593;</button>\n<script src="js/main.js"></script>')
        with open(ppath, 'w') as f:
            f.write(h)
        print(f"  OK: {page}")

print("\nDone! All upgrades complete.")
