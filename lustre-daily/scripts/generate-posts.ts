#!/usr/bin/env npx ts-node

/**
 * Post Generation Script
 * Generates MDX posts for the beauty blog
 *
 * Usage:
 *   npm run generate:seed      - Generate initial 50 posts (30 monetized, 20 non-monetized)
 *   npm run generate:daily     - Generate 3 daily posts (2 monetized, 1 non-monetized)
 *
 * Environment Variables:
 *   LLM_PROVIDER     - LLM provider (optional: openai, anthropic, none)
 *   LLM_API_KEY      - API key for LLM provider
 *   AMAZON_ASSOC_TAG - Amazon Associate tag (defaults to shelzysbeauty-20)
 */

import fs from "fs";
import path from "path";

interface Product {
  asin: string;
  name: string;
  brand: string;
  category: string;
  image?: string;
  shortDescription: string;
  whyWeLikeIt: string;
  tags: string[];
}

interface Topic {
  id: string;
  title: string;
  category: string;
  type: string;
  productTags?: string[];
  used: boolean;
}

interface PostFrontmatter {
  title: string;
  description: string;
  date: string;
  category: string;
  tags: string[];
  heroImage: string;
  monetized: boolean;
}

// Load products
function loadProducts(): Product[] {
  const productsPath = path.join(process.cwd(), "content/products/products.json");
  const data = JSON.parse(fs.readFileSync(productsPath, "utf8"));
  return data.products;
}

// Load topics
function loadTopics(monetized: boolean): Topic[] {
  const filename = monetized ? "monetized-topics.json" : "non-monetized-topics.json";
  const topicsPath = path.join(process.cwd(), "content/queues", filename);
  const data = JSON.parse(fs.readFileSync(topicsPath, "utf8"));
  return data.topics;
}

// Save topics (to mark as used)
function saveTopics(topics: Topic[], monetized: boolean): void {
  const filename = monetized ? "monetized-topics.json" : "non-monetized-topics.json";
  const topicsPath = path.join(process.cwd(), "content/queues", filename);
  const data = {
    description: monetized
      ? "Queue of topics for monetized posts (with affiliate links). Each topic has a suggested category and product focus areas."
      : "Queue of topics for non-monetized posts (no affiliate links). These are trend pieces, news, techniques, and educational content.",
    topics,
  };
  fs.writeFileSync(topicsPath, JSON.stringify(data, null, 2));
}

// Get products by tags with category fallback
function getProductsByTags(products: Product[], tags: string[], count: number, category?: string): Product[] {
  const minCount = 6; // Minimum products needed
  const targetCount = Math.max(count, minCount);

  // First, try to match by tags
  const matching = products.filter((p) =>
    p.tags.some((t) => tags.map((tag) => tag.toLowerCase()).includes(t.toLowerCase()))
  );

  // Shuffle matching products
  let result = matching.sort(() => Math.random() - 0.5);

  // If not enough, add products from the same category
  if (result.length < targetCount && category) {
    const categoryProducts = products.filter(
      (p) => p.category === category && !result.some((r) => r.asin === p.asin)
    );
    const shuffledCategory = categoryProducts.sort(() => Math.random() - 0.5);
    result = [...result, ...shuffledCategory];
  }

  // If still not enough, add any remaining products
  if (result.length < targetCount) {
    const remaining = products.filter((p) => !result.some((r) => r.asin === p.asin));
    const shuffledRemaining = remaining.sort(() => Math.random() - 0.5);
    result = [...result, ...shuffledRemaining];
  }

  return result.slice(0, targetCount);
}

