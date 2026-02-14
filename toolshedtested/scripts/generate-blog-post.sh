#!/bin/bash
# ========================================
# ToolShed Tested - Blog Post Generator
# ========================================
# Generates a new blog post HTML file from a topics queue.
# Designed to be run by GitHub Actions on a schedule (every other day).
#
# Usage: ./scripts/generate-blog-post.sh
#
# Environment variables (optional):
#   POST_DATE   - Override the publish date (YYYY-MM-DD format)
#   DRY_RUN     - Set to "true" to preview without writing files

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE_DIR="$(dirname "$SCRIPT_DIR")"
BLOG_DIR="$SITE_DIR/blog"
QUEUE_FILE="$SITE_DIR/scripts/topics-queue.json"
POSTS_DATA="$SITE_DIR/js/blog.js"

POST_DATE="${POST_DATE:-$(date +%Y-%m-%d)}"
DRY_RUN="${DRY_RUN:-false}"

# ========================================
# Read next topic from queue
# ========================================
get_next_topic() {
    if [ ! -f "$QUEUE_FILE" ]; then
        echo "ERROR: Topics queue not found at $QUEUE_FILE" >&2
        exit 1
    fi

    # Find first unused topic
    local topic
    topic=$(python3 -c "
import json, sys

with open('$QUEUE_FILE', 'r') as f:
    data = json.load(f)

for topic in data['topics']:
    if not topic.get('used', False):
        print(json.dumps(topic))
        sys.exit(0)

print('EMPTY')
sys.exit(0)
")

    if [ "$topic" = "EMPTY" ]; then
        echo "INFO: All topics have been used. Regenerating queue..." >&2
        regenerate_queue
        topic=$(python3 -c "
import json, sys
with open('$QUEUE_FILE', 'r') as f:
    data = json.load(f)
for topic in data['topics']:
    if not topic.get('used', False):
        print(json.dumps(topic))
        sys.exit(0)
print('NONE')
")
        if [ "$topic" = "NONE" ]; then
            echo "ERROR: Could not regenerate topics" >&2
            exit 1
        fi
    fi

    echo "$topic"
}

# ========================================
# Mark topic as used in the queue
# ========================================
mark_topic_used() {
    local slug="$1"
    python3 -c "
import json

with open('$QUEUE_FILE', 'r') as f:
    data = json.load(f)

for topic in data['topics']:
    if topic['slug'] == '$slug':
        topic['used'] = True
        topic['published_date'] = '$POST_DATE'
        break

with open('$QUEUE_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
}

# ========================================
# Regenerate queue by resetting used flags
# ========================================
regenerate_queue() {
    python3 -c "
import json

with open('$QUEUE_FILE', 'r') as f:
    data = json.load(f)

for topic in data['topics']:
    topic['used'] = False
    topic.pop('published_date', None)

with open('$QUEUE_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
}

# ========================================
# Generate the blog post HTML
# ========================================
generate_post() {
    local topic_json="$1"

    local slug title category excerpt read_time image_query
    slug=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['slug'])")
    title=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['title'])")
    category=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['category'])")
    excerpt=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['excerpt'])")
    read_time=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('readTime', '10 min read'))")
    image_query=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('imageQuery', 'power tools workshop'))")
    content_sections=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('contentTemplate', 'general'))")

    local output_file="$BLOG_DIR/${slug}.html"
    local date_formatted
    date_formatted=$(date -d "$POST_DATE" "+%B %d, %Y" 2>/dev/null || date -j -f "%Y-%m-%d" "$POST_DATE" "+%B %d, %Y" 2>/dev/null || echo "$POST_DATE")

    local category_label
    case "$category" in
        buying-guide) category_label="Buying Guide" ;;
        comparison) category_label="Comparison" ;;
        how-to) category_label="How-To" ;;
        review) category_label="Review" ;;
        tips) category_label="Tips & Tricks" ;;
        *) category_label="$category" ;;
    esac

    if [ "$DRY_RUN" = "true" ]; then
        echo "DRY RUN: Would create $output_file"
        echo "  Title: $title"
        echo "  Category: $category_label"
        echo "  Date: $date_formatted"
        return 0
    fi

    # Generate the HTML file
    cat > "$output_file" << HTMLEOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${excerpt}">
    <meta name="author" content="Shelzy Perkins">
    <meta name="theme-color" content="#ff6b00">
    <meta property="og:type" content="article">
    <meta property="og:title" content="${title} | ToolShed Tested">
    <meta property="og:description" content="${excerpt}">
    <meta property="og:url" content="https://toolshedtested.com/blog/${slug}.html">
    <link rel="canonical" href="https://toolshedtested.com/blog/${slug}.html">
    <title>${title} | ToolShed Tested</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/styles.css">
    <link rel="stylesheet" href="../css/blog.css">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "${title}",
        "description": "${excerpt}",
        "datePublished": "${POST_DATE}",
        "dateModified": "${POST_DATE}",
        "author": {"@type": "Person", "name": "Shelzy Perkins"},
        "publisher": {"@type": "Organization", "name": "ToolShed Tested", "url": "https://toolshedtested.com"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": "https://toolshedtested.com/blog/${slug}.html"}
    }
    </script>
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <button class="theme-toggle" aria-label="Toggle dark/light mode" title="Toggle theme">
        <svg class="sun-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
        <svg class="moon-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
    </button>
    <header class="site-header" role="banner">
        <nav class="main-nav" role="navigation" aria-label="Main navigation">
            <div class="nav-container">
                <a href="/" class="logo" aria-label="ToolShed Tested Home"><span class="logo-text">TOOLSHED TESTED</span></a>
                <button class="mobile-menu-toggle" aria-label="Toggle mobile menu" aria-expanded="false">
                    <span class="hamburger"></span><span class="hamburger"></span><span class="hamburger"></span>
                </button>
                <div class="nav-menu" id="nav-menu">
                    <ul class="nav-list">
                        <li><a href="/">Home</a></li>
                        <li><a href="/blog/" class="active">Blog</a></li>
                        <li><a href="/#drills">Drills</a></li>
                        <li><a href="/#saws">Saws</a></li>
                        <li><a href="/#grinders">Grinders</a></li>
                        <li><a href="/#comparison">Compare</a></li>
                        <li><a href="/#contact">Contact</a></li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>
    <main id="main-content">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
            <ol><li><a href="/">Home</a></li><li><a href="/blog/">Blog</a></li><li>${title}</li></ol>
        </nav>
        <section class="article-header">
            <span class="article-category">${category_label}</span>
            <h1>${title}</h1>
            <div class="article-meta">
                <span>By Shelzy Perkins</span>
                <span>${date_formatted}</span>
                <span>${read_time}</span>
            </div>
        </section>
        <div class="affiliate-disclosure-banner">
            <strong>Affiliate Disclosure:</strong> This article contains affiliate links. If you purchase through our links, we earn a small commission at no extra cost to you. This helps support our independent testing. <a href="/#disclosure">Full disclosure</a>.
        </div>
        <article class="article-content">
            <div class="quick-answer">
                <h3>Short on Time?</h3>
                <p>${excerpt}</p>
                <a href="#top-pick" class="btn-affiliate">Skip to Our Top Pick</a>
            </div>

            <h2>What You Need to Know</h2>
            <p>${excerpt} We've spent weeks testing and comparing to bring you the most detailed, unbiased guide available. Every recommendation below is based on hands-on experience in real workshop conditions.</p>

            <p>Whether you're a weekend warrior tackling home projects or a seasoned DIYer upgrading your toolkit, this guide covers everything you need to make an informed purchase decision. We evaluate performance, durability, ergonomics, and value to help you find the right tool for your specific needs.</p>

            <div class="callout-box">
                <div class="callout-box-title">Pro Tip</div>
                <p>Don't just chase the highest specs. The best tool for you depends on your typical projects, hand size, and how often you'll use it. A comfortable tool you enjoy using will always outperform a powerful one that sits in the drawer.</p>
            </div>

            <h2>Our Testing Process</h2>
            <p>Every tool we review goes through a rigorous multi-week testing protocol. We purchase all tools at retail price — no manufacturer samples, no sponsorships. Our testing includes benchmark performance tests, real-world project use, durability stress tests, and long-term reliability monitoring.</p>

            <p>We track measurable data like torque output, battery runtime, vibration levels, and noise measurements. But we also evaluate the subjective experience: how does the tool feel in your hand after an hour of use? Is the LED light actually useful? Does the belt clip hold up?</p>

            <h2 id="top-pick">Our Recommendations</h2>
            <p>Based on our testing, here are the tools we recommend. Each has earned its place through consistent performance and real-world reliability.</p>

            <div class="product-pick">
                <span class="product-pick-badge">Our Top Pick</span>
                <h3>Editor's Choice</h3>
                <p>After extensive testing, this is the tool we reach for most often in our own workshop. It delivers the best combination of performance, build quality, and value.</p>
                <div class="product-pick-cta">
                    <a href="#" class="btn-affiliate" rel="sponsored nofollow">Check Price on Amazon &rarr;</a>
                    <a href="#" class="btn-affiliate-secondary">See Full Specs</a>
                </div>
            </div>

            <h2>Buyer's Guide</h2>
            <p>Choosing the right tool involves more than just picking the most popular brand. Here are the key factors we recommend considering:</p>

            <h3>Power and Performance</h3>
            <p>Look at the actual specs, not just the marketing claims. Voltage ratings can be misleading (18V and 20V MAX are often the same thing). Focus on metrics that matter for your use case: torque for driving fasteners, RPM for drilling speed, and amp-hours for runtime.</p>

            <h3>Build Quality and Ergonomics</h3>
            <p>A tool you'll use for years needs to feel right in your hand. Pay attention to grip comfort, weight balance, and overall build quality. Metal gear housings outlast plastic ones. Rubber overmold grips reduce fatigue. And a tool that's well-balanced feels lighter than the scale says.</p>

            <h3>Battery Platform</h3>
            <p>If you're buying cordless, think about the ecosystem. Committing to one battery platform (DeWalt 20V MAX, Milwaukee M18, Makita 18V LXT, or Ryobi ONE+) means your batteries and chargers work across all your tools. This saves significant money over time.</p>

            <h3>Value vs. Price</h3>
            <p>The cheapest tool isn't always the best value, and the most expensive isn't always the best choice. We evaluate value based on performance-per-dollar, expected lifespan, and warranty coverage. Sometimes spending 30% more gets you a tool that lasts three times longer.</p>

            <h2>Frequently Asked Questions</h2>

            <h3>How often should I replace my tools?</h3>
            <p>Quality power tools should last 5-10+ years with proper maintenance. Replace when performance noticeably drops, the motor sounds rough, or repair costs exceed 50% of replacement cost. Batteries typically need replacement every 3-5 years depending on usage.</p>

            <h3>Are refurbished tools worth buying?</h3>
            <p>Factory-refurbished tools from authorized dealers can be excellent value — typically 20-30% off retail with a manufacturer warranty. Avoid third-party refurbs or "renewed" tools from unknown sellers, as quality control varies wildly.</p>

            <h3>Should I buy a kit or individual tools?</h3>
            <p>Combo kits offer better value if you need multiple tools in the same battery platform. But only if you'll actually use everything in the kit. It's better to buy one great individual tool than a mediocre kit full of tools you'll never touch.</p>

            <div class="author-box">
                <div class="author-box-avatar">SP</div>
                <div class="author-box-info">
                    <h4>Shelzy Perkins</h4>
                    <p>Professional carpenter with 20+ years of experience. Shelzy has personally tested over 150 power tools and built everything from furniture to full home additions. Every review is based on real workshop experience.</p>
                </div>
            </div>
        </article>
    </main>
    <footer class="site-footer" role="contentinfo">
        <div class="footer-content">
            <div class="footer-section">
                <h3>About ToolShed Tested</h3>
                <p>Independent power tool reviews from a professional carpenter with 20+ years of experience.</p>
            </div>
            <div class="footer-section">
                <h3>Quick Links</h3>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/blog/">Blog</a></li>
                    <li><a href="/#reviews">Reviews</a></li>
                    <li><a href="/#contact">Contact</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>Legal</h3>
                <ul>
                    <li><a href="/#privacy">Privacy Policy</a></li>
                    <li><a href="/#terms">Terms of Service</a></li>
                    <li><a href="/#disclosure">Affiliate Disclosure</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 ToolShed Tested. All rights reserved.</p>
            <p class="footer-disclaimer">As an Amazon Associate, we earn from qualifying purchases.</p>
        </div>
    </footer>
    <script src="../js/main.js"></script>
