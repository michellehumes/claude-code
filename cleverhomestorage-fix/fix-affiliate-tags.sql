-- CleverHomeStorage.com Affiliate Tag Fix
-- Run this against the WordPress database
-- BACKUP YOUR DATABASE FIRST: mysqldump -u [user] -p [database] > backup_$(date +%Y%m%d).sql

-- ============================================================
-- FIX 1: Replace wrong affiliate tags in post content
-- ============================================================

-- Replace cleverhomestorage-20 → customgiftfinder-20 (~353 links)
UPDATE wp_posts
SET post_content = REPLACE(post_content, 'tag=cleverhomestorage-20', 'tag=customgiftfinder-20')
WHERE post_content LIKE '%tag=cleverhomestorage-20%';

-- Replace neatnesthome-20 → customgiftfinder-20 (~49 links)
UPDATE wp_posts
SET post_content = REPLACE(post_content, 'tag=neatnesthome-20', 'tag=customgiftfinder-20')
WHERE post_content LIKE '%tag=neatnesthome-20%';

-- ============================================================
-- FIX 1b: Check and fix postmeta and options tables
-- ============================================================

UPDATE wp_postmeta
SET meta_value = REPLACE(meta_value, 'tag=cleverhomestorage-20', 'tag=customgiftfinder-20')
WHERE meta_value LIKE '%tag=cleverhomestorage-20%';

UPDATE wp_postmeta
SET meta_value = REPLACE(meta_value, 'tag=neatnesthome-20', 'tag=customgiftfinder-20')
WHERE meta_value LIKE '%tag=neatnesthome-20%';

UPDATE wp_options
SET option_value = REPLACE(option_value, 'tag=cleverhomestorage-20', 'tag=customgiftfinder-20')
WHERE option_value LIKE '%tag=cleverhomestorage-20%';

UPDATE wp_options
SET option_value = REPLACE(option_value, 'tag=neatnesthome-20', 'tag=customgiftfinder-20')
WHERE option_value LIKE '%tag=neatnesthome-20%';

-- ============================================================
-- FIX 2: Author Display Name
-- ============================================================

UPDATE wp_users
SET display_name = 'CHS Editorial Team'
WHERE user_login = 'michelle-e-humes'
   OR user_login = 'michelle.e.humes'
   OR user_email LIKE '%michelle%';

-- ============================================================
-- VERIFICATION: Check for any remaining wrong tags
-- ============================================================

SELECT 'wp_posts - cleverhomestorage-20 remaining' AS check_name,
       COUNT(*) AS count
FROM wp_posts
WHERE post_content LIKE '%tag=cleverhomestorage-20%';

SELECT 'wp_posts - neatnesthome-20 remaining' AS check_name,
       COUNT(*) AS count
FROM wp_posts
WHERE post_content LIKE '%tag=neatnesthome-20%';

SELECT 'wp_posts - customgiftfinder-20 total' AS check_name,
       COUNT(*) AS count
FROM wp_posts
WHERE post_content LIKE '%tag=customgiftfinder-20%';

SELECT 'wp_postmeta - wrong tags remaining' AS check_name,
       COUNT(*) AS count
FROM wp_postmeta
WHERE meta_value LIKE '%tag=cleverhomestorage-20%'
   OR meta_value LIKE '%tag=neatnesthome-20%';

SELECT 'wp_options - wrong tags remaining' AS check_name,
       COUNT(*) AS count
FROM wp_options
WHERE option_value LIKE '%tag=cleverhomestorage-20%'
   OR option_value LIKE '%tag=neatnesthome-20%';

SELECT 'Author display name' AS check_name, display_name
FROM wp_users
WHERE user_login LIKE '%michelle%';