// Generate slug from title
function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, "")
    .replace(/[\s_-]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

// Get date string for post (spread posts over past 30 days for seed)
function getDateString(index: number, total: number, isSeed: boolean): string {
  if (!isSeed) {
    return new Date().toISOString().split("T")[0];
  }

  const now = new Date();
  const daysAgo = Math.floor((index / total) * 30);
  const date = new Date(now.getTime() - daysAgo * 24 * 60 * 60 * 1000);
  return date.toISOString().split("T")[0];
}

// Generate monetized post content
function generateMonetizedPost(topic: Topic, products: Product[], date: string): string {
  const selectedProducts = getProductsByTags(
    products,
    topic.productTags || [],
    8,
    topic.category !== "trends" ? topic.category : undefined
  );

  const frontmatter: PostFrontmatter = {
    title: topic.title,
    description: generateDescription(topic.title, topic.category, true),
    date,
    category: topic.category,
    tags: generateTags(topic.title, topic.category, topic.productTags),
    heroImage: "/images/placeholder-hero.jpg",
    monetized: true,
  };

  const productCards = selectedProducts
    .map(
      (p) =>
        `<ProductCard asin="${p.asin}" name="${p.name}" brand="${p.brand}" description="${p.shortDescription}" whyWeLikeIt="${p.whyWeLikeIt}"${p.image ? ` image="${p.image}"` : ""} />`
    )
    .join("\n\n");

  const content = generateMonetizedContent(topic, selectedProducts, productCards);

  return formatMdx(frontmatter, content);
}

// Generate non-monetized post content
function generateNonMonetizedPost(topic: Topic, date: string): string {
  const frontmatter: PostFrontmatter = {
    title: topic.title,
    description: generateDescription(topic.title, topic.category, false),
    date,
    category: topic.category,
    tags: generateTags(topic.title, topic.category),
    heroImage: "/images/placeholder-hero.jpg",
    monetized: false,
  };

  const content = generateNonMonetizedContent(topic);

  return formatMdx(frontmatter, content);
}

// Generate description based on title
function generateDescription(title: string, category: string, monetized: boolean): string {
  const descriptions: Record<string, string[]> = {
    makeup: [
      `Discover ${title.toLowerCase()} with our expert picks and insider tips for flawless application.`,
      `Everything you need to know about ${title.toLowerCase()} from our beauty editors.`,
      `Master ${title.toLowerCase()} with this comprehensive guide featuring pro techniques.`,
    ],
    hair: [
      `Transform your hair routine with our guide to ${title.toLowerCase()}.`,
      `Expert advice on ${title.toLowerCase()} for healthier, more beautiful hair.`,
      `Your complete guide to ${title.toLowerCase()} from professionals who know.`,
    ],
    skincare: [
      `Achieve your best skin yet with our deep dive into ${title.toLowerCase()}.`,
      `Everything dermatologists want you to know about ${title.toLowerCase()}.`,
      `The ultimate guide to ${title.toLowerCase()} for glowing, healthy skin.`,
    ],
    trends: [
      `Breaking down ${title.toLowerCase()} and why it matters in beauty right now.`,
      `A complete analysis of ${title.toLowerCase()} shaping the beauty industry.`,
      `Understanding ${title.toLowerCase()} and how to make it work for you.`,
    ],
  };

  const options = descriptions[category] || descriptions.trends;
  return options[Math.floor(Math.random() * options.length)];
}

// Generate tags
function generateTags(title: string, category: string, productTags?: string[]): string[] {
  const baseTags = [category];

  if (productTags) {
    baseTags.push(...productTags.slice(0, 3));
  }

  // Add some common tags based on title keywords
  const titleLower = title.toLowerCase();
  if (titleLower.includes("best")) baseTags.push("recommendations");
  if (titleLower.includes("guide")) baseTags.push("guide");
  if (titleLower.includes("routine")) baseTags.push("routine");
  if (titleLower.includes("trend")) baseTags.push("trends");
  if (titleLower.includes("drugstore")) baseTags.push("budget-friendly");
  if (titleLower.includes("luxury")) baseTags.push("luxury");

  return [...new Set(baseTags)].slice(0, 5);
}

// Generate monetized content
function generateMonetizedContent(topic: Topic, products: Product[], productCards: string): string {
  const intro = getMonetizedIntro(topic);
  const sections = getMonetizedSections(topic, products, productCards);
  const conclusion = getMonetizedConclusion(topic);

  return `${intro}

${sections}

${conclusion}`;
}

// Get monetized intro
function getMonetizedIntro(topic: Topic): string {
  const intros: Record<string, string[]> = {
    roundup: [
      `Finding the right products can feel overwhelming with so many options on the market. We've done the research, testing, and comparing so you don't have to. Here are our top picks that deliver real results.`,
      `After months of testing and countless product trials, we've narrowed down the absolute best options available right now. These picks have earned their spot through performance, value, and rave reviews from our team and readers alike.`,
      `Whether you're a beauty beginner or a seasoned pro, having the right products makes all the difference. We've curated this list based on performance, ingredients, and real-world results.`,
    ],
    guide: [
      `Navigating the world of beauty products doesn't have to be complicated. This comprehensive guide breaks down everything you need to know, along with our top product recommendations at every price point.`,
      `Consider this your ultimate resource for making informed decisions. We've combined expert knowledge with hands-on testing to bring you a guide that actually helps.`,
      `From understanding what to look for to finding products that deliver, this guide covers it all. Let's dive into what really works.`,
    ],
    routine: [
      `Building an effective routine is about choosing the right products and using them in the right order. Here's exactly what you need and how to use it for best results.`,
      `A good routine doesn't require dozens of products—it requires the right ones. We've put together a streamlined approach that maximizes results without the overwhelm.`,
      `Ready to upgrade your routine? These are the products that have earned permanent spots in our beauty arsenal.`,
    ],
    comparison: [
      `With so many options available, knowing which products truly deliver can save you time and money. We've put these head-to-head to help you decide.`,
      `The debate is real, and we're here to settle it. After extensive testing, here's what you need to know about each option.`,
      `Both approaches have their merits, but which is right for you? Let's break down the pros, cons, and best products for each.`,
    ],
    tutorial: [
      `Achieving professional results at home is absolutely possible with the right technique and products. Here's your step-by-step guide to success.`,
      `We've broken down the process into easy-to-follow steps, complete with product recommendations that make the technique foolproof.`,
      `Ready to master this technique? Follow along as we walk you through exactly how to get stunning results.`,
    ],
  };

  const options = intros[topic.type] || intros.roundup;
  return options[Math.floor(Math.random() * options.length)];
}

// Get monetized sections
function getMonetizedSections(topic: Topic, products: Product[], productCards: string): string {
  const productCardsArray = productCards.split("\n\n");
  const sections: string[] = [];

  // Introduction section
  sections.push(`## What to Look For

When shopping for products in this category, keep these key factors in mind:

- **Ingredients**: Look for proven, effective ingredients that match your specific concerns.
- **Formula**: Consider your preferences—do you prefer lightweight textures or rich formulas?
- **Value**: The most expensive option isn't always the best. We've included picks at various price points.
- **Reviews**: Real user experiences matter. We consider both professional testing and community feedback.

<Callout type="tip" title="Pro Tip">
Start with one new product at a time to see how your skin or hair responds before building a complete routine.
</Callout>`);

  // Product sections
  if (products.length > 0) {
    sections.push(`## Our Top Picks

After extensive research and testing, these are the products that consistently deliver results:`);

    // Add products with context
    productCardsArray.forEach((card, index) => {
      if (card.trim()) {
        const product = products[index];
        if (product) {
          sections.push(`### ${index + 1}. ${product.brand} ${product.name}

${card}`);
        }
      }
    });
  }

  // How to choose section
  sections.push(`## How to Choose the Right Product

Not sure which option is best for you? Consider these factors:

1. **Your specific concerns**: Match the product benefits to your needs.
2. **Your budget**: Great options exist at every price point.
3. **Your routine**: Consider how this fits with products you already use.
4. **Your preferences**: Texture, scent, and application method all matter for consistency.

<Callout type="expert" title="Expert Advice">
Don't be afraid to try samples or travel sizes before committing to a full-size product. Many retailers offer generous sample programs.
</Callout>`);

  // Tips section
  sections.push(`## Application Tips for Best Results

Getting the most out of your products often comes down to technique:

- **Consistency matters**: Use products as directed for the recommended time period before judging results.
- **Order matters**: Apply products from thinnest to thickest consistency.
- **Less is more**: Start with a small amount—you can always add more.
- **Give it time**: Most products need 4-6 weeks of consistent use to show full results.`);

  return sections.join("\n\n");
}

// Get monetized conclusion
function getMonetizedConclusion(topic: Topic): string {
  return `## The Bottom Line

Finding the right products is a personal journey, and what works for one person may not work for another. The options we've shared here represent the best of what's available right now, backed by research, testing, and real results.

Remember, the best product is one you'll actually use consistently. Start with the option that feels right for your needs and budget, and don't be afraid to adjust as you learn what works best for you.

Have you tried any of these products? We'd love to hear about your experience in the comments below.`;
}

// Generate non-monetized content
function generateNonMonetizedContent(topic: Topic): string {
  const intro = getNonMonetizedIntro(topic);
  const sections = getNonMonetizedSections(topic);
  const conclusion = getNonMonetizedConclusion(topic);

  return `${intro}

${sections}

${conclusion}`;
}

// Get non-monetized intro
function getNonMonetizedIntro(topic: Topic): string {
  const intros: Record<string, string[]> = {
    "trend-analysis": [
      `Social media is buzzing, beauty editors are taking notes, and this trend has officially entered the mainstream. But what exactly is it, and is it worth your attention? Let's break it down.`,
      `Every so often, a trend emerges that genuinely shifts how we think about beauty. This is one of those moments. Here's everything you need to know.`,
      `From runways to real life, this trend has captured the attention of beauty enthusiasts everywhere. Let's explore why it's resonating and how to make it your own.`,
    ],
    "deep-dive": [
      `Some topics deserve more than a surface-level look. We're going deep to explore the history, science, and cultural significance that makes this fascinating.`,
      `Pull up a chair—we're about to explore every angle of this topic with the depth it deserves.`,
      `There's more to this story than meets the eye. Let's dig into what really matters.`,
    ],
    educational: [
      `Understanding the fundamentals changes everything. Whether you're new to this or looking to deepen your knowledge, this guide has you covered.`,
      `Knowledge is power, especially when it comes to making informed decisions. Here's what you need to know.`,
      `Let's cut through the confusion and get to the facts. This comprehensive breakdown explains everything clearly.`,
    ],
    "ingredient-deep-dive": [
      `Ingredient lists can be confusing, but understanding what actually works—and why—empowers you to make better choices. Let's decode this popular ingredient.`,
      `This ingredient has developed a cult following, and for good reason. Here's the science behind the hype.`,
      `From lab research to real-world results, here's everything you need to know about this powerhouse ingredient.`,
    ],
    "event-coverage": [
      `The beauty looks at this event had everyone talking. From bold statements to subtle elegance, here are the moments that stood out.`,
      `Red carpets and major events always bring beauty inspiration. These are the looks that caught our eye and why they work.`,
      `Every major event brings fresh beauty inspiration. Here's our breakdown of the most notable looks and how to interpret them for everyday wear.`,
    ],
    "expert-insight": [
      `We went straight to the experts to get the real story. Here's what the professionals actually think—and it might surprise you.`,
      `Cutting through the noise requires expertise. We gathered insights from industry professionals to separate fact from fiction.`,
      `When trends go viral, experts weigh in. Here's what they want you to know before you try this for yourself.`,
    ],
  };

  const options = intros[topic.type] || intros["trend-analysis"];
  return options[Math.floor(Math.random() * options.length)];
}

// Get non-monetized sections
function getNonMonetizedSections(topic: Topic): string {
  const sections: string[] = [];

  // Context section
  sections.push(`## Understanding the Context

To truly appreciate what's happening here, we need to look at the bigger picture. This isn't just a passing fad—it reflects broader shifts in how we think about beauty, self-expression, and authenticity.

The beauty industry has always been a mirror reflecting cultural values, and current trends are no exception. What we're seeing now is a response to years of heavily curated, filtered aesthetics.

<Callout type="info">
Trends don't emerge in a vacuum. They're responses to what came before and predictions of where we're headed.
</Callout>`);

  // Main analysis
  sections.push(`## Breaking It Down

Let's examine the key elements that define this moment:

### The Aesthetic
At its core, this approach prioritizes a specific look and feel that resonates with contemporary values. It's less about perfection and more about intentionality.

### The Philosophy
Beyond the surface, there's a mindset shift happening. This isn't just about looking a certain way—it's about a relationship with beauty that feels sustainable and authentic.

### The Accessibility
One reason for widespread adoption is accessibility. Unlike trends that require expensive products or professional skills, this approach can be adapted to various budgets and skill levels.`);

  // Expert perspective
  sections.push(`## What Experts Say

Industry professionals have weighed in with varied perspectives:

> "What we're seeing is a natural evolution. People are more educated than ever about what works and what doesn't." — Industry Expert

The consensus seems to be that this represents a maturation of beauty culture rather than a radical departure. It's refinement, not revolution.

<Callout type="expert" title="Expert Perspective">
Long-term trends often start as reactions to excess. The current moment is about finding balance and sustainability in beauty routines.
</Callout>`);

  // Practical applications
  sections.push(`## How to Approach This

If you're interested in incorporating these ideas into your own routine, consider these principles:

1. **Start with intention**: Before making changes, think about what you want to achieve.
2. **Adapt, don't copy**: Make trends work for your unique features and lifestyle.
3. **Be patient**: Meaningful changes in routine take time to show results.
4. **Stay critical**: Not everything popular is right for everyone.

The best approach is always one that feels authentic to you while incorporating elements that genuinely improve your routine.`);

  // Cultural context
  sections.push(`## The Bigger Picture

Beauty trends are never just about beauty. They reflect broader cultural conversations about identity, wellness, sustainability, and self-expression.

What makes this particular moment interesting is how it synthesizes influences from multiple sources—social media, professional expertise, cultural movements, and individual creativity.

As we move forward, expect to see continued evolution. The beauty industry is remarkably adaptive, and today's trend becomes tomorrow's foundation for something new.`);

  return sections.join("\n\n");
}

// Get non-monetized conclusion
function getNonMonetizedConclusion(topic: Topic): string {
  return `## Final Thoughts

Whether you fully embrace this trend, take selective inspiration, or simply appreciate understanding what's happening in the beauty world, staying informed empowers better decisions.

The most important thing to remember is that trends are tools, not rules. Use what serves you, leave what doesn't, and always prioritize what makes you feel confident and comfortable.

What's your take on this? Share your thoughts in the comments—we'd love to hear how you're interpreting these ideas in your own beauty journey.

*This article is for informational purposes only and reflects current trends and expert opinions at the time of publication.*`;
}

// Format MDX file
function formatMdx(frontmatter: PostFrontmatter, content: string): string {
  const frontmatterYaml = `---
title: "${frontmatter.title}"
description: "${frontmatter.description}"
date: "${frontmatter.date}"
category: "${frontmatter.category}"
tags: ${JSON.stringify(frontmatter.tags)}
heroImage: "${frontmatter.heroImage}"
monetized: ${frontmatter.monetized}
---`;

  return `${frontmatterYaml}

${content}
`;
}

// Save post to file
function savePost(slug: string, content: string): void {
  const postsDir = path.join(process.cwd(), "content/posts");
  if (!fs.existsSync(postsDir)) {
    fs.mkdirSync(postsDir, { recursive: true });
  }

  const filePath = path.join(postsDir, `${slug}.mdx`);
  fs.writeFileSync(filePath, content);
  console.log(`Created: ${filePath}`);
}

// Generate seed posts (50 total: 30 monetized, 20 non-monetized)
async function generateSeedPosts(): Promise<void> {
  console.log("Generating seed posts (50 total: 30 monetized, 20 non-monetized)...\n");

  const products = loadProducts();
  const monetizedTopics = loadTopics(true);
  const nonMonetizedTopics = loadTopics(false);

  let monetizedCount = 0;
  let nonMonetizedCount = 0;
  const totalPosts = 50;

  // Generate 30 monetized posts
  for (let i = 0; i < 30 && i < monetizedTopics.length; i++) {
    const topic = monetizedTopics[i];
    if (!topic.used) {
      const date = getDateString(i, totalPosts, true);
      const content = generateMonetizedPost(topic, products, date);
      const slug = `${date}-${slugify(topic.title)}`;
      savePost(slug, content);
      topic.used = true;
      monetizedCount++;
    }
  }

  // Generate 20 non-monetized posts
  for (let i = 0; i < 20 && i < nonMonetizedTopics.length; i++) {
    const topic = nonMonetizedTopics[i];
    if (!topic.used) {
      const date = getDateString(30 + i, totalPosts, true);
      const content = generateNonMonetizedPost(topic, date);
      const slug = `${date}-${slugify(topic.title)}`;
      savePost(slug, content);
      topic.used = true;
      nonMonetizedCount++;
    }
  }

  // Save updated topics
  saveTopics(monetizedTopics, true);
  saveTopics(nonMonetizedTopics, false);

  console.log(`\nGeneration complete!`);
  console.log(`Monetized posts: ${monetizedCount}`);
  console.log(`Non-monetized posts: ${nonMonetizedCount}`);
  console.log(`Total: ${monetizedCount + nonMonetizedCount}`);
}

// Generate daily posts (3 total: 2 monetized, 1 non-monetized)
async function generateDailyPosts(): Promise<void> {
  console.log("Generating daily posts (3 total: 2 monetized, 1 non-monetized)...\n");

  const products = loadProducts();
  const monetizedTopics = loadTopics(true);
  const nonMonetizedTopics = loadTopics(false);

  const date = new Date().toISOString().split("T")[0];
  let monetizedCount = 0;
  let nonMonetizedCount = 0;

  // Generate 2 monetized posts
  const unusedMonetized = monetizedTopics.filter((t) => !t.used);
  for (let i = 0; i < 2 && i < unusedMonetized.length; i++) {
    const topic = unusedMonetized[i];
    const content = generateMonetizedPost(topic, products, date);
    const slug = `${date}-${slugify(topic.title)}`;
    savePost(slug, content);

    // Mark as used
    const topicIndex = monetizedTopics.findIndex((t) => t.id === topic.id);
    if (topicIndex !== -1) {
      monetizedTopics[topicIndex].used = true;
    }
    monetizedCount++;
  }

  // Generate 1 non-monetized post
  const unusedNonMonetized = nonMonetizedTopics.filter((t) => !t.used);
  if (unusedNonMonetized.length > 0) {
    const topic = unusedNonMonetized[0];
    const content = generateNonMonetizedPost(topic, date);
    const slug = `${date}-${slugify(topic.title)}`;
    savePost(slug, content);

    // Mark as used
    const topicIndex = nonMonetizedTopics.findIndex((t) => t.id === topic.id);
    if (topicIndex !== -1) {
      nonMonetizedTopics[topicIndex].used = true;
    }
    nonMonetizedCount++;
  }

  // Save updated topics
  saveTopics(monetizedTopics, true);
  saveTopics(nonMonetizedTopics, false);

  console.log(`\nGeneration complete!`);
  console.log(`Monetized posts: ${monetizedCount}`);
  console.log(`Non-monetized posts: ${nonMonetizedCount}`);
  console.log(`Total: ${monetizedCount + nonMonetizedCount}`);

  // Validation
  if (monetizedCount !== 2 || nonMonetizedCount !== 1) {
    console.error("\nWARNING: Daily post counts do not match expected ratios!");
    console.error("Expected: 2 monetized, 1 non-monetized");
    process.exit(1);
  }
}

// Main execution
const args = process.argv.slice(2);
const mode = args[0] || "seed";

if (mode === "seed") {
  generateSeedPosts();
} else if (mode === "daily") {
  generateDailyPosts();
} else {
  console.log("Usage: npx ts-node scripts/generate-posts.ts [seed|daily]");
  process.exit(1);
}
