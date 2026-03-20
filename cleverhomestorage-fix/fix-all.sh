#!/bin/bash
# CleverHomeStorage.com - Complete Fix Script
# Run this on the WordPress server with WP-CLI access
# Usage: bash fix-all.sh

set -e

echo "=========================================="
echo "CleverHomeStorage.com Fix Script"
echo "=========================================="

# ---- Configuration ----
# Update these if your WP-CLI path or DB prefix differs
WPCLI="wp"
SITE_URL="https://cleverhomestorage.com"

# ---- Step 0: Backup ----
echo ""
echo "[Step 0] Creating database backup..."
$WPCLI db export "backup_$(date +%Y%m%d_%H%M%S).sql"
echo "Backup created successfully."

# ---- Step 1: Fix affiliate tags ----
echo ""
echo "[Step 1] Fixing affiliate tags..."

echo "  Replacing cleverhomestorage-20 -> customgiftfinder-20..."
$WPCLI db query "UPDATE wp_posts SET post_content = REPLACE(post_content, 'tag=cleverhomestorage-20', 'tag=customgiftfinder-20') WHERE post_content LIKE '%tag=cleverhomestorage-20%';"

echo "  Replacing neatnesthome-20 -> customgiftfinder-20..."
$WPCLI db query "UPDATE wp_posts SET post_content = REPLACE(post_content, 'tag=neatnesthome-20', 'tag=customgiftfinder-20') WHERE post_content LIKE '%tag=neatnesthome-20%';"

echo "  Checking wp_postmeta..."
$WPCLI db query "UPDATE wp_postmeta SET meta_value = REPLACE(meta_value, 'tag=cleverhomestorage-20', 'tag=customgiftfinder-20') WHERE meta_value LIKE '%tag=cleverhomestorage-20%';"
$WPCLI db query "UPDATE wp_postmeta SET meta_value = REPLACE(meta_value, 'tag=neatnesthome-20', 'tag=customgiftfinder-20') WHERE meta_value LIKE '%tag=neatnesthome-20%';"

echo "  Checking wp_options..."
$WPCLI db query "UPDATE wp_options SET option_value = REPLACE(option_value, 'tag=cleverhomestorage-20', 'tag=customgiftfinder-20') WHERE option_value LIKE '%tag=cleverhomestorage-20%';"
$WPCLI db query "UPDATE wp_options SET option_value = REPLACE(option_value, 'tag=neatnesthome-20', 'tag=customgiftfinder-20') WHERE option_value LIKE '%tag=neatnesthome-20%';"

echo "  Affiliate tags fixed!"

# ---- Step 2: Fix author display name ----
echo ""
echo "[Step 2] Fixing author display name..."
$WPCLI db query "UPDATE wp_users SET display_name = 'CHS Editorial Team' WHERE user_login = 'michelle-e-humes' OR user_login = 'michelle.e.humes' OR user_email LIKE '%michelle%';"
echo "  Author display name updated!"

# ---- Step 3: Clear caches ----
echo ""
echo "[Step 3] Clearing caches..."

# LiteSpeed cache
if $WPCLI plugin is-active litespeed-cache 2>/dev/null; then
    $WPCLI litespeed-purge all
    echo "  LiteSpeed cache purged."
else
    echo "  LiteSpeed cache plugin not active, skipping."
fi

# WP object cache
$WPCLI cache flush 2>/dev/null && echo "  Object cache flushed." || echo "  No object cache to flush."

# WP transients
$WPCLI transient delete --all 2>/dev/null && echo "  Transients cleared." || true

echo ""
echo "[Step 4] Verification..."

echo ""
echo "  Wrong tags remaining in wp_posts:"
$WPCLI db query "SELECT COUNT(*) AS wrong_count FROM wp_posts WHERE post_content LIKE '%tag=cleverhomestorage-20%' OR post_content LIKE '%tag=neatnesthome-20%';"

echo "  Correct tags in wp_posts:"
$WPCLI db query "SELECT COUNT(*) AS correct_count FROM wp_posts WHERE post_content LIKE '%tag=customgiftfinder-20%';"

echo "  Author display name:"
$WPCLI db query "SELECT user_login, display_name FROM wp_users WHERE user_login LIKE '%michelle%';"

echo ""
echo "=========================================="
echo "Done! Now verify by spot-checking articles:"
echo "=========================================="

SLUGS=(
    "best-kitchen-cabinet-organizers"
    "best-pantry-pull-out-shelves"
    "best-closet-organizers-under-100"
    "best-garage-bike-storage-racks"
    "best-pantry-can-organizers"
)

for slug in "${SLUGS[@]}"; do
    wrong=$(curl -s "${SITE_URL}/${slug}/" | grep -oP 'tag=cleverhomestorage-20|tag=neatnesthome-20' | wc -l)
    correct=$(curl -s "${SITE_URL}/${slug}/" | grep -oP 'tag=customgiftfinder-20' | wc -l)
    echo "  ${slug}: wrong=${wrong} correct=${correct}"
done

# Check homepage too
wrong=$(curl -s "${SITE_URL}/" | grep -oP 'tag=cleverhomestorage-20|tag=neatnesthome-20' | wc -l)
correct=$(curl -s "${SITE_URL}/" | grep -oP 'tag=customgiftfinder-20' | wc -l)
echo "  homepage: wrong=${wrong} correct=${correct}"

echo ""
echo "=========================================="
echo "MANUAL STEPS STILL NEEDED:"
echo "=========================================="
echo "1. Fix Navigation: Go to WordPress Admin > Appearance > Menus"
echo "   Move 'Kitchen Organization' out from under 'Garage' to top-level"
echo ""
echo "2. Yoast Article Schema: Go to Yoast SEO > Search Appearance > Content Types"
echo "   Set Posts schema to 'Article' type"
echo "   For FAQ schema, install a JSON-LD plugin or add this to functions.php"
echo "=========================================="
