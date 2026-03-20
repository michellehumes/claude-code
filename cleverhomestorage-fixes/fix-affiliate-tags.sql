-- =============================================================================
-- CleverHomeStorage.com — Affiliate Tag Fix (Direct SQL)
-- =============================================================================
-- Use this if WP-CLI is not available. Run via MySQL CLI or phpMyAdmin.
--
-- IMPORTANT: Take a database backup BEFORE running these queries!
--   mysqldump -u [user] -p [database] wp_posts wp_postmeta wp_options > backup.sql
-- =============================================================================

-- ---- Pre-fix audit ----
SELECT 'PRE-FIX AUDIT' AS status;

SELECT 'cleverhomestorage-20 in wp_posts' AS tag,
       COUNT(*) AS affected_posts
FROM wp_posts
WHERE post_content LIKE '%tag=cleverhomestorage-20%';

SELECT 'neatnesthome-20 in wp_posts' AS tag,
       COUNT(*) AS affected_posts
FROM wp_posts
WHERE post_content LIKE '%tag=neatnesthome-20%';

SELECT 'customgiftfinder-20 in wp_posts (already correct)' AS tag,
       COUNT(*) AS posts
FROM wp_posts
WHERE post_content LIKE '%tag=customgiftfinder-20%';

-- Show which posts are affected (for reference)
SELECT ID, post_name, post_title, post_type
FROM wp_posts
WHERE post_content LIKE '%tag=cleverhomestorage-20%'
   OR post_content LIKE '%tag=neatnesthome-20%'
ORDER BY post_type, post_name;

-- ---- Fix 1: wp_posts — cleverhomestorage-20 → customgiftfinder-20 ----
UPDATE wp_posts
SET post_content = REPLACE(post_content, 'tag=cleverhomestorage-20', 'tag=customgiftfinder-20')
WHERE post_content LIKE '%tag=cleverhomestorage-20%';

-- ---- Fix 2: wp_posts — neatnesthome-20 → customgiftfinder-20 ----
UPDATE wp_posts
SET post_content = REPLACE(post_content, 'tag=neatnesthome-20', 'tag=customgiftfinder-20')
WHERE post_content LIKE '%tag=neatnesthome-20%';

-- ---- Fix 3: wp_postmeta — catch any cached/widget affiliate links ----
UPDATE wp_postmeta
SET meta_value = REPLACE(meta_value, 'tag=cleverhomestorage-20', 'tag=customgiftfinder-20')
WHERE meta_value LIKE '%tag=cleverhomestorage-20%';

UPDATE wp_postmeta
SET meta_value = REPLACE(meta_value, 'tag=neatnesthome-20', 'tag=customgiftfinder-20')
WHERE meta_value LIKE '%tag=neatnesthome-20%';

-- ---- Fix 4: wp_options — widgets, theme customizer, cached HTML ----
UPDATE wp_options
SET option_value = REPLACE(option_value, 'tag=cleverhomestorage-20', 'tag=customgiftfinder-20')
WHERE option_value LIKE '%tag=cleverhomestorage-20%';

UPDATE wp_options
SET option_value = REPLACE(option_value, 'tag=neatnesthome-20', 'tag=customgiftfinder-20')
WHERE option_value LIKE '%tag=neatnesthome-20%';

-- ---- Post-fix verification ----
SELECT 'POST-FIX VERIFICATION' AS status;

SELECT 'cleverhomestorage-20 remaining' AS tag,
       COUNT(*) AS should_be_zero
FROM wp_posts
WHERE post_content LIKE '%tag=cleverhomestorage-20%';

SELECT 'neatnesthome-20 remaining' AS tag,
       COUNT(*) AS should_be_zero
FROM wp_posts
WHERE post_content LIKE '%tag=neatnesthome-20%';

SELECT 'customgiftfinder-20 (correct)' AS tag,
       COUNT(*) AS total_posts
FROM wp_posts
WHERE post_content LIKE '%tag=customgiftfinder-20%';
