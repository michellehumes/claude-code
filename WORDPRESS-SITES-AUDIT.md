# WordPress Sites Infrastructure Audit - Action Items

These sites run on WordPress/GeneratePress and cannot be modified via code in this repo.
Michelle needs to apply these changes via the WordPress admin dashboard.

---

## CustomGiftFinder.com (PRIORITY: HIGH - Site is invisible to Google)

### 1. CRITICAL: Fix Indexing (Site Not Appearing in Google)

Check these items in WordPress Admin:

- **Settings > Reading**: Uncheck "Discourage search engines from indexing this site" if checked
- **robots.txt**: Visit customgiftfinder.com/robots.txt in a browser
  - If it shows `Disallow: /`, the site is blocking all crawlers
  - Fix: Install Rank Math or Yoast SEO plugin, which manages robots.txt automatically
- **noindex tags**: Check if pages have `<meta name="robots" content="noindex">` in page source
  - If using Rank Math: Go to Rank Math > Titles & Meta > ensure pages are set to "Index"
  - If using Yoast: Check each page's SEO settings for noindex toggle
- **Sitemap**: Visit customgiftfinder.com/sitemap_index.xml
  - If it 404s, install Rank Math or Yoast and enable XML sitemap generation
  - Submit sitemap to Google Search Console at search.google.com/search-console

### 2. Google Search Console

- Go to search.google.com/search-console
- Add property for customgiftfinder.com (if not already added)
- Verify ownership via DNS TXT record or HTML file upload
- Submit sitemap URL
- Use "URL Inspection" tool to request indexing of key pages
- Check "Coverage" report for any crawl errors

### 3. GA4 Tracking

Option A (Plugin - Recommended):
- Install "Site Kit by Google" plugin
- Connect Google Analytics 4 account
- It will auto-add the tracking code

Option B (Manual):
- Go to Appearance > Customize > Additional CSS/Scripts (if GeneratePress has this)
- Or install "Insert Headers and Footers" plugin
- Add this to the header:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```
Replace G-XXXXXXXXXX with your GA4 measurement ID.

### 4. Upload Pending Posts

- Check Posts > All Posts in WordPress admin for any drafts
- If 6 pending articles exist as drafts, review and click "Publish" on each
- If they exist as local files, create new posts and paste content

### 5. Affiliate Link Verification

- Check all posts for Amazon affiliate links
- Every Amazon link should contain `tag=customgiftfinder-20`
- Example correct format: `https://www.amazon.com/dp/BXXXXXXXX?tag=customgiftfinder-20`
- Use browser "Find" (Ctrl+F) on each post to search for "amazon.com" and verify the tag

### 6. Schema Markup

Install Rank Math SEO plugin (free version):
- Go to Rank Math > Titles & Meta > Posts
- Set default Schema Type to "Article"
- For product review posts, edit each post and set Schema to "Product" or "Review"
- Rank Math auto-generates JSON-LD schema

Or manually add JSON-LD to each post via a custom field or code block:
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "review": {
    "@type": "Review",
    "author": {"@type": "Person", "name": "Michelle"},
    "reviewRating": {"@type": "Rating", "ratingValue": "4.5", "bestRating": "5"}
  }
}
```

### 7. Site Speed

- Run PageSpeed Insights: pagespeed.web.dev
- Common GeneratePress optimizations:
  - Enable caching plugin (WP Super Cache or LiteSpeed Cache)
  - Optimize images with ShortPixel or Imagify plugin
  - Minimize plugins (remove unused ones)
  - Use GeneratePress's built-in performance features

---

## CleverHomeStorage.com (PRIORITY: MEDIUM)

### 1. GA4 Tracking

Same steps as CustomGiftFinder above. Check if already installed:
- View page source and search for "gtag" or "GA4" or "G-"
- If Site Kit plugin is installed, check its settings
- If not present, add via Site Kit or Insert Headers and Footers plugin

### 2. Core Web Vitals

- Run PageSpeed Insights at pagespeed.web.dev for desktop and mobile
- Common issues with WordPress/GeneratePress:
  - LCP (Largest Contentful Paint): Optimize hero images, use WebP format
  - CLS (Cumulative Layout Shift): Set explicit width/height on images
  - FID/INP: Minimize JavaScript, defer non-critical scripts
- Install WP Rocket or LiteSpeed Cache for caching
- Install ShortPixel for image optimization

### 3. Schema Markup

With 33+ buying guides, schema is important for rich snippets:

Install Rank Math SEO plugin:
- Set default post schema to "Article"
- For buying guides, manually set schema to "Product" + "Review" on each post
- For FAQ sections within articles, add FAQ schema:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Question text here",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Answer text here"
    }
  }]
}
```

### 4. Affiliate Link Audit

- All 33+ articles should use Amazon tag: `customgiftfinder-20`
- This IS the correct tag (same tag used across both CleverHomeStorage and CustomGiftFinder)
- Check each article by searching page source for "amazon.com"
- Verify each link contains `tag=customgiftfinder-20`
- Flag any broken links (404s) by clicking through them
- Consider using "Broken Link Checker" WordPress plugin for automated checking

### 5. OG Image Tags

Check if og:image tags are present:
- View page source of any article page
- Search for "og:image"
- If missing, Rank Math or Yoast SEO will auto-generate these from the featured image
- Ensure every post has a Featured Image set in WordPress

### 6. XML Sitemap

- Check if sitemap exists: cleverhomestorage.com/sitemap_index.xml
- If using Rank Math: Go to Rank Math > Sitemap Settings > enable
- If using Yoast: Go to Yoast > Settings > Site features > XML sitemaps
- Submit sitemap URL to Google Search Console

---

## Domain & DNS Instructions

### cadencehealthmedia.com (connect to Netlify)

If DNS is managed at GoDaddy:
1. Log in to GoDaddy > DNS Management for cadencehealthmedia.com
2. Add/update these records:
   - **A Record**: Host: `@`, Points to: `75.2.60.5`
   - **CNAME Record**: Host: `www`, Points to: `thunderous-sawine-53ff65.netlify.app`
3. In Netlify dashboard:
   - Go to Site settings > Domain management > Add custom domain
   - Add `cadencehealthmedia.com`
   - Add `www.cadencehealthmedia.com`
   - SSL will auto-provision via Let's Encrypt

### shelzysdesigns.com (connect to Vercel)

1. In Vercel dashboard:
   - Go to Project settings > Domains
   - Add `shelzysdesigns.com`
   - Add `www.shelzysdesigns.com`
2. Update DNS records at your registrar:
   - **A Record**: Host: `@`, Points to: `76.76.21.21`
   - **CNAME Record**: Host: `www`, Points to: `cname.vercel-dns.com`
3. SSL auto-provisions on Vercel

### Email Forwarding for michelle@cadencehealthmedia.com

Option A - GoDaddy Email Forwarding:
1. GoDaddy > Products > Email > Set up forwarding
2. Create forward from michelle@cadencehealthmedia.com to personal email

Option B - ImprovMX (Free):
1. Sign up at improvmx.com
2. Add cadencehealthmedia.com
3. Add MX records to DNS:
   - MX: `mx1.improvmx.com` (priority 10)
   - MX: `mx2.improvmx.com` (priority 20)
4. Add SPF TXT record: `v=spf1 include:spf.improvmx.com ~all`

Option C - Cloudflare Email Routing (Free):
1. Move DNS to Cloudflare (free plan)
2. Use Email Routing to forward michelle@cadencehealthmedia.com
