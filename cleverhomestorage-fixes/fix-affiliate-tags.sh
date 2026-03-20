#!/bin/bash
# =============================================================================
# CleverHomeStorage.com — Affiliate Tag Fix Script
# =============================================================================
# Replaces ALL incorrect Amazon affiliate tags with the correct one:
#   - cleverhomestorage-20 → customgiftfinder-20  (~353 links across 32 articles + homepage)
#   - neatnesthome-20      → customgiftfinder-20  (~49 links across 6 articles)
#
# Usage: SSH into the WordPress server, then run:
#   bash fix-affiliate-tags.sh
#
# Requirements: WP-CLI installed and accessible
# =============================================================================

set -euo pipefail

CORRECT_TAG="customgiftfinder-20"
WRONG_TAG_1="cleverhomestorage-20"
WRONG_TAG_2="neatnesthome-20"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "============================================="
echo " CleverHomeStorage.com Affiliate Tag Fix"
echo "============================================="
echo ""

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
    echo "  Example: WP_PATH=/var/www/html bash fix-affiliate-tags.sh"
    exit 1
fi

echo "WordPress directory: $WP_DIR"
echo ""

# Check WP-CLI availability
if ! command -v wp &> /dev/null; then
    echo -e "${RED}ERROR: WP-CLI (wp) not found. Install it or use the SQL script instead.${NC}"
    exit 1
fi

WP="wp --path=$WP_DIR --allow-root"

# ---- Pre-fix count ----
echo -e "${YELLOW}--- Pre-Fix Counts ---${NC}"

COUNT_WRONG1=$($WP db query "SELECT COUNT(*) as cnt FROM wp_posts WHERE post_content LIKE '%tag=${WRONG_TAG_1}%';" --skip-column-names 2>/dev/null | tr -d '[:space:]')
COUNT_WRONG2=$($WP db query "SELECT COUNT(*) as cnt FROM wp_posts WHERE post_content LIKE '%tag=${WRONG_TAG_2}%';" --skip-column-names 2>/dev/null | tr -d '[:space:]')
COUNT_CORRECT=$($WP db query "SELECT COUNT(*) as cnt FROM wp_posts WHERE post_content LIKE '%tag=${CORRECT_TAG}%';" --skip-column-names 2>/dev/null | tr -d '[:space:]')

echo "Posts with tag=${WRONG_TAG_1}: ${COUNT_WRONG1}"
echo "Posts with tag=${WRONG_TAG_2}: ${COUNT_WRONG2}"
echo "Posts with tag=${CORRECT_TAG}: ${COUNT_CORRECT}"
echo ""

# ---- Backup ----
echo -e "${YELLOW}--- Creating Backup ---${NC}"
BACKUP_FILE="wp_posts_backup_$(date +%Y%m%d_%H%M%S).sql"
$WP db export "$BACKUP_FILE" --tables=wp_posts,wp_postmeta,wp_options 2>/dev/null
echo "Backup saved to: $BACKUP_FILE"
echo ""

# ---- Fix 1: Replace cleverhomestorage-20 in wp_posts ----
echo -e "${YELLOW}--- Replacing tag=${WRONG_TAG_1} → tag=${CORRECT_TAG} in wp_posts ---${NC}"
$WP db query "UPDATE wp_posts SET post_content = REPLACE(post_content, 'tag=${WRONG_TAG_1}', 'tag=${CORRECT_TAG}') WHERE post_content LIKE '%tag=${WRONG_TAG_1}%';"
echo -e "${GREEN}Done.${NC}"

# ---- Fix 2: Replace neatnesthome-20 in wp_posts ----
echo -e "${YELLOW}--- Replacing tag=${WRONG_TAG_2} → tag=${CORRECT_TAG} in wp_posts ---${NC}"
$WP db query "UPDATE wp_posts SET post_content = REPLACE(post_content, 'tag=${WRONG_TAG_2}', 'tag=${CORRECT_TAG}') WHERE post_content LIKE '%tag=${WRONG_TAG_2}%';"
echo -e "${GREEN}Done.${NC}"

# ---- Fix 3: Check and fix wp_postmeta ----
echo -e "${YELLOW}--- Checking wp_postmeta for wrong tags ---${NC}"
META_WRONG1=$($WP db query "SELECT COUNT(*) FROM wp_postmeta WHERE meta_value LIKE '%tag=${WRONG_TAG_1}%';" --skip-column-names 2>/dev/null | tr -d '[:space:]')
META_WRONG2=$($WP db query "SELECT COUNT(*) FROM wp_postmeta WHERE meta_value LIKE '%tag=${WRONG_TAG_2}%';" --skip-column-names 2>/dev/null | tr -d '[:space:]')

if [ "$META_WRONG1" -gt 0 ] 2>/dev/null; then
    echo "Found ${META_WRONG1} postmeta entries with ${WRONG_TAG_1}, fixing..."
    $WP db query "UPDATE wp_postmeta SET meta_value = REPLACE(meta_value, 'tag=${WRONG_TAG_1}', 'tag=${CORRECT_TAG}') WHERE meta_value LIKE '%tag=${WRONG_TAG_1}%';"
    echo -e "${GREEN}Fixed.${NC}"
