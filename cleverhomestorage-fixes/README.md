# CleverHomeStorage.com — Site-Wide Fix Scripts

## Problem
~401 Amazon affiliate links use wrong tracking tags, resulting in zero revenue attribution to the correct Amazon Associates account.

| Wrong Tag | Scope | Link Count |
|-----------|-------|------------|
| `cleverhomestorage-20` | 32 articles + homepage | ~353 |
| `neatnesthome-20` | 6 articles | ~49 |

**Correct tag:** `customgiftfinder-20`

## Scripts

### 1. `fix-affiliate-tags.sh` (Primary — WP-CLI)
Automated fix using WP-CLI. Backs up the database first.

```bash
ssh user@server
cd /var/www/html   # or wherever WordPress is installed
bash /path/to/fix-affiliate-tags.sh
```

### 2. `fix-affiliate-tags.sql` (Alternative — Direct SQL)
Run via MySQL CLI or phpMyAdmin if WP-CLI is unavailable.

```bash
# Backup first!
mysqldump -u dbuser -p dbname wp_posts wp_postmeta wp_options > backup.sql

# Apply fixes
mysql -u dbuser -p dbname < fix-affiliate-tags.sql
```

### 3. `verify-affiliate-tags.sh` (Verification)
Run from any machine with curl access after applying fixes.

```bash
bash verify-affiliate-tags.sh
```

### 4. `fix-additional-issues.sh` (Nav + Author + Schema)
Fixes three additional issues:
- **Navigation:** Moves "Kitchen Organization" from under Garage to top-level
- **Author:** Changes display name to "CHS Editorial Team"
- **Schema:** Sets Yoast Article schema for posts + installs FAQ JSON-LD mu-plugin

```bash
ssh user@server
cd /var/www/html
bash /path/to/fix-additional-issues.sh
```

## Execution Order

1. Run `fix-affiliate-tags.sh` (or `.sql`)
2. Run `fix-additional-issues.sh`
3. Run `verify-affiliate-tags.sh` to confirm
4. Spot-check articles in browser
5. Test FAQ schema at https://search.google.com/test/rich-results
