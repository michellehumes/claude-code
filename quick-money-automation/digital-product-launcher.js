#!/usr/bin/env node

/**
 * DIGITAL PRODUCT FLASH SALE LAUNCHER
 *
 * Helps you create and launch a digital product in 30 minutes
 */

const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise(resolve => {
    rl.question(question, answer => {
      resolve(answer);
    });
  });
}

async function main() {
  console.log('\n🚀 DIGITAL PRODUCT FLASH SALE LAUNCHER\n');
  console.log('This will help you launch a product in 30 minutes\n');

  // Step 1: Product idea
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('STEP 1: Choose Your Product');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const productTypes = {
    1: 'Notion Template Pack',
    2: 'Canva Template Bundle',
    3: 'ChatGPT Prompt Library',
    4: 'Spreadsheet Tool/Calculator',
    5: 'Checklist/Guide PDF',
    6: 'Social Media Content Pack',
    7: 'Email Template Bundle',
    8: 'Resume/CV Templates'
  };

  for (let [num, type] of Object.entries(productTypes)) {
    console.log(`${num}. ${type}`);
  }

  const productChoice = await ask('\nChoose product type (1-8): ');
  const productType = productTypes[productChoice] || 'Digital Product';

  const productName = await ask('Product name: ');
  const niche = await ask('Target audience/niche: ');

  // Step 2: Pricing
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('STEP 2: Pricing Strategy');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const regularPrice = await ask('Regular price ($19-49 recommended): $');
  const flashPrice = await ask('Flash sale price ($9.99-19.99 recommended): $');

  // Step 3: Calculate profit
  const salesNeeded = Math.ceil(100 / parseFloat(flashPrice));

  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('PROFIT CALCULATOR');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  console.log(`Flash price: $${flashPrice}`);
  console.log(`Sales needed for $100: ${salesNeeded} sales`);
  console.log(`10 sales = $${(parseFloat(flashPrice) * 10).toFixed(2)}`);
  console.log(`20 sales = $${(parseFloat(flashPrice) * 20).toFixed(2)}`);

  // Step 4: Generate marketing copy
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('STEP 3: Marketing Copy (Copy & Paste)');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const copy = generateMarketingCopy(productName, productType, niche, regularPrice, flashPrice);

  console.log('REDDIT/FORUM POST:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(copy.reddit);

  console.log('\n\nTWITTER/X POST:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(copy.twitter);

  console.log('\n\nLINKEDIN POST:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(copy.linkedin);

  console.log('\n\nGUMROAD PRODUCT DESCRIPTION:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(copy.gumroad);

  // Step 5: Action checklist
  console.log('\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('STEP 4: YOUR ACTION CHECKLIST');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const checklist = [
    `[ ] Create the ${productType} (20-30 min)`,
    '[ ] Sign up/login to Gumroad.com',
    '[ ] Create product listing (use description above)',
    `[ ] Set price at $${flashPrice}`,
    '[ ] Upload your files',
    '[ ] Get product URL',
    '[ ] Post to Reddit (copy above) + add Gumroad link',
    '[ ] Post to Twitter (copy above) + add link',
    '[ ] Post to LinkedIn (copy above) + add link',
    '[ ] Share in Facebook groups (3-5 groups)',
    '[ ] Check for orders every 15 minutes',
    '[ ] Respond to questions FAST (under 5 min)',
    '[ ] After first sale, add "X people already bought this!"'
  ];

  checklist.forEach(item => console.log(item));

  // Where to post
  console.log('\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('WHERE TO POST (Open these now):');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const platforms = getRelevantPlatforms(productType, niche);
  platforms.forEach(platform => {
    console.log(`✓ ${platform.name}`);
    console.log(`  URL: ${platform.url}`);
    console.log(`  Why: ${platform.reason}\n`);
  });

  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('⏱️  START YOUR TIMER: 30 MINUTES');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  console.log('Your goal: Create and launch within 30 minutes!\n');
  console.log('Good luck! 🚀\n');

  rl.close();
}

function generateMarketingCopy(productName, productType, niche, regularPrice, flashPrice) {
  const discount = Math.round((1 - flashPrice / regularPrice) * 100);

  return {
    reddit: `I just launched "${productName}" - ${productType} for ${niche}

After spending weeks creating this, I'm running a 24-hour flash sale to get feedback from early users.

Regular price: $${regularPrice}
Flash sale (today only): $${flashPrice} (${discount}% off)

What's included:
[List 3-5 key features/benefits]

Perfect for anyone who wants to [solve specific problem].

Link: [YOUR GUMROAD LINK]

Would love to hear your thoughts!`,

    twitter: `Just launched: ${productName} 🚀

${productType} for ${niche}

24-hour flash sale:
❌ $${regularPrice}
✅ $${flashPrice} (${discount}% off)

Grab it: [link]

Limited time! ⏰`,

    linkedin: `I'm excited to share a new resource I've created for ${niche}:

"${productName}" - ${productType}

I've spent the last few weeks putting this together, and I'm offering it at a special launch price for the next 24 hours.

What's included:
• [Feature 1]
• [Feature 2]
• [Feature 3]
• [Feature 4]

Normally $${regularPrice}, but available for $${flashPrice} during this flash sale.

If you're looking to [achieve outcome], this will help you get there faster.

Link in comments. Would love your feedback!`,

    gumroad: `${productName}

The complete ${productType} designed specifically for ${niche}.

🎯 What you'll get:

[List all included items]

✨ Why this works:

[Benefit 1]
[Benefit 2]
[Benefit 3]

💰 Pricing:

Regular price: $${regularPrice}
⚡ Flash sale (24 hours): $${flashPrice}

🚀 Instant download. Lifetime access. Commercial license included.

Perfect for:
• [Use case 1]
• [Use case 2]
• [Use case 3]

Grab it now before the price goes up!`
  };
}

function getRelevantPlatforms(productType, niche) {
  const platforms = [
    {
      name: 'Gumroad',
      url: 'https://gumroad.com',
      reason: 'Main selling platform - start here'
    },
    {
      name: 'Twitter/X',
      url: 'https://twitter.com',
      reason: 'Fast virality potential, use hashtags'
    },
    {
      name: 'Reddit r/entrepreneur',
      url: 'https://reddit.com/r/entrepreneur',
      reason: 'Buyers actively looking for tools'
    },
    {
      name: 'Product Hunt',
      url: 'https://producthunt.com',
      reason: 'Tech-savvy audience, launches at midnight PT'
    },
    {
      name: 'Indie Hackers',
      url: 'https://indiehackers.com',
      reason: 'Great for productivity/business tools'
    }
  ];

  // Add niche-specific platforms
  if (productType.includes('Notion')) {
    platforms.push({
      name: 'r/Notion',
      url: 'https://reddit.com/r/notion',
      reason: 'Dedicated Notion community'
    });
  }

  if (productType.includes('Resume') || productType.includes('CV')) {
    platforms.push({
      name: 'r/jobs',
      url: 'https://reddit.com/r/jobs',
      reason: 'Job seekers need resumes'
    });
  }

  if (productType.includes('Social Media')) {
    platforms.push({
      name: 'r/socialmedia',
      url: 'https://reddit.com/r/socialmedia',
      reason: 'Social media managers'
    });
  }

  return platforms;
}

// Run the script
main().catch(console.error);