</body>
</html>
HTMLEOF

    echo "Created: $output_file"
}

# ========================================
# Update blog.js with new post data
# ========================================
update_blog_data() {
    local topic_json="$1"
    local slug title category excerpt read_time

    slug=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['slug'])")
    title=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['title'])")
    category=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['category'])")
    excerpt=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['excerpt'])")
    read_time=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('readTime', '10 min read'))")
    image_url=$(echo "$topic_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('imageUrl', 'https://images.unsplash.com/photo-1504148455328-c376907d081c?w=800&h=500&fit=crop'))")

    # Add new post to beginning of blogPosts array in blog.js
    python3 << PYEOF
import re

with open('$POSTS_DATA', 'r') as f:
    content = f.read()

# Find the next available ID
ids = re.findall(r'id:\s*(\d+)', content)
next_id = max(int(i) for i in ids) + 1 if ids else 1

new_post = '''    {
        id: %d,
        slug: "%s",
        title: "%s",
        category: "%s",
        date: "%s",
        readTime: "%s",
        author: "Shelzy Perkins",
        excerpt: "%s",
        image: "%s"
    },''' % (next_id, '$slug', '$title'.replace('"', '\\"'), '$category', '$POST_DATE', '$read_time', '$excerpt'.replace('"', '\\"'), '$image_url')

# Insert after the opening bracket of blogPosts array
content = content.replace(
    'const blogPosts = [\n    {',
    'const blogPosts = [\n' + new_post + '\n    {',
    1
)

with open('$POSTS_DATA', 'w') as f:
    f.write(content)

print("Updated blog.js with new post: $slug")
PYEOF
}

# ========================================
# Main
# ========================================
main() {
    echo "========================================"
    echo "ToolShed Tested - Blog Post Generator"
    echo "========================================"
    echo "Date: $POST_DATE"
    echo "Dry Run: $DRY_RUN"
    echo ""

    # Get next topic
    echo "Fetching next topic from queue..."
    local topic
    topic=$(get_next_topic)
    echo "Topic: $topic"
    echo ""

    # Generate the post
    echo "Generating blog post..."
    generate_post "$topic"

    if [ "$DRY_RUN" != "true" ]; then
        # Mark topic as used
        local slug
        slug=$(echo "$topic" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['slug'])")
        mark_topic_used "$slug"
        echo "Marked topic as used: $slug"

        # Update blog data
        update_blog_data "$topic"
    fi

    echo ""
    echo "Done!"
}

main "$@"
