// ==UserScript==
// @name         Stop & Shop - Clip All Coupons
// @namespace    https://stopandshop.com
// @version      1.0.0
// @description  Adds a "Clip All Coupons" button to automatically load and clip every available coupon on Stop & Shop
// @match        https://stopandshop.com/coupons*
// @match        https://www.stopandshop.com/coupons*
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function () {
  "use strict";

  // ── Configuration ──────────────────────────────────────────────────
  const CONFIG = {
    // Delay between each coupon clip (ms) to avoid rate-limiting
    clipDelay: 800,
    // Delay after scrolling to load more coupons (ms)
    scrollDelay: 1500,
    // Max scroll attempts to load all coupons before giving up
    maxScrollAttempts: 30,
    // Selectors – update these if Stop & Shop changes their DOM
    selectors: {
      // The clickable button on each unclipped coupon
      clipButton: [
        'button[aria-label*="Load to card"]',
        'button[aria-label*="load to card"]',
        'button[aria-label*="Clip"]',
        'button[aria-label*="clip"]',
        'button[data-testid*="clip"]',
        'button[data-testid*="load-to-card"]',
        '.coupon-clip-button:not(.clipped)',
        '.load-to-card-button:not(.clipped)',
        'button.clip-btn:not(.clipped)',
        'button:not([disabled])[class*="clip" i]',
        'button:not([disabled])[class*="load-to-card" i]',
      ],
      // Indicator that a coupon is already clipped
      clippedIndicator: [
        'button[aria-label*="Clipped"]',
        'button[aria-label*="clipped"]',
        'button[aria-label*="Added"]',
        '.coupon-clipped',
        '.clipped',
        'button[disabled][class*="clip" i]',
      ],
      // "Load More" or infinite scroll trigger
      loadMore: [
        'button[aria-label*="Load more"]',
        'button[aria-label*="Show more"]',
        'button[class*="load-more"]',
        'button[class*="show-more"]',
        'a[class*="load-more"]',
      ],
    },
  };

  // ── Utility Functions ──────────────────────────────────────────────

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  function querySelectorAll(selectorList) {
    const results = new Set();
    for (const selector of selectorList) {
      try {
        document.querySelectorAll(selector).forEach((el) => results.add(el));
      } catch {
        // Ignore invalid selectors
      }
    }
    return [...results];
  }

  function querySelector(selectorList) {
    for (const selector of selectorList) {
      try {
        const el = document.querySelector(selector);
        if (el) return el;
      } catch {
        // Ignore
      }
    }
    return null;
  }

  // ── Core Logic ─────────────────────────────────────────────────────

  async function scrollToLoadAll(statusEl) {
    let previousHeight = 0;
    let attempts = 0;

    while (attempts < CONFIG.maxScrollAttempts) {
      // Try clicking a "Load More" button first
      const loadMoreBtn = querySelector(CONFIG.selectors.loadMore);
      if (loadMoreBtn) {
        loadMoreBtn.click();
        statusEl.textContent = `Loading more coupons... (attempt ${attempts + 1})`;
        await sleep(CONFIG.scrollDelay);
        attempts++;
        continue;
      }

      // Scroll to bottom to trigger infinite scroll
      window.scrollTo(0, document.body.scrollHeight);
      await sleep(CONFIG.scrollDelay);

      const currentHeight = document.body.scrollHeight;
      if (currentHeight === previousHeight) {
        // No new content loaded – we've reached the end
        break;
      }
      previousHeight = currentHeight;
      attempts++;
      statusEl.textContent = `Scrolling to load all coupons... (${attempts}/${CONFIG.maxScrollAttempts})`;
    }

    // Scroll back to top
    window.scrollTo(0, 0);
    await sleep(500);
  }

  async function clipAllCoupons(statusEl, progressEl) {
    // Phase 1: Load all coupons
    statusEl.textContent = "Loading all available coupons...";
    await scrollToLoadAll(statusEl);

    // Phase 2: Find all unclipped coupon buttons
    const clipButtons = querySelectorAll(CONFIG.selectors.clipButton);
    const alreadyClipped = querySelectorAll(CONFIG.selectors.clippedIndicator);

    // Filter out buttons that are already clipped
    const clippedSet = new Set(alreadyClipped);
    const toClip = clipButtons.filter((btn) => {
      if (clippedSet.has(btn)) return false;
      if (btn.disabled) return false;
      const text = btn.textContent.toLowerCase();
      if (text.includes("clipped") || text.includes("added")) return false;
      return true;
    });

    if (toClip.length === 0) {
      statusEl.textContent = "No unclipped coupons found! All coupons may already be clipped.";
      progressEl.textContent = `Already clipped: ${alreadyClipped.length}`;
      return;
    }

    statusEl.textContent = `Found ${toClip.length} coupons to clip...`;
    progressEl.textContent = `Already clipped: ${alreadyClipped.length}`;
    await sleep(1000);

    // Phase 3: Click each coupon button with a delay
    let clipped = 0;
    let failed = 0;

    for (const btn of toClip) {
      try {
        // Scroll the button into view
        btn.scrollIntoView({ behavior: "smooth", block: "center" });
        await sleep(300);

        btn.click();
        clipped++;
        statusEl.textContent = `Clipping coupons: ${clipped}/${toClip.length}`;
        progressEl.textContent = `Clipped: ${clipped} | Failed: ${failed} | Remaining: ${toClip.length - clipped - failed}`;
      } catch (err) {
        failed++;
        console.warn("Failed to clip coupon:", err);
      }

      await sleep(CONFIG.clipDelay);
    }

    // Done
    statusEl.textContent = `Done! Clipped ${clipped} coupons.`;
    progressEl.textContent = `Total clipped: ${clipped} | Failed: ${failed} | Previously clipped: ${alreadyClipped.length}`;
  }

  // ── UI ─────────────────────────────────────────────────────────────

  function createUI() {
    const container = document.createElement("div");
    container.id = "sas-coupon-clipper";
    container.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      z-index: 999999;
      background: #ffffff;
      border: 2px solid #e31837;
      border-radius: 12px;
      padding: 16px 20px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.2);
      font-family: Arial, sans-serif;
      min-width: 300px;
      max-width: 400px;
    `;

    const title = document.createElement("div");
    title.textContent = "Coupon Clipper";
    title.style.cssText = `
      font-size: 16px;
      font-weight: bold;
      color: #e31837;
      margin-bottom: 10px;
    `;

    const statusEl = document.createElement("div");
    statusEl.textContent = "Ready to clip all coupons.";
    statusEl.style.cssText = `
      font-size: 13px;
      color: #333;
      margin-bottom: 6px;
    `;

    const progressEl = document.createElement("div");
    progressEl.textContent = "";
    progressEl.style.cssText = `
      font-size: 12px;
      color: #666;
      margin-bottom: 12px;
    `;

    const clipBtn = document.createElement("button");
    clipBtn.textContent = "Clip All Coupons";
    clipBtn.style.cssText = `
      background: #e31837;
      color: white;
      border: none;
      border-radius: 8px;
      padding: 10px 20px;
      font-size: 14px;
      font-weight: bold;
      cursor: pointer;
      width: 100%;
      transition: background 0.2s;
    `;
    clipBtn.addEventListener("mouseover", () => {
      clipBtn.style.background = "#c01530";
    });
    clipBtn.addEventListener("mouseout", () => {
      clipBtn.style.background = "#e31837";
    });

    const closeBtn = document.createElement("button");
    closeBtn.textContent = "X";
    closeBtn.style.cssText = `
      position: absolute;
      top: 8px;
      right: 12px;
      background: none;
      border: none;
      font-size: 16px;
      cursor: pointer;
      color: #999;
    `;
    closeBtn.addEventListener("click", () => {
      container.style.display =
        container.style.display === "none" ? "block" : "none";
    });

    let isRunning = false;
    clipBtn.addEventListener("click", async () => {
      if (isRunning) return;
      isRunning = true;
      clipBtn.disabled = true;
      clipBtn.textContent = "Clipping...";
      clipBtn.style.background = "#999";

      try {
        await clipAllCoupons(statusEl, progressEl);
      } catch (err) {
        statusEl.textContent = `Error: ${err.message}`;
        console.error("Coupon clipper error:", err);
      }

      clipBtn.disabled = false;
      clipBtn.textContent = "Clip All Coupons";
      clipBtn.style.background = "#e31837";
      isRunning = false;
    });

    container.appendChild(closeBtn);
    container.appendChild(title);
    container.appendChild(statusEl);
    container.appendChild(progressEl);
    container.appendChild(clipBtn);
    document.body.appendChild(container);
  }

  // ── Initialize ─────────────────────────────────────────────────────

  // Wait for the page to fully load before injecting UI
  if (document.readyState === "complete") {
    createUI();
  } else {
    window.addEventListener("load", createUI);
  }
})();
