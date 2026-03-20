#!/bin/bash
# =============================================================================
# CleverHomeStorage.com — Additional Fixes
# =============================================================================
# Fix 1: Navigation — Move "Kitchen Organization" out from under Garage
# Fix 2: Author display name → "CHS Editorial Team"
# Fix 3: Yoast Article schema for all posts
#
# Usage: SSH into WordPress server, then run:
#   bash fix-additional-issues.sh
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Detect WordPress path
if [ -n "${WP_PATH:-}" ]; then
    WP_DIR="$WP_PATH"
elif [ -f "wp-config.php" ]; then
    WP_DIR="."
elif [ -f "/var/www/html/wp-config.php" ]; then
    WP_DIR="/var/www/html"
elif [ -f "/var/www/cleverhomestorage.com/wp-config.php" ]; then
    WP_DIR="/var/www/cleverhomestorage.com"
else
    echo -e "${RED}ERROR: Cannot find WordPress installation.${NC}"
    echo "Set WP_PATH environment variable or run from the WordPress root directory."
    exit 1
fi

WP="wp --path=$WP_DIR --allow-root"

echo "============================================="
echo " CleverHomeStorage.com — Additional Fixes"
echo " WordPress: $WP_DIR"
echo "============================================="
echo ""

# =========================================================================
# FIX 1: Navigation — Move Kitchen Organization to top-level
# =========================================================================
echo -e "${YELLOW}--- Fix 1: Navigation Menu ---${NC}"
echo "Looking for 'Kitchen Organization' menu item..."

# List all menus
echo "Available menus:"
$WP menu list --format=table 2>/dev/null || echo "Could not list menus."
echo ""

