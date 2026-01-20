#!/usr/bin/env npx ts-node

/**
 * Daily Publishing Script
 * Generates 3 new posts daily (2 monetized, 1 non-monetized) and commits them
 *
 * This script is meant to be run by GitHub Actions on a schedule.
 * It generates content, validates it, and commits to the repository.
 *
 * Environment Variables:
 *   GITHUB_TOKEN          - GitHub token for committing (provided by Actions)
 *   LLM_PROVIDER          - Optional: LLM provider for content generation
 *   LLM_API_KEY           - Optional: API key for LLM provider
 *   AMAZON_ASSOC_TAG      - Amazon Associate tag (defaults to shelzysbeauty-20)
 */

import { execSync } from "child_process";
import fs from "fs";
import path from "path";

// Configuration
const EXPECTED_MONETIZED = 2;
const EXPECTED_NON_MONETIZED = 1;

interface GenerationResult {
  success: boolean;
  postsGenerated: number;
  monetizedCount: number;
  nonMonetizedCount: number;
  errors: string[];
}

// Run a command and return output
function runCommand(command: string, options: { cwd?: string } = {}): string {
  try {
    return execSync(command, {
      encoding: "utf8",
      cwd: options.cwd || process.cwd(),
      stdio: ["pipe", "pipe", "pipe"],
    });
  } catch (error: unknown) {
    const err = error as { stderr?: string; message?: string };
    throw new Error(err.stderr || err.message || "Command failed");
  }
}

// Generate daily posts
function generateDailyPosts(): GenerationResult {
  console.log("📝 Generating daily posts...\n");

  const errors: string[] = [];

  try {
    // Run the generation script
    const output = runCommand("npm run generate:daily");
    console.log(output);

    // Parse the output to verify counts
    const monetizedMatch = output.match(/Monetized posts: (\d+)/);
    const nonMonetizedMatch = output.match(/Non-monetized posts: (\d+)/);

    const monetizedCount = monetizedMatch ? parseInt(monetizedMatch[1], 10) : 0;
    const nonMonetizedCount = nonMonetizedMatch ? parseInt(nonMonetizedMatch[1], 10) : 0;
    const totalGenerated = monetizedCount + nonMonetizedCount;

    // Validate counts
    if (monetizedCount !== EXPECTED_MONETIZED) {
      errors.push(`Expected ${EXPECTED_MONETIZED} monetized posts, got ${monetizedCount}`);
    }

    if (nonMonetizedCount !== EXPECTED_NON_MONETIZED) {
      errors.push(`Expected ${EXPECTED_NON_MONETIZED} non-monetized posts, got ${nonMonetizedCount}`);
    }

    return {
      success: errors.length === 0,
      postsGenerated: totalGenerated,
      monetizedCount,
      nonMonetizedCount,
      errors,
    };
  } catch (error: unknown) {
    const err = error as { message?: string };
    return {
      success: false,
      postsGenerated: 0,
      monetizedCount: 0,
      nonMonetizedCount: 0,
      errors: [err.message || "Unknown error during generation"],
    };
  }
}

// Validate generated posts
function validatePosts(): boolean {
  console.log("\n🔍 Validating generated posts...\n");

  try {
    const output = runCommand("npm run validate:affiliate daily");
    console.log(output);
    return true;
  } catch {
    console.error("Validation failed");
    return false;
  }
}

// Commit and push changes
function commitAndPush(): boolean {
  console.log("\n📤 Committing and pushing changes...\n");

  const today = new Date().toISOString().split("T")[0];

  try {
    // Configure git (for GitHub Actions)
    if (process.env.GITHUB_ACTIONS) {
      runCommand('git config user.name "github-actions[bot]"');
      runCommand('git config user.email "github-actions[bot]@users.noreply.github.com"');
    }

    // Stage new posts
    runCommand("git add content/posts/");
    runCommand("git add content/queues/");

    // Check if there are changes to commit
    try {
      runCommand("git diff --cached --quiet");
      console.log("No changes to commit.");
      return true;
    } catch {
      // There are changes to commit
    }

    // Commit with descriptive message
    const commitMessage = `Add daily posts for ${today} (2 monetized, 1 trend)`;
    runCommand(`git commit -m "${commitMessage}"`);

    // Push changes
    runCommand("git push");

    console.log(`✅ Successfully committed and pushed daily posts for ${today}`);
    return true;
  } catch (error: unknown) {
    const err = error as { message?: string };
    console.error("Failed to commit and push:", err.message);
    return false;
  }
}

// Main execution
async function main(): Promise<void> {
  console.log("=".repeat(60));
  console.log("DAILY PUBLISHING SCRIPT");
  console.log(`Date: ${new Date().toISOString()}`);
  console.log("=".repeat(60) + "\n");

  // Step 1: Generate posts
  const generationResult = generateDailyPosts();

  if (!generationResult.success) {
    console.error("\n❌ Generation failed:");
    generationResult.errors.forEach((err) => console.error(`   - ${err}`));
    process.exit(1);
  }

  console.log(`\n✅ Generated ${generationResult.postsGenerated} posts`);
  console.log(`   - Monetized: ${generationResult.monetizedCount}`);
  console.log(`   - Non-monetized: ${generationResult.nonMonetizedCount}`);

  // Step 2: Validate posts
  const validationPassed = validatePosts();

  if (!validationPassed) {
    console.error("\n❌ Validation failed. Aborting.");
    process.exit(1);
  }

  // Step 3: Commit and push (only in CI or if --commit flag is passed)
  const shouldCommit = process.env.GITHUB_ACTIONS || process.argv.includes("--commit");

  if (shouldCommit) {
    const pushSucceeded = commitAndPush();

    if (!pushSucceeded) {
      console.error("\n❌ Failed to commit and push changes.");
      process.exit(1);
    }
  } else {
    console.log("\n📋 Skipping commit (not in CI and --commit flag not passed)");
    console.log("   Run with --commit flag to commit changes locally");
  }

  console.log("\n" + "=".repeat(60));
  console.log("✅ DAILY PUBLISHING COMPLETE");
  console.log("=".repeat(60) + "\n");
}

main();
