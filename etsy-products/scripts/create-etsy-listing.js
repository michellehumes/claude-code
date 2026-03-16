/**
 * Shelzy's Designs — Etsy Draft Listing Creator
 * Playwright CLI script (NOT Playwright MCP)
 *
 * Usage:
 *   cd /Users/michellehumes/etsy-products/scripts
 *   npm install
 *   npx playwright install chromium
 *   node create-etsy-listing.js
 *
 * First run: log into Etsy when the browser opens, then re-run.
 * The session is saved in .playwright-profile/ — you only log in once.
 *
 * Run a single product:
 *   node create-etsy-listing.js --product easter-basket-budget-planner
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ── Config ───────────────────────────────────────────────────────────────────
const PRODUCTS_DIR = '/Users/michellehumes/etsy-products';
const LOGS_DIR = path.join(PRODUCTS_DIR, 'logs');
// Dedicated Playwright profile — avoids conflict with running Chrome
const CHROME_PROFILE = path.join(__dirname, '.playwright-profile');
const DEFAULT_PRICE = '4.99';
const ETSY_CREATE_URL = 'https://www.etsy.com/your/listings/create';

// ── Logger ───────────────────────────────────────────────────────────────────
function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
  try {
    if (!fs.existsSync(LOGS_DIR)) fs.mkdirSync(LOGS_DIR, { recursive: true });
    fs.appendFileSync(path.join(LOGS_DIR, 'listing-creator.log'), line + '\n');
  } catch (_) {}
}

// ── Product Scanner ──────────────────────────────────────────────────────────
function getReadyProducts() {
  const skip = new Set(['logs', 'scripts']);
  const dirs = fs.readdirSync(PRODUCTS_DIR).filter(d => {
    if (skip.has(d)) return false;
    if (d.startsWith('.')) return false;  // skip hidden dirs like .playwright-profile
    return fs.statSync(path.join(PRODUCTS_DIR, d)).isDirectory();
  });

  const ready = [];
  const skipped = [];

  for (const slug of dirs) {
    const base = path.join(PRODUCTS_DIR, slug);
    const imgDir = path.join(base, 'images');
    const tplDir = path.join(base, 'templates');
    const listDir = path.join(base, 'listing');

    const images = fs.existsSync(imgDir)
      ? fs.readdirSync(imgDir).filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f)).sort()
      : [];
    const templates = fs.existsSync(tplDir)
      ? fs.readdirSync(tplDir).filter(f => /\.xlsx$/i.test(f))
      : [];

    const hasTitle = fs.existsSync(path.join(listDir, 'title.txt'));
    const hasDesc  = fs.existsSync(path.join(listDir, 'description.txt'));
    const hasTags  = fs.existsSync(path.join(listDir, 'tags.txt'));

    const reasons = [];
    if (images.length === 0)   reasons.push('no images');
    if (templates.length === 0) reasons.push('no template');
    if (!hasTitle) reasons.push('no title.txt');
    if (!hasDesc)  reasons.push('no description.txt');
    if (!hasTags)  reasons.push('no tags.txt');

    if (reasons.length > 0) {
      skipped.push({ slug, reasons });
      continue;
    }

    ready.push({
      slug,
      title:        fs.readFileSync(path.join(listDir, 'title.txt'), 'utf8').trim(),
      description:  fs.readFileSync(path.join(listDir, 'description.txt'), 'utf8').trim(),
      tags:         fs.readFileSync(path.join(listDir, 'tags.txt'), 'utf8')
                      .split('\n').map(t => t.trim()).filter(Boolean),
      images:       images.map(f => path.join(imgDir, f)),
      templatePath: path.join(tplDir, templates[0]),
      price:        DEFAULT_PRICE,
    });
  }

  return { ready, skipped };
}

// ── Progress Tracker ─────────────────────────────────────────────────────────
const PROGRESS_FILE = path.join(PRODUCTS_DIR, 'progress.json');

function loadProgress() {
  try { return JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8')); }
  catch (_) { return { completed: [], failed: {} }; }
}

function markCompleted(slug, listingUrl) {
  const p = loadProgress();
  if (!p.completed) p.completed = [];
  p.completed.push({ slug, listingUrl, completedAt: new Date().toISOString() });
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(p, null, 2));
}

function markFailed(slug, error) {
  const p = loadProgress();
  // Guard: failed must be a plain object, not an array or other type
  if (!p.failed || Array.isArray(p.failed)) p.failed = {};
  p.failed[slug] = { error: String(error), failedAt: new Date().toISOString() };
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(p, null, 2));
}

// ── Helpers ──────────────────────────────────────────────────────────────────
async function humanDelay(ms = 800) {
  await new Promise(r => setTimeout(r, ms + Math.random() * 400));
}

// ── Core: Upload Images ──────────────────────────────────────────────────────
async function uploadImages(page, imagePaths) {
  log(`  Uploading ${imagePaths.length} images (image-1 = primary thumbnail)...`);
  await page.waitForSelector('input[type="file"]', { timeout: 20000 });

  for (let i = 0; i < imagePaths.length; i++) {
    const imgPath = imagePaths[i];
    log(`    image ${i + 1}: ${path.basename(imgPath)}`);

    const [fileChooser] = await Promise.all([
      page.waitForEvent('filechooser', { timeout: 10000 }).catch(() => null),
      page.evaluate(() => {
        const inputs = document.querySelectorAll('input[type="file"][accept*="image"]');
        if (inputs.length) inputs[0].click();
      }),
    ]);

    if (fileChooser) {
      await fileChooser.setFiles(imgPath);
    } else {
      const input = await page.$('input[type="file"][accept*="image"]');
      if (input) await input.setInputFiles(imgPath);
    }

    await humanDelay(1500);
    await page.waitForTimeout(2000);
  }
  log('  Images uploaded.');
}

// ── Core: Set Digital Listing Type ───────────────────────────────────────────
async function setDigitalType(page) {
  log('  Setting listing type to Digital...');
  const selectors = [
    'input[value="download"]',
    'input[value="digital"]',
    'label:has-text("Digital")',
    '[data-testid="listing-type-digital"]',
  ];
  for (const sel of selectors) {
    const el = await page.$(sel);
    if (el) { await el.click(); await humanDelay(); return; }
  }
  await page.locator('text=Digital').first().click().catch(() => {});
  await humanDelay();
}

// ── Core: Fill Title ─────────────────────────────────────────────────────────
async function fillTitle(page, title) {
  log(`  Title: ${title.substring(0, 60)}...`);
  const selectors = [
    '#listing-edit-form-title',
    'input[name="title"]',
    'input[placeholder*="title" i]',
    '[data-testid="listing-title"]',
    'input[id*="title"]',
  ];
  for (const sel of selectors) {
    const el = await page.$(sel);
    if (el) {
      await el.click();
      await el.fill('');
      await el.type(title, { delay: 20 });
      await humanDelay();
      return;
    }
  }
  throw new Error('Could not find title input field');
}

// ── Core: Fill Description ───────────────────────────────────────────────────
async function fillDescription(page, description) {
  log('  Filling description...');
  const selectors = [
    '#listing-edit-form-description',
    'textarea[name="description"]',
    '[data-testid="listing-description"]',
    'div[contenteditable="true"]',
    'textarea[id*="description"]',
  ];
  for (const sel of selectors) {
    const el = await page.$(sel);
    if (el) {
      await el.click();
      await el.fill('');
      await el.type(description, { delay: 5 });
      await humanDelay();
      return;
    }
  }
  throw new Error('Could not find description field');
}

// ── Core: Fill Tags ──────────────────────────────────────────────────────────
async function fillTags(page, tags) {
  log(`  Adding ${Math.min(tags.length, 13)} tags...`);
  const tagSelectors = [
    'input[placeholder*="tag" i]',
    '[data-testid="listing-tags"] input',
    'input[name*="tag" i]',
    '#listing-edit-form-tags input',
  ];

  for (const tag of tags.slice(0, 13)) {
    let tagInput = null;
    for (const sel of tagSelectors) {
      tagInput = await page.$(sel);
      if (tagInput) break;
    }
    if (!tagInput) {
      log('  Warning: tag input not found, skipping remaining tags');
      break;
    }
    await tagInput.click();
    await tagInput.type(tag, { delay: 30 });
    await page.keyboard.press('Enter');
    await humanDelay(600);
  }
}

// ── Core: Set Price ──────────────────────────────────────────────────────────
async function setPrice(page, price) {
  log(`  Price: $${price}`);
  const selectors = [
    'input[name="price"]',
    '[data-testid="listing-price"] input',
    'input[id*="price"]',
    'input[placeholder*="price" i]',
  ];
  for (const sel of selectors) {
    const el = await page.$(sel);
    if (el) {
      await el.click();
      await el.fill('');
      await el.type(price, { delay: 30 });
      await humanDelay();
      return;
    }
  }
  log('  Warning: price field not found');
}

// ── Core: Upload Digital File (Excel template) ───────────────────────────────
async function uploadDigitalFile(page, templatePath) {
  log(`  Uploading template: ${path.basename(templatePath)}...`);
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await humanDelay(1000);

  const selectors = [
    'input[type="file"][accept*=".xlsx"]',
    'input[type="file"]:not([accept*="image"])',
    '[data-testid="digital-file-upload"] input[type="file"]',
  ];

  for (const sel of selectors) {
    const el = await page.$(sel);
    if (el) {
      await el.setInputFiles(templatePath);
      await humanDelay(3000);
      log('  Template uploaded.');
      return;
    }
  }

  const [fileChooser] = await Promise.all([
    page.waitForEvent('filechooser', { timeout: 8000 }).catch(() => null),
    page.locator('text=Upload a file').first().click().catch(() => {}),
  ]);
  if (fileChooser) {
    await fileChooser.setFiles(templatePath);
    await humanDelay(3000);
    log('  Template uploaded via chooser.');
  } else {
    log('  Warning: could not upload template — upload manually if needed');
  }
}

// ── Core: Save as Draft ──────────────────────────────────────────────────────
async function saveAsDraft(page) {
  log('  Saving as draft...');
  const selectors = [
    'button:has-text("Save as draft")',
    'button:has-text("Save draft")',
    '[data-testid="save-draft-button"]',
  ];
  for (const sel of selectors) {
    const el = await page.$(sel);
    if (el) {
      await el.click();
      await page.waitForTimeout(3000);
      log('  Draft saved.');
      return;
    }
  }
  await page.locator('text=/save.*draft/i').first().click().catch(() => {});
  await page.waitForTimeout(3000);
}

// ── Main: Create One Listing ─────────────────────────────────────────────────
async function createListing(page, product) {
  log(`\nCreating listing: ${product.slug}`);
  await page.goto(ETSY_CREATE_URL, { waitUntil: 'networkidle', timeout: 30000 });
  await humanDelay(2000);

  if (page.url().includes('/signin') || page.url().includes('/login')) {
    const err = new Error('NOT_LOGGED_IN');
    err.fatal = true;
    throw err;
  }

  await setDigitalType(page);
  await uploadImages(page, product.images);
  await fillTitle(page, product.title);
  await fillDescription(page, product.description);
  await fillTags(page, product.tags);
  await setPrice(page, product.price);
  await uploadDigitalFile(page, product.templatePath);
  await saveAsDraft(page);

  const url = page.url();
  log(`  Done! URL: ${url}`);
  return url;
}

// ── Entry Point ──────────────────────────────────────────────────────────────
async function main() {
  const args = process.argv.slice(2);
  const productFlagIdx = args.indexOf('--product');
  const singleProduct = productFlagIdx !== -1 ? args[productFlagIdx + 1] : null;

  const { ready, skipped } = getReadyProducts();

  if (skipped.length > 0) {
    log('\n── Skipped (missing assets) ──');
    for (const { slug, reasons } of skipped) {
      log(`  SKIP ${slug}: ${reasons.join(', ')}`);
    }
  }

  const products = singleProduct
    ? ready.filter(p => p.slug === singleProduct)
    : ready;

  if (products.length === 0) {
    log('\nNo ready products. Exiting.');
    if (singleProduct) log(`  "${singleProduct}" not found or not ready.`);
    process.exit(0);
  }

  log(`\n── Creating ${products.length} listing(s) ──`);
  for (const p of products) log(`  • ${p.slug} (${p.images.length} images)`);

  const progress = loadProgress();
  const completedSlugs = new Set((progress.completed || []).map(c => c.slug));

  log('\nLaunching browser (dedicated profile — won\'t conflict with Chrome)...');
  const browser = await chromium.launchPersistentContext(CHROME_PROFILE, {
    channel: 'chrome',  // Use real Chrome — bypasses bot detection
    headless: false,
    args: ['--no-first-run', '--no-default-browser-check'],
    viewport: { width: 1280, height: 900 },
  });

  const page = await browser.newPage();
  const results = { success: [], failed: [] };

  for (const product of products) {
    if (completedSlugs.has(product.slug)) {
      log(`SKIP ${product.slug} — already completed`);
      continue;
    }

    try {
      const listingUrl = await createListing(page, product);
      markCompleted(product.slug, listingUrl);
      results.success.push(product.slug);
      await humanDelay(3000);
    } catch (err) {
      if (err.fatal) {
        log('\nNot logged into Etsy. Log in in the browser window, then re-run the script.');
        await browser.close().catch(() => {});
        process.exit(1);
      }
      log(`ERROR on ${product.slug}: ${err.message}`);
      markFailed(product.slug, err.message);
      results.failed.push({ slug: product.slug, error: err.message });
      try {
        const screenshotPath = path.join(LOGS_DIR, `error-${product.slug}-${Date.now()}.png`);
        await page.screenshot({ path: screenshotPath });
        log(`  Screenshot: ${screenshotPath}`);
      } catch (_) {}
    }
  }

  await browser.close();

  log('\n── Run Complete ──');
  log(`Success: ${results.success.length} | Failed: ${results.failed.length}`);
  if (results.success.length) log(`  Created: ${results.success.join(', ')}`);
  if (results.failed.length) {
    for (const f of results.failed) log(`  FAILED ${f.slug}: ${f.error}`);
  }
}

main().catch(err => {
  log(`FATAL: ${err.message}`);
  process.exit(1);
});
