# Stop & Shop Bulk Coupon Clipper

Automatically clip **all** available coupons on [stopandshop.com](https://www.stopandshop.com/coupons) instead of clicking them one at a time.

Three options are provided — pick whichever fits your comfort level.

---

## Option 1: Bookmarklet (Easiest)

No installs required. Works in any desktop browser.

### Setup
1. Open **bookmarklet.js** in this folder
2. Copy the entire line that starts with `javascript:void(...)`
3. Create a new bookmark in your browser toolbar
4. Name it **Clip All Coupons**
5. Paste the copied code as the bookmark **URL**

### Usage
1. Go to <https://www.stopandshop.com/coupons>
2. Log in to your account
3. Click the **Clip All Coupons** bookmark
4. A small panel will appear in the top-right showing progress
5. Wait for it to finish — all coupons will be loaded to your card

---

## Option 2: Tampermonkey Userscript (Automatic)

Runs every time you visit the coupons page. Adds a persistent "Clip All Coupons" button.

### Setup
1. Install the [Tampermonkey](https://www.tampermonkey.net/) browser extension
   - [Chrome](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)
   - [Firefox](https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/)
   - [Edge](https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfphd)
2. Click the Tampermonkey icon > **Create a new script**
3. Delete the template content
4. Copy/paste the entire contents of **stopandshop-clip-all.user.js**
5. Press **Ctrl+S** to save

### Usage
1. Go to <https://www.stopandshop.com/coupons>
2. Log in to your account
3. A red **"Clip All Coupons"** button appears in the top-right corner
4. Click it and watch the progress as all coupons get clipped

---

## Option 3: Node.js Puppeteer Script (Developer)

A standalone script that opens a browser and automates everything.

### Setup
```bash
cd stopandshop-coupon-clipper
npm install
```

### Usage
```bash
# Run with visible browser window (recommended for first use)
npm run start:visible

# Run headless (background)
npm start
```

The script will:
1. Open the Stop & Shop login page
2. Wait for you to log in manually
3. Navigate to the coupons page
4. Scroll to load all coupons
5. Click every unclipped coupon
6. Print a summary of results

---

## How It Works

All three approaches follow the same logic:

1. **Scroll** the coupons page to load all available coupons (handles infinite scroll and "Load More" buttons)
2. **Find** all unclipped coupon buttons by checking common selectors (`aria-label`, CSS classes, `data-testid` attributes)
3. **Click** each button with a short delay between clicks to avoid rate-limiting
4. **Report** progress and a final summary

## Troubleshooting

**"No unclipped coupons found"**
- Stop & Shop may have updated their website. The button selectors may need updating.
- Open browser DevTools (F12), go to the coupons page, and inspect a coupon's "Clip" button to find the current selector.
- Update the `selectors` in the script accordingly.

**Coupons load but don't clip**
- Increase the `clipDelay` value (e.g., from 800 to 1500) — the site may be rate-limiting.
- Make sure you're logged in before running the script.

**Page layout changed**
- Stop & Shop periodically redesigns their site. If the tool stops working, inspect the new coupon buttons and update the selectors in the config section at the top of each script.

## Disclaimer

This tool is for personal use to save time clipping coupons on your own Stop & Shop account. Use responsibly and in accordance with Stop & Shop's terms of service.