else
    echo "No postmeta entries with ${WRONG_TAG_1}."
fi

if [ "$META_WRONG2" -gt 0 ] 2>/dev/null; then
    echo "Found ${META_WRONG2} postmeta entries with ${WRONG_TAG_2}, fixing..."
    $WP db query "UPDATE wp_postmeta SET meta_value = REPLACE(meta_value, 'tag=${WRONG_TAG_2}', 'tag=${CORRECT_TAG}') WHERE meta_value LIKE '%tag=${WRONG_TAG_2}%';"
    echo -e "${GREEN}Fixed.${NC}"
else
    echo "No postmeta entries with ${WRONG_TAG_2}."
fi

# ---- Fix 4: Check and fix wp_options (widgets, cached content) ----
echo -e "${YELLOW}--- Checking wp_options for wrong tags ---${NC}"
OPT_WRONG1=$($WP db query "SELECT COUNT(*) FROM wp_options WHERE option_value LIKE '%tag=${WRONG_TAG_1}%';" --skip-column-names 2>/dev/null | tr -d '[:space:]')
OPT_WRONG2=$($WP db query "SELECT COUNT(*) FROM wp_options WHERE option_value LIKE '%tag=${WRONG_TAG_2}%';" --skip-column-names 2>/dev/null | tr -d '[:space:]')

if [ "$OPT_WRONG1" -gt 0 ] 2>/dev/null; then
    echo "Found ${OPT_WRONG1} options with ${WRONG_TAG_1}, fixing..."
    $WP db query "UPDATE wp_options SET option_value = REPLACE(option_value, 'tag=${WRONG_TAG_1}', 'tag=${CORRECT_TAG}') WHERE option_value LIKE '%tag=${WRONG_TAG_1}%';"
    echo -e "${GREEN}Fixed.${NC}"
else
    echo "No options with ${WRONG_TAG_1}."
fi

if [ "$OPT_WRONG2" -gt 0 ] 2>/dev/null; then
    echo "Found ${OPT_WRONG2} options with ${WRONG_TAG_2}, fixing..."
    $WP db query "UPDATE wp_options SET option_value = REPLACE(option_value, 'tag=${WRONG_TAG_2}', 'tag=${CORRECT_TAG}') WHERE option_value LIKE '%tag=${WRONG_TAG_2}%';"
    echo -e "${GREEN}Fixed.${NC}"
else
    echo "No options with ${WRONG_TAG_2}."
fi

# ---- Post-fix count ----
echo ""
echo -e "${YELLOW}--- Post-Fix Counts ---${NC}"
POST_WRONG1=$($WP db query "SELECT COUNT(*) FROM wp_posts WHERE post_content LIKE '%tag=${WRONG_TAG_1}%';" --skip-column-names 2>/dev/null | tr -d '[:space:]')
POST_WRONG2=$($WP db query "SELECT COUNT(*) FROM wp_posts WHERE post_content LIKE '%tag=${WRONG_TAG_2}%';" --skip-column-names 2>/dev/null | tr -d '[:space:]')
POST_CORRECT=$($WP db query "SELECT COUNT(*) FROM wp_posts WHERE post_content LIKE '%tag=${CORRECT_TAG}%';" --skip-column-names 2>/dev/null | tr -d '[:space:]')

echo "Posts with tag=${WRONG_TAG_1}: ${POST_WRONG1} (should be 0)"
echo "Posts with tag=${WRONG_TAG_2}: ${POST_WRONG2} (should be 0)"
echo "Posts with tag=${CORRECT_TAG}: ${POST_CORRECT}"
echo ""

if [ "$POST_WRONG1" -eq 0 ] && [ "$POST_WRONG2" -eq 0 ]; then
    echo -e "${GREEN}SUCCESS: All affiliate tags have been corrected!${NC}"
else
    echo -e "${RED}WARNING: Some wrong tags remain. Check manually.${NC}"
fi

# ---- Clear caches ----
echo ""
echo -e "${YELLOW}--- Clearing Caches ---${NC}"

# LiteSpeed Cache
if $WP plugin is-active litespeed-cache 2>/dev/null; then
    echo "Purging LiteSpeed Cache..."
    $WP litespeed-purge all 2>/dev/null || echo "LiteSpeed purge command not available, try manually."
    echo -e "${GREEN}LiteSpeed cache purged.${NC}"
else
    echo "LiteSpeed Cache plugin not active. Trying alternative cache plugins..."
fi

# WP Super Cache
if $WP plugin is-active wp-super-cache 2>/dev/null; then
    $WP super-cache flush 2>/dev/null || true
    echo "WP Super Cache flushed."
fi

# W3 Total Cache
if $WP plugin is-active w3-total-cache 2>/dev/null; then
    $WP w3-total-cache flush all 2>/dev/null || true
    echo "W3 Total Cache flushed."
fi

# WordPress object cache
$WP cache flush 2>/dev/null && echo "WordPress object cache flushed." || true

# WordPress transients
$WP transient delete --all 2>/dev/null && echo "Transients cleared." || true

echo ""
echo "============================================="
echo -e "${GREEN} Affiliate tag fix complete!${NC}"
echo " Backup file: $BACKUP_FILE"
echo "============================================="
