#!/usr/bin/env npx ts-node

/**
 * Affiliate Validation Script
 * Validates that posts meet the required monetization ratios and compliance rules
 *
 * Usage:
 *   npm run validate:affiliate          - Run all validations
 *   npm run validate:affiliate seed     - Validate seed posts (50 total, 30/20 split)
 *   npm run validate:affiliate daily    - Validate today's posts (3 total, 2/1 split)
 *
 * Exit Codes:
 *   0 - All validations passed
 *   1 - Validation failed
 */

import fs from "fs";
import path from "path";
import matter from "gray-matter";

interface PostFrontmatter {
  title: string;
  description: string;
  date: string;
  category: string;
  tags: string[];
  heroImage: string;
  monetized: boolean;
}

interface ValidationResult {
  passed: boolean;
  errors: string[];
  warnings: string[];
  stats: {
    totalPosts: number;
    monetizedPosts: number;
    nonMonetizedPosts: number;
  };
}

// Load all posts
function loadAllPosts(): { slug: string; frontmatter: PostFrontmatter; content: string }[] {
  const postsDir = path.join(process.cwd(), "content/posts");

  if (!fs.existsSync(postsDir)) {
    return [];
  }

  const files = fs.readdirSync(postsDir).filter((f) => f.endsWith(".mdx"));

  return files.map((file) => {
    const filePath = path.join(postsDir, file);
    const fileContents = fs.readFileSync(filePath, "utf8");
    const { data, content } = matter(fileContents);

    return {
      slug: file.replace(/\.mdx$/, ""),
      frontmatter: data as PostFrontmatter,
      content,
    };
  });
}

// Get posts for a specific date
function getPostsByDate(
  posts: { slug: string; frontmatter: PostFrontmatter; content: string }[],
  date: string
) {
  return posts.filter((p) => p.frontmatter.date === date);
}

// Check if content has ProductCard components
function hasProductCards(content: string): boolean {
  return /<ProductCard/i.test(content);
}

// Count ProductCard components
function countProductCards(content: string): number {
  const matches = content.match(/<ProductCard/gi);
  return matches ? matches.length : 0;
}

// Check if content has Amazon links
function hasAmazonLinks(content: string): boolean {
  return /amazon\.com/i.test(content);
}

// Validate seed posts (50 total, 30 monetized, 20 non-monetized)
function validateSeedPosts(
  posts: { slug: string; frontmatter: PostFrontmatter; content: string }[]
): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  const monetized = posts.filter((p) => p.frontmatter.monetized === true);
  const nonMonetized = posts.filter((p) => p.frontmatter.monetized === false);

  // Check total count
  if (posts.length !== 50) {
    errors.push(`Expected 50 total posts, found ${posts.length}`);
  }

  // Check monetized count
  if (monetized.length !== 30) {
    errors.push(`Expected 30 monetized posts, found ${monetized.length}`);
  }

  // Check non-monetized count
  if (nonMonetized.length !== 20) {
    errors.push(`Expected 20 non-monetized posts, found ${nonMonetized.length}`);
  }

  // Validate each monetized post
  monetized.forEach((post) => {
    const productCardCount = countProductCards(post.content);

    // Check for minimum product cards
    if (productCardCount < 3) {
      errors.push(
        `Monetized post "${post.frontmatter.title}" has ${productCardCount} ProductCards (minimum 3 required)`
      );
    }

    // Check that post doesn't claim specific prices
    if (/\$\d+\.\d{2}/.test(post.content)) {
      warnings.push(
        `Monetized post "${post.frontmatter.title}" may contain specific prices (avoid real-time price assertions)`
      );
    }
  });

  // Validate each non-monetized post
  nonMonetized.forEach((post) => {
    // Check that non-monetized posts have NO product cards
    if (hasProductCards(post.content)) {
      errors.push(
        `Non-monetized post "${post.frontmatter.title}" contains ProductCard components (not allowed)`
      );
    }

    // Check that non-monetized posts have NO Amazon links
    if (hasAmazonLinks(post.content)) {
      errors.push(
        `Non-monetized post "${post.frontmatter.title}" contains Amazon links (not allowed)`
      );
    }
  });

  return {
    passed: errors.length === 0,
    errors,
    warnings,
    stats: {
      totalPosts: posts.length,
      monetizedPosts: monetized.length,
      nonMonetizedPosts: nonMonetized.length,
    },
  };
}

// Validate daily posts (3 total, 2 monetized, 1 non-monetized)
function validateDailyPosts(
  posts: { slug: string; frontmatter: PostFrontmatter; content: string }[]
): ValidationResult {
  const today = new Date().toISOString().split("T")[0];
  const todaysPosts = getPostsByDate(posts, today);

  const errors: string[] = [];
  const warnings: string[] = [];

  const monetized = todaysPosts.filter((p) => p.frontmatter.monetized === true);
  const nonMonetized = todaysPosts.filter((p) => p.frontmatter.monetized === false);

  // Check total count for today
  if (todaysPosts.length !== 3) {
    errors.push(`Expected 3 posts for today (${today}), found ${todaysPosts.length}`);
  }

  // Check monetized count
  if (monetized.length !== 2) {
    errors.push(`Expected 2 monetized posts for today, found ${monetized.length}`);
  }

  // Check non-monetized count
  if (nonMonetized.length !== 1) {
    errors.push(`Expected 1 non-monetized post for today, found ${nonMonetized.length}`);
  }

  // Validate each monetized post
  monetized.forEach((post) => {
    const productCardCount = countProductCards(post.content);

    if (productCardCount < 3) {
      errors.push(
        `Monetized post "${post.frontmatter.title}" has ${productCardCount} ProductCards (minimum 3 required)`
      );
    }
  });

  // Validate each non-monetized post
  nonMonetized.forEach((post) => {
    if (hasProductCards(post.content)) {
      errors.push(
        `Non-monetized post "${post.frontmatter.title}" contains ProductCard components (not allowed)`
      );
    }

    if (hasAmazonLinks(post.content)) {
      errors.push(
        `Non-monetized post "${post.frontmatter.title}" contains Amazon links (not allowed)`
      );
    }
  });

  return {
    passed: errors.length === 0,
    errors,
    warnings,
    stats: {
      totalPosts: todaysPosts.length,
      monetizedPosts: monetized.length,
      nonMonetizedPosts: nonMonetized.length,
    },
  };
}

