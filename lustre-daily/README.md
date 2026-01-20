# LustreDaily - Beauty Blog

A production-ready, automated Amazon affiliate beauty blog built with Next.js, featuring daily content automation, SEO optimization, and full affiliate compliance.

## Features

- **50 Launch Articles**: 30 monetized + 20 non-monetized posts
- **Daily Automation**: 3 new posts/day (2 monetized, 1 trend) via GitHub Actions
- **Amazon Affiliate Integration**: Compliant link handling with configurable tag
- **SEO Optimized**: Sitemap, RSS feed, structured data, OpenGraph
- **Mobile-First Design**: Responsive Tailwind CSS styling
- **MDX Content**: Rich content with custom components

## Quick Start

### Local Development

```bash
# Navigate to project
cd lustre-daily

# Install dependencies
npm install

# Generate seed posts (first time only)
npm run generate:seed

# Start development server
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
npm start
```

## Configuration

### Amazon Associate Tag

The affiliate tag defaults to `shelzysbeauty-20`. To change it:

1. **Environment Variable** (recommended for production):
   ```bash
   AMAZON_ASSOC_TAG=your-tag-20
   ```

2. **Site Config** (for development):
   Edit `site.config.ts`:
   ```typescript
   amazonAssociateTag: process.env.AMAZON_ASSOC_TAG || "your-tag-20",
   ```

### Brand Name

Change the brand name by editing `site.config.ts`:

```typescript
export const siteConfig = {
  name: "YourBrandName",
  tagline: "Your Tagline Here",
  // ...
}
```

## Project Structure

```
lustre-daily/
├── .github/workflows/     # GitHub Actions for daily automation
├── content/
│   ├── posts/             # MDX blog posts
│   ├── products/          # Product catalog (products.json)
│   └── queues/            # Topic queues for automation
├── lib/                   # Utility functions
│   ├── affiliate.ts       # Affiliate link helpers
│   ├── posts.ts           # Post loading/parsing
│   ├── products.ts        # Product catalog helpers
│   ├── schema.ts          # Structured data generators
│   └── utils.ts           # General utilities
├── public/                # Static assets
├── scripts/               # Build & automation scripts
├── src/
│   ├── app/               # Next.js App Router pages
│   └── components/        # React components
│       ├── layout/        # Header, Footer
│       ├── mdx/           # MDX components
│       └── ui/            # UI components
├── site.config.ts         # Site configuration
└── package.json
```

## Content Management

### Post Types

1. **Monetized Posts** (with affiliate links)
   - Include `<ProductCard>` components
   - Have `monetized: true` in frontmatter
   - Include affiliate disclosure at top

2. **Non-Monetized Posts** (no affiliate links)
   - No ProductCard components
   - No Amazon links
   - Have `monetized: false` in frontmatter

### Post Frontmatter

```yaml
---
title: "Your Post Title"
description: "SEO description"
date: "2024-01-20"
category: "makeup"  # makeup, hair, skincare, trends
tags: ["foundation", "drugstore"]
heroImage: "/images/placeholder-hero.jpg"
monetized: true  # or false
---
```

### Custom Components

Available in MDX posts:

```mdx
<ProductCard asin="B0BEAUTY001" />

<Callout type="tip" title="Pro Tip">
  Your tip content here
</Callout>

<ProsCons
  pros={["Pro 1", "Pro 2"]}
  cons={["Con 1", "Con 2"]}
/>

<RoutineSteps
  title="Morning Routine"
  steps={[
    { title: "Cleanse", description: "Start with a gentle cleanser" },
    { title: "Tone", description: "Apply toner" }
  ]}
/>
```

## Daily Automation

### How It Works

GitHub Actions runs daily at 06:10 AM EST to:

1. Generate 2 monetized posts from topic queue
2. Generate 1 non-monetized trend post
3. Validate affiliate compliance
4. Build site to verify no errors
5. Commit and push changes

### Schedule

The workflow runs at **11:10 UTC** (06:10 AM America/New_York):

```yaml
schedule:
  - cron: "10 11 * * *"
```

### Manual Trigger

You can manually run the workflow from GitHub Actions with optional dry-run mode.

### Topic Queues

Edit topic queues in `content/queues/`:

- `monetized-topics.json` - Topics for affiliate posts
- `non-monetized-topics.json` - Topics for trend/news posts

## Validation

### Validate All Posts

```bash
npm run validate:affiliate
```

### Validate Seed Posts (50 total, 30/20 split)

```bash
npm run validate:affiliate seed
```

### Validate Daily Posts (3 total, 2/1 split)

```bash
npm run validate:affiliate daily
```

## Deployment

### Vercel (Recommended)

1. Push to GitHub
2. Import project in Vercel
3. Set environment variables:
   - `AMAZON_ASSOC_TAG` - Your affiliate tag
   - `NEXT_PUBLIC_SITE_URL` - Your production URL

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AMAZON_ASSOC_TAG` | Amazon Associate tag | `shelzysbeauty-20` |
| `NEXT_PUBLIC_SITE_URL` | Production URL | `https://lustredaily.com` |
| `LLM_PROVIDER` | LLM for content (optional) | none |
| `LLM_API_KEY` | LLM API key (optional) | none |

## NPM Scripts

| Script | Description |
|--------|-------------|
| `dev` | Start development server |
| `build` | Build for production |
| `start` | Start production server |
| `generate:seed` | Generate initial 50 posts |
| `generate:daily` | Generate 3 daily posts |
| `publish:daily` | Full daily publishing workflow |
| `validate:affiliate` | Validate affiliate compliance |
| `generate:sitemap` | Generate sitemap.xml |
| `generate:rss` | Generate RSS feeds |

## Products Catalog

Edit `content/products/products.json` to add/modify products:

```json
{
  "asin": "B0BEAUTY001",
  "name": "Product Name",
  "brand": "Brand Name",
  "category": "makeup",
  "shortDescription": "Brief description",
  "whyWeLikeIt": "Why we recommend it",
  "tags": ["foundation", "luxury"]
}
```

## Affiliate Compliance

The site includes all required Amazon Associates disclosures:

- Site-wide footer disclosure
- Dedicated Affiliate Disclosure page (`/affiliate-disclosure`)
- Per-post disclosure on monetized articles
- `rel="sponsored nofollow"` on affiliate links
- No specific price claims

## SEO Features

- **Sitemap**: Auto-generated at `/sitemap.xml`
- **RSS Feed**: Available at `/feed.xml`, `/atom.xml`, `/feed.json`
- **Robots.txt**: Configured for optimal crawling
- **Structured Data**: BlogPosting, Organization, BreadcrumbList schemas
- **OpenGraph**: Full meta tags for social sharing
- **Twitter Cards**: Summary large image cards

## License

Private - All rights reserved.
