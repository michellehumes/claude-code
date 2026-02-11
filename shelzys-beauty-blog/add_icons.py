#!/usr/bin/env python3
"""Add emoji icons to all post card images in index.html."""
import re

# Map each post's href to its emoji icon
post_icons = {
    # Post 1-9: Skincare
    'best-moisturizers-dry-sensitive-skin.html': '🧴',
    'best-retinol-products-beginners.html': '✨',
    'best-sunscreens-no-white-cast.html': '☀️',
    'best-pimple-patches.html': '🩹',
    'best-niacinamide-serums.html': '💧',
    'best-k-beauty-products-glass-skin.html': '🪞',
    'best-hyaluronic-acid-serums.html': '💦',
    'best-peptide-moisturizers.html': '🧬',
    'cosrx-snail-mucin-30-day-review.html': '🐌',
    'amazon-beauty-repurchase-favorites.html': '❤️',
    'best-body-lotions.html': '🧴',
    'best-eye-creams.html': '👁️',
    'best-chemical-exfoliants-aha-bha.html': '⚗️',
    'best-self-tanners.html': '🌞',
    'best-vitamin-c-serums.html': '🍊',

    # Haircare
    'best-bond-repair-treatments.html': '💪',
    'best-rosemary-oils-hair-growth.html': '🌿',
    'best-shampoos-color-treated-hair.html': '🎨',
    'best-heatless-curlers.html': '🌀',
    'best-scalp-treatments-thinning-hair.html': '💆',

    # Makeup
    'best-drugstore-foundations.html': '🎨',
    'best-long-lasting-lipsticks.html': '💋',
    'best-concealers-dark-circles.html': '✨',
    'best-clean-beauty-makeup.html': '🌱',
    'best-waterproof-mascaras.html': '💧',
    'best-setting-sprays.html': '💫',
    'best-lip-oils.html': '👄',

    # Tools & Devices
    'best-led-face-masks.html': '💡',
    'best-facial-tools.html': '🪨',
    'best-hair-dryer-brushes.html': '💨',
    'best-makeup-brush-sets.html': '🖌️',

    # Comparisons
    'cerave-vs-la-roche-posay.html': '⚖️',
    'olaplex-vs-k18.html': '🔬',
    'ordinary-vs-paulas-choice-niacinamide.html': '💎',
    'dyson-airwrap-vs-shark-flexstyle.html': '🌪️',
    'drunk-elephant-vs-the-ordinary.html': '🐘',
    'olaplex-vs-redken-vs-k18.html': '🧪',

    # Budget Beauty
    'amazon-skincare-under-20.html': '💰',
    'charlotte-tilbury-dupes.html': '👑',
    'drunk-elephant-dupes.html': '🐘',
    'amazon-mascara-rivals-lancome.html': '👁️',
    'replaced-routine-amazon-under-15.html': '💵',
    'viral-tiktok-beauty-products-tested.html': '📱',

    # Routines & Guides
    'morning-skincare-routine.html': '🌅',
    'anti-aging-routine-amazon.html': '⏳',
    'korean-skincare-routine-beginners.html': '🇰🇷',
    'nighttime-routine-acne-prone.html': '🌙',
    'curly-hair-routine-beginners.html': '🌀',
    'minimalist-skincare-routine.html': '✂️',
    'skin-cycling-routine.html': '🔄',
    'retinol-complete-guide.html': '📖',
    'build-skincare-routine-beginners.html': '📋',
    'read-skincare-ingredient-labels.html': '🏷️',
    'choose-foundation-shade-online.html': '🎯',
    'best-skincare-routine-over-40.html': '🌟',

    # Seasonal / Gift Guides
    'holiday-beauty-gift-guide.html': '🎁',
    'beauty-gifts-under-25.html': '🎀',
    'mothers-day-beauty-gifts.html': '💐',
    'summer-skincare-swap.html': '☀️',
    'winter-skincare-rescue.html': '❄️',
    'amazon-prime-day-beauty-deals.html': '🏷️',
}

with open('index.html', 'r') as f:
    html = f.read()

# Add data-icon to featured post image
html = html.replace(
    '<div class="featured-post-image" role="img" aria-label="Vitamin C serums lined up for testing"></div>',
    '<div class="featured-post-image" data-icon="🍊" role="img" aria-label="Vitamin C serums lined up for testing"></div>'
)

# Add data-icon to each post card image div
for filename, icon in post_icons.items():
    # Match the post-card-image div that comes before a link containing this filename
    pattern = r'(<div class="post-card-image" role="img" aria-label="[^"]*"></div>\s*<div class="post-card-body">\s*<span class="post-card-category">[^<]*</span>\s*<h3 class="post-card-title"><a href="[^"]*' + re.escape(filename) + r'")'
    match = re.search(pattern, html)
    if match:
        # Find the post-card-image div for this specific post
        # Look backwards from the match to find the div
        pass

# Alternative simpler approach: process each post-card block
lines = html.split('\n')
output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Check if this is a post-card-image div
    if 'class="post-card-image"' in line and 'role="img"' in line and 'data-icon' not in line:
        # Look ahead to find the href in this post card
        lookahead = '\n'.join(lines[i:i+8])
        href_match = re.search(r'href="[^"]*?/([^/"]+\.html)"', lookahead)
        if href_match:
            fname = href_match.group(1)
            icon = post_icons.get(fname, '')
            if icon:
                line = line.replace('class="post-card-image"', f'class="post-card-image" data-icon="{icon}"')
    output_lines.append(line)
    i += 1

html = '\n'.join(output_lines)

with open('index.html', 'w') as f:
    f.write(html)

print("Done! Added emoji icons to all post cards.")
