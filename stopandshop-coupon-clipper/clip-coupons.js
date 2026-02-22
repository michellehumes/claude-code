#!/usr/bin/env node

/**
 * Stop & Shop Bulk Coupon Clipper
 *
 * Automates clipping all available coupons on stopandshop.com.
 * Opens a browser, lets you log in, then clips every coupon.
 *
 * Usage:
 *   node clip-coupons.js
 *   HEADLESS=false node clip-coupons.js   (to see the browser)
 */

const puppeteer = require("puppeteer");
const readline = require("readline");

// ── Configuration ────────────────────────────────────────────────────
const CONFIG = {
  couponsUrl: "https://www.stopandshop.com/coupons",
  loginUrl: "https://www.stopandshop.com/login",
  headless: process.env.HEADLESS !== "false",
  clipDelay: 1000, // ms between each clip
  scrollDelay: 2000, // ms after scrolling
  maxScrollAttempts: 40,
  loginTimeout: 120000, // 2 min for manual login
  selectors: {
    clipButton: [
      'button[aria-label*="Load to card"]',
      'button[aria-label*="load to card"]',
      'button[aria-label*="Clip"]',
      'button[aria-label*="clip"]',
      'button[data-testid*="clip"]',
      'button[data-testid*="load-to-card"]',
      '.coupon-clip-button:not(.clipped)',
      '.load-to-card-button:not(.clipped)',
    ],
    loadMore: [
      'button[aria-label*="Load more"]',
      'button[aria-label*="Show more"]',
      'button[class*="load-more"]',
      'button[class*="show-more"]',
    ],
  },
};

// ── Helpers ──────────────────────────────────────────────────────────

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function prompt(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

function log(msg) {
  const ts = new Date().toLocaleTimeString();
  console.log(`[${ts}] ${msg}`);
}

// ── Main ─────────────────────────────────────────────────────────────

async function main() {
  log("Starting Stop & Shop Coupon Clipper...");

  const browser = await puppeteer.launch({
    headless: CONFIG.headless,
    defaultViewport: { width: 1280, height: 900 },
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  // Set a realistic user agent
  await page.setUserAgent(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  );

  try {
    // Step 1: Navigate to login page
    log("Navigating to Stop & Shop login page...");
    await page.goto(CONFIG.loginUrl, { waitUntil: "networkidle2", timeout: 30000 });

    if (CONFIG.headless) {
      log("Running in headless mode. Set HEADLESS=false to see the browser.");
      log("You will need to log in manually if not already authenticated.");
    }

    // Step 2: Wait for user to log in
    log("");
    log("=== MANUAL LOGIN REQUIRED ===");
    log("A browser window should be open (or will open when you set HEADLESS=false).");
    log("Please log in to your Stop & Shop account.");
    log("");
    await prompt("Press ENTER after you have logged in...");

    // Step 3: Navigate to coupons page
    log("Navigating to coupons page...");
    await page.goto(CONFIG.couponsUrl, { waitUntil: "networkidle2", timeout: 30000 });
    await sleep(3000); // Wait for dynamic content

    // Step 4: Scroll to load all coupons
    log("Loading all available coupons...");
    let scrollAttempts = 0;
    let previousHeight = 0;

    while (scrollAttempts < CONFIG.maxScrollAttempts) {
      // Try "Load More" button first
      let loadMoreClicked = false;
      for (const sel of CONFIG.selectors.loadMore) {
        const btn = await page.$(sel);
        if (btn) {
          const isVisible = await btn.isIntersectingViewport();
          if (isVisible) {
            await btn.click();
            loadMoreClicked = true;
            log(`  Clicked "Load More" (attempt ${scrollAttempts + 1})`);
            await sleep(CONFIG.scrollDelay);
            break;
          }
        }
      }

      if (!loadMoreClicked) {
        // Scroll to bottom
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        await sleep(CONFIG.scrollDelay);

        const currentHeight = await page.evaluate(() => document.body.scrollHeight);
        if (currentHeight === previousHeight) {
          log("  Reached end of coupon list.");
          break;
        }
        previousHeight = currentHeight;
      }

      scrollAttempts++;
      if (scrollAttempts % 5 === 0) {
        log(`  Scroll attempt ${scrollAttempts}/${CONFIG.maxScrollAttempts}...`);
      }
    }

    // Scroll back to top
    await page.evaluate(() => window.scrollTo(0, 0));
    await sleep(1000);

    // Step 5: Find and clip all coupons
    log("Scanning for unclipped coupons...");

    const findClipButtons = async () => {
      return await page.evaluate((selectors) => {
        const results = [];
        for (const sel of selectors) {
          try {
            const buttons = document.querySelectorAll(sel);
            buttons.forEach((btn) => {
              if (btn.disabled) return;
              const text = btn.textContent.toLowerCase();
              if (text.includes("clipped") || text.includes("added")) return;

              // Create a unique-ish identifier
              const rect = btn.getBoundingClientRect();
              results.push({
                selector: sel,
                text: btn.textContent.trim().substring(0, 50),
                x: rect.x + rect.width / 2,
                y: rect.y + rect.height / 2,
              });
            });
          } catch {
            // skip
          }
        }
        return results;
      }, CONFIG.selectors.clipButton);
    };

    let allButtons = await findClipButtons();
    log(`Found ${allButtons.length} coupons to clip.`);

    if (allButtons.length === 0) {
      log("No unclipped coupons found. They may all be clipped already!");
      await browser.close();
      return;
    }

    let clipped = 0;
    let failed = 0;

    // Process coupons in batches since the page may change as we clip
    while (true) {
      const buttons = await findClipButtons();
      if (buttons.length === 0) break;

      const btn = buttons[0];

      try {
        // Scroll to the button position
        await page.evaluate((y) => {
          window.scrollTo(0, y - 300);
        }, btn.y);
        await sleep(500);

        // Click the button
        await page.mouse.click(btn.x, btn.y);
        clipped++;
        log(`  Clipped ${clipped}/${allButtons.length}: "${btn.text}"`);
      } catch (err) {
        failed++;
        log(`  Failed to clip: "${btn.text}" - ${err.message}`);
      }

      await sleep(CONFIG.clipDelay);

      // Refresh the button list periodically
      if (clipped % 10 === 0) {
        await sleep(1000);
      }
    }

    // Summary
    log("");
    log("========== SUMMARY ==========");
    log(`  Coupons clipped: ${clipped}`);
    log(`  Failed:          ${failed}`);
    log(`  Total found:     ${allButtons.length}`);
    log("=============================");
    log("");
    log("All done! Your coupons have been loaded to your Stop & Shop card.");
  } catch (err) {
    log(`Error: ${err.message}`);
    console.error(err);
  } finally {
    await prompt("Press ENTER to close the browser...");
    await browser.close();
  }
}

main();