// Validate all posts for compliance
function validateAllPosts(
  posts: { slug: string; frontmatter: PostFrontmatter; content: string }[]
): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  const monetized = posts.filter((p) => p.frontmatter.monetized === true);
  const nonMonetized = posts.filter((p) => p.frontmatter.monetized === false);

  // Validate each post
  posts.forEach((post) => {
    // Check required frontmatter
    if (!post.frontmatter.title) {
      errors.push(`Post "${post.slug}" is missing title`);
    }
    if (!post.frontmatter.description) {
      errors.push(`Post "${post.slug}" is missing description`);
    }
    if (!post.frontmatter.date) {
      errors.push(`Post "${post.slug}" is missing date`);
    }
    if (!post.frontmatter.category) {
      errors.push(`Post "${post.slug}" is missing category`);
    }
    if (post.frontmatter.monetized === undefined) {
      errors.push(`Post "${post.slug}" is missing monetized flag`);
    }

    // Validate category
    const validCategories = ["makeup", "hair", "skincare", "trends"];
    if (!validCategories.includes(post.frontmatter.category)) {
      warnings.push(
        `Post "${post.slug}" has invalid category "${post.frontmatter.category}"`
      );
    }
  });

  // Validate monetized posts
  monetized.forEach((post) => {
    const productCardCount = countProductCards(post.content);

    if (productCardCount < 3) {
      errors.push(
        `Monetized post "${post.frontmatter.title}" has ${productCardCount} ProductCards (minimum 3 required)`
      );
    }

    // Check content length (should be 900-1400 words)
    const wordCount = post.content.split(/\s+/).length;
    if (wordCount < 900) {
      warnings.push(
        `Monetized post "${post.frontmatter.title}" has ${wordCount} words (recommended: 900-1400)`
      );
    }
    if (wordCount > 1400) {
      warnings.push(
        `Monetized post "${post.frontmatter.title}" has ${wordCount} words (recommended: 900-1400)`
      );
    }
  });

  // Validate non-monetized posts
  nonMonetized.forEach((post) => {
    if (hasProductCards(post.content)) {
      errors.push(
        `Non-monetized post "${post.frontmatter.title}" contains ProductCard components (not allowed)`
      );
    }

    if (hasAmazonLinks(post.content)) {
      errors.push(
        `Non-monetized post "${post.frontmatter.title}" contains Amazon links (not allowed)`
      );
    }

    // Check content length (should be 600-900 words)
    const wordCount = post.content.split(/\s+/).length;
    if (wordCount < 600) {
      warnings.push(
        `Non-monetized post "${post.frontmatter.title}" has ${wordCount} words (recommended: 600-900)`
      );
    }
    if (wordCount > 900) {
      warnings.push(
        `Non-monetized post "${post.frontmatter.title}" has ${wordCount} words (recommended: 600-900)`
      );
    }
  });

  return {
    passed: errors.length === 0,
    errors,
    warnings,
    stats: {
      totalPosts: posts.length,
      monetizedPosts: monetized.length,
      nonMonetizedPosts: nonMonetized.length,
    },
  };
}

// Print validation results
function printResults(results: ValidationResult, mode: string): void {
  console.log("\n" + "=".repeat(60));
  console.log(`AFFILIATE VALIDATION RESULTS (${mode.toUpperCase()} MODE)`);
  console.log("=".repeat(60) + "\n");

  console.log("📊 Statistics:");
  console.log(`   Total posts: ${results.stats.totalPosts}`);
  console.log(`   Monetized posts: ${results.stats.monetizedPosts}`);
  console.log(`   Non-monetized posts: ${results.stats.nonMonetizedPosts}`);
  console.log();

  if (results.errors.length > 0) {
    console.log("❌ Errors:");
    results.errors.forEach((error) => {
      console.log(`   - ${error}`);
    });
    console.log();
  }

  if (results.warnings.length > 0) {
    console.log("⚠️  Warnings:");
    results.warnings.forEach((warning) => {
      console.log(`   - ${warning}`);
    });
    console.log();
  }

  if (results.passed) {
    console.log("✅ All validations passed!\n");
  } else {
    console.log("❌ Validation failed. Please fix the errors above.\n");
  }
}

// Main execution
const args = process.argv.slice(2);
const mode = args[0] || "all";

console.log("Loading posts...");
const posts = loadAllPosts();
console.log(`Found ${posts.length} posts.\n`);

let results: ValidationResult;

switch (mode) {
  case "seed":
    results = validateSeedPosts(posts);
    break;
  case "daily":
    results = validateDailyPosts(posts);
    break;
  case "all":
  default:
    results = validateAllPosts(posts);
    break;
}

printResults(results, mode);

// Exit with appropriate code
process.exit(results.passed ? 0 : 1);
