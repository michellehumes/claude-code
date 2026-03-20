#!/bin/bash
# =============================================================================
# CleverHomeStorage.com — Affiliate Tag Verification Script
# =============================================================================
# Run this AFTER applying fixes to verify all tags are correct.
# Can be run from any machine with curl access to the site.
#
# Usage: bash verify-affiliate-tags.sh
# =============================================================================

set -euo pipefail

CORRECT_TAG="customgiftfinder-20"
WRONG_TAGS=("cleverhomestorage-20" "neatnesthome-20")
SITE="https://cleverhomestorage.com"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Articles that previously used neatnesthome-20
BATCH1_SLUGS=(
    "best-pantry-pull-out-shelves"
    "best-garage-bike-storage-racks"
    "best-pantry-can-organizers"
    "best-over-the-toilet-storage"
    "best-garage-storage-cabinets"
    "how-to-organize-your-pantry-step-by-step-guide"
)

# Sample of articles that previously used cleverhomestorage-20
BATCH2_SLUGS=(
    "best-kitchen-cabinet-organizers"
    "best-closet-organizers-under-100"
    "small-kitchen-organization-ideas"
    "best-garage-shelving-units"
    "best-under-sink-organizers"
    "best-shoe-storage-solutions"
    "best-closet-systems"
    "best-drawer-organizers"
    "best-spice-rack-organizers"
    "best-laundry-room-organizers"
)

TOTAL_PASS=0
TOTAL_FAIL=0
TOTAL_CHECKED=0

check_page() {
    local slug="$1"
    local url
    if [ "$slug" = "homepage" ]; then
        url="$SITE/"
    else
        url="$SITE/$slug/"
    fi

    local content
    content=$(curl -sL --max-time 15 "$url" 2>/dev/null) || {
        echo -e "  ${YELLOW}SKIP${NC} $slug — could not fetch page"
        return
    }

    local wrong_count=0
    for wtag in "${WRONG_TAGS[@]}"; do
        local wc
        wc=$(echo "$content" | grep -oP "tag=${wtag}" | wc -l)
        wrong_count=$((wrong_count + wc))
    done

    local correct_count
    correct_count=$(echo "$content" | grep -oP "tag=${CORRECT_TAG}" | wc -l)

    TOTAL_CHECKED=$((TOTAL_CHECKED + 1))

    if [ "$wrong_count" -eq 0 ] && [ "$correct_count" -gt 0 ]; then
        echo -e "  ${GREEN}PASS${NC} $slug — wrong=0, correct=$correct_count"
        TOTAL_PASS=$((TOTAL_PASS + 1))
    elif [ "$wrong_count" -eq 0 ] && [ "$correct_count" -eq 0 ]; then
        echo -e "  ${YELLOW}WARN${NC} $slug — no affiliate links found at all"
    else
        echo -e "  ${RED}FAIL${NC} $slug — wrong=$wrong_count, correct=$correct_count"
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
    fi
}

echo "============================================="
echo " Affiliate Tag Verification"
echo " Correct tag: ${CORRECT_TAG}"
echo "============================================="
echo ""

# Check homepage
echo -e "${YELLOW}--- Homepage ---${NC}"
check_page "homepage"
echo ""

# Check Batch 1 (previously neatnesthome-20)
echo -e "${YELLOW}--- Batch 1: Previously neatnesthome-20 ---${NC}"
for slug in "${BATCH1_SLUGS[@]}"; do
    check_page "$slug"
done
echo ""

# Check Batch 2 (previously cleverhomestorage-20)
echo -e "${YELLOW}--- Batch 2: Previously cleverhomestorage-20 (sample) ---${NC}"
for slug in "${BATCH2_SLUGS[@]}"; do
    check_page "$slug"
done
echo ""

# Summary
echo "============================================="
echo " Results: ${TOTAL_CHECKED} pages checked"
echo -e "   ${GREEN}PASS: ${TOTAL_PASS}${NC}"
echo -e "   ${RED}FAIL: ${TOTAL_FAIL}${NC}"
echo "============================================="

if [ "$TOTAL_FAIL" -eq 0 ]; then
    echo -e "${GREEN}All checked pages have correct affiliate tags!${NC}"
    exit 0
else
    echo -e "${RED}Some pages still have wrong tags. Investigate above failures.${NC}"
    exit 1
fi