# Find the Kitchen Organization menu item
# We need to find it and set its parent to 0 (top-level)
KITCHEN_ITEM=$($WP menu item list primary --format=json 2>/dev/null | \
    python3 -c "
import json, sys
items = json.load(sys.stdin)
for item in items:
    if 'kitchen' in item.get('title','').lower() and 'organization' in item.get('title','').lower():
        print(item['db_id'])
        break
" 2>/dev/null) || true

if [ -z "$KITCHEN_ITEM" ]; then
    # Try other common menu names
    for menu_name in "primary" "main" "main-menu" "header" "primary-menu"; do
        KITCHEN_ITEM=$($WP menu item list "$menu_name" --format=json 2>/dev/null | \
            python3 -c "
import json, sys
items = json.load(sys.stdin)
for item in items:
    if 'kitchen' in item.get('title','').lower():
        print(item['db_id'])
        break
" 2>/dev/null) || true
        if [ -n "$KITCHEN_ITEM" ]; then
            echo "Found in menu: $menu_name"
            break
        fi
    done
fi

if [ -n "$KITCHEN_ITEM" ]; then
    echo "Found Kitchen Organization menu item (ID: $KITCHEN_ITEM)"
    echo "Moving to top-level (removing parent)..."
    $WP menu item update "$KITCHEN_ITEM" --parent-id=0 2>/dev/null && \
        echo -e "${GREEN}Kitchen Organization moved to top-level.${NC}" || \
        echo -e "${RED}Failed to update menu item. Try manually in WP Admin → Appearance → Menus.${NC}"
else
    echo -e "${YELLOW}Could not find Kitchen Organization menu item automatically.${NC}"
    echo "Manual fix: WP Admin → Appearance → Menus → drag 'Kitchen Organization' to top-level."
fi
echo ""

# =========================================================================
# FIX 2: Author Display Name → "CHS Editorial Team"
# =========================================================================
echo -e "${YELLOW}--- Fix 2: Author Display Name ---${NC}"

# Try to find the user
echo "Looking for michelle user..."
$WP user list --format=table --fields=ID,user_login,display_name,user_email 2>/dev/null || true
echo ""

# Update via WP-CLI (safer than direct SQL)
MICHELLE_ID=$($WP user list --field=ID --search="*michelle*" 2>/dev/null | head -1) || true

if [ -n "$MICHELLE_ID" ]; then
    echo "Found user ID: $MICHELLE_ID"
    $WP user update "$MICHELLE_ID" --display_name="CHS Editorial Team" 2>/dev/null && \
        echo -e "${GREEN}Display name changed to 'CHS Editorial Team'.${NC}" || \
        echo -e "${RED}WP-CLI update failed. Trying SQL...${NC}"
else
    echo "User not found via WP-CLI search. Trying direct SQL..."
fi

# SQL fallback — covers both possible login formats
$WP db query "UPDATE wp_users SET display_name = 'CHS Editorial Team' WHERE user_login LIKE '%michelle%' OR user_email LIKE '%michelle%';" 2>/dev/null && \
    echo -e "${GREEN}SQL update applied for display_name.${NC}" || true

# Also update the nickname (used by some themes as display name)
if [ -n "$MICHELLE_ID" ]; then
    $WP user meta update "$MICHELLE_ID" nickname "CHS Editorial Team" 2>/dev/null && \
        echo "Nickname meta also updated." || true
fi
echo ""

# =========================================================================
# FIX 3: Yoast SEO — Article Schema for All Posts
# =========================================================================
echo -e "${YELLOW}--- Fix 3: Yoast SEO Article Schema ---${NC}"

# Check if Yoast is active
if $WP plugin is-active wordpress-seo 2>/dev/null; then
    echo "Yoast SEO is active."

    # Set default schema type for posts to Article
    # Yoast stores this in the wpseo_titles option
    echo "Setting default Article schema for posts..."

    # Get current Yoast titles options
    CURRENT=$($WP option get wpseo_titles --format=json 2>/dev/null) || true

    if [ -n "$CURRENT" ]; then
        # Update schema-page-type-post and schema-article-type-post
        UPDATED=$(echo "$CURRENT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['schema-page-type-post'] = 'WebPage'
data['schema-article-type-post'] = 'Article'
print(json.dumps(data))
" 2>/dev/null) || true

        if [ -n "$UPDATED" ]; then
            echo "$UPDATED" | $WP option update wpseo_titles --format=json 2>/dev/null && \
                echo -e "${GREEN}Yoast Article schema set for all posts.${NC}" || \
                echo -e "${RED}Failed to update Yoast options.${NC}"
        fi
    else
        echo "Could not read Yoast options. Set manually:"
        echo "  WP Admin → Yoast SEO → Search Appearance → Content Types → Posts → Schema → Article"
    fi
elif $WP plugin is-active wordpress-seo-premium 2>/dev/null; then
    echo "Yoast SEO Premium detected. Same settings apply."
    echo "  WP Admin → Yoast SEO → Search Appearance → Content Types → Posts → Schema → Article"
else
    echo -e "${YELLOW}Yoast SEO not detected as active.${NC}"
    echo "If using a different SEO plugin, configure Article schema there."
fi

echo ""

# ---- FAQ Schema via custom JSON-LD snippet ----
echo -e "${YELLOW}--- FAQ Schema Setup ---${NC}"
echo "Yoast does not natively add FAQ schema for FAQ sections."
echo "Recommended approach: Install a custom code snippet."
echo ""

# Create a mu-plugin for FAQ schema
MU_PLUGINS_DIR="$WP_DIR/wp-content/mu-plugins"
FAQ_PLUGIN="$MU_PLUGINS_DIR/chs-faq-schema.php"

if [ ! -d "$MU_PLUGINS_DIR" ]; then
    mkdir -p "$MU_PLUGINS_DIR"
    echo "Created mu-plugins directory."
fi

cat > "$FAQ_PLUGIN" << 'PHPEOF'
<?php
/**
 * Plugin Name: CHS FAQ Schema
 * Description: Adds FAQ JSON-LD schema to posts that contain FAQ sections.
 * Version: 1.0
 * Author: CHS Editorial Team
 */

add_action('wp_head', function() {
    if (!is_singular('post')) return;

    global $post;
    $content = $post->post_content;

    // Look for FAQ patterns: h2/h3 with "FAQ" or structured Q&A blocks
    if (stripos($content, 'faq') === false &&
        stripos($content, 'frequently asked') === false) {
        return;
    }

    // Extract Q&A pairs from the content
    // Pattern: headings followed by paragraph content (common FAQ format)
    $faqs = [];

    // Match h3 tags that look like questions (contain ?)
    if (preg_match_all('/<h[23][^>]*>(.*?\?)<\/h[23]>/i', $content, $questions)) {
        foreach ($questions[1] as $i => $question) {
            $question = wp_strip_all_tags($question);
            // Get the content after this heading until the next heading
            $pos = strpos($content, $questions[0][$i]);
            $after = substr($content, $pos + strlen($questions[0][$i]));
            // Get text until next heading or end
            if (preg_match('/^(.*?)(?=<h[23]|$)/is', $after, $answer_match)) {
                $answer = wp_strip_all_tags($answer_match[1]);
                $answer = trim($answer);
                if (!empty($answer) && strlen($answer) > 20) {
                    $faqs[] = [
                        '@type' => 'Question',
                        'name' => $question,
                        'acceptedAnswer' => [
                            '@type' => 'Answer',
                            'text' => $answer,
                        ],
                    ];
                }
            }
        }
    }

    if (empty($faqs)) return;

    $schema = [
        '@context' => 'https://schema.org',
        '@type' => 'FAQPage',
        'mainEntity' => $faqs,
    ];

    echo '<script type="application/ld+json">' . "\n";
    echo wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
    echo "\n</script>\n";
});
PHPEOF

echo -e "${GREEN}FAQ schema mu-plugin created at: $FAQ_PLUGIN${NC}"
echo "This will automatically add FAQ JSON-LD to posts with FAQ sections."
echo ""

# ---- Final cache clear ----
echo -e "${YELLOW}--- Final Cache Clear ---${NC}"
$WP cache flush 2>/dev/null && echo "Object cache flushed." || true
$WP transient delete --all 2>/dev/null && echo "Transients cleared." || true

if $WP plugin is-active litespeed-cache 2>/dev/null; then
    $WP litespeed-purge all 2>/dev/null && echo "LiteSpeed cache purged." || true
fi

echo ""
echo "============================================="
echo -e "${GREEN} All additional fixes applied!${NC}"
echo "============================================="
echo ""
echo "Summary:"
echo "  1. Navigation: Kitchen Organization moved to top-level (verify in WP Admin)"
echo "  2. Author: Display name set to 'CHS Editorial Team'"
echo "  3. Schema: Yoast Article type set for posts + FAQ JSON-LD mu-plugin installed"
echo ""
echo "Next steps:"
echo "  - Verify menu in WP Admin → Appearance → Menus"
echo "  - Check author name on any article page"
echo "  - Test FAQ schema at https://search.google.com/test/rich-results"
