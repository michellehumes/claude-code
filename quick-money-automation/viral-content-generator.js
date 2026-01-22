#!/usr/bin/env node

/**
 * VIRAL CONTENT GENERATOR
 *
 * Creates viral Twitter threads, LinkedIn posts, and more
 * Then helps you monetize them instantly
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

const VIRAL_FORMULAS = {
  1: {
    name: 'Data Analysis Thread',
    template: 'I analyzed [NUMBER] [THING] and found [X] patterns...',
    example: 'I analyzed 1000 viral tweets and found 7 patterns that got 100k+ views',
    potential: 'High - People love data-backed insights'
  },
  2: {
    name: 'Journey Story',
    template: 'How I went from [BEFORE] to [AFTER] in [TIME]',
    example: 'How I went from $0 to $10k MRR in 6 months (full breakdown)',
    potential: 'Very High - Transformation stories always work'
  },
  3: {
    name: 'Numbered List',
    template: '[NUMBER] [TACTICS/TIPS/SECRETS] that got me [RESULT]',
    example: '7 copywriting tricks that 10x my conversion rate',
    potential: 'High - Easy to scan, actionable'
  },
  4: {
    name: 'Controversial Take',
    template: 'Unpopular opinion: [CONTROVERSIAL STATEMENT]',
    example: 'Unpopular opinion: You don't need a business plan to make $10k',
    potential: 'Very High - Controversy drives engagement'
  },
  5: {
    name: 'Challenge Results',
    template: 'I tried [THING] for [TIME], here's what happened',
    example: 'I posted on Twitter every day for 30 days. Results:',
    potential: 'High - Curiosity-driven'
  },
  6: {
    name: 'Mistake Lessons',
    template: 'I lost/wasted [X] on [Y]. Here's what I learned',
    example: 'I wasted $5000 on Facebook ads. Here are the 5 mistakes I made',
    potential: 'High - People learn from failures'
  },
  7: {
    name: 'Behind the Scenes',
    template: 'Here's exactly how I [ACHIEVEMENT]',
    example: 'Here's exactly how I got 10k followers in 60 days',
    potential: 'Very High - Transparency builds trust'
  },
  8: {
    name: 'Tool Stack',
    template: 'My [GOAL] tech stack (tools that actually work)',
    example: 'My $50k/mo side hustle tech stack (15 tools)',
    potential: 'High - Everyone wants shortcuts'
  }
};

const MONETIZATION_METHODS = [
  {
    name: 'Gumroad Product in Bio',
    setup: '5 minutes',
    potential: '$50-500',
    howTo: 'Create quick guide/template related to thread topic, price at $9.99, link in bio'
  },
  {
    name: 'DM for Full Guide',
    setup: '10 minutes',
    potential: '$100-300',
    howTo: 'Tweet: "DM me for the full breakdown" → Send payment link → Deliver PDF guide'
  },
  {
    name: 'Consulting Offer',
    setup: '2 minutes',
    potential: '$50-200',
    howTo: 'Bio: "Book a 15-min call: $50" → Calendly link → Quick calls'
  },
  {
    name: 'Email List → Product',
    setup: '15 minutes',
    potential: '$200-1000',
    howTo: 'Tweet: "I wrote a full guide, link in bio" → Collect emails → Sell $19 product'
  },
  {
    name: 'Thread → Course',
    setup: '30 minutes',
    potential: '$300-2000',
    howTo: 'Create Gumroad course from thread content, price at $49-99'
  }
];

async function main() {
  console.log('\n🔥 VIRAL CONTENT MONETIZATION GENERATOR\n');
  console.log('Create viral content + monetize it instantly\n');

  // Step 1: Choose formula
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('STEP 1: Choose Your Viral Formula');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  for (let [num, formula] of Object.entries(VIRAL_FORMULAS)) {
    console.log(`${num}. ${formula.name}`);
    console.log(`   Template: "${formula.template}"`);
    console.log(`   Example: "${formula.example}"`);
    console.log(`   Viral Potential: ${formula.potential}\n`);
  }

  const formulaChoice = await ask('Choose formula (1-8): ');
  const formula = VIRAL_FORMULAS[formulaChoice];

  if (!formula) {
    console.log('Invalid choice. Exiting.');
    rl.close();
    return;
  }

  // Step 2: Customize
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`STEP 2: Customize Your ${formula.name}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const topic = await ask('Your topic/niche: ');
  const credibility = await ask('Your credibility/result (e.g., "made $10k", "got 50k followers"): ');

  // Step 3: Generate content
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('STEP 3: Your Viral Content (Ready to Post)');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const content = generateContent(formula, topic, credibility);

  console.log('TWITTER THREAD:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(content.twitter);

  console.log('\n\nLINKEDIN POST:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(content.linkedin);

  // Step 4: Monetization
  console.log('\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('STEP 4: Choose Monetization Method');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  MONETIZATION_METHODS.forEach((method, i) => {
    console.log(`${i + 1}. ${method.name}`);
    console.log(`   Setup time: ${method.setup}`);
    console.log(`   Potential: ${method.potential}`);
    console.log(`   How: ${method.howTo}\n`);
  });

  const monetizeChoice = await ask('Choose method (1-5): ');
  const method = MONETIZATION_METHODS[parseInt(monetizeChoice) - 1];

  if (method) {
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('YOUR MONETIZATION SETUP');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

    const monetizationGuide = generateMonetizationGuide(method, topic, credibility);
    console.log(monetizationGuide);
  }

  // Step 5: Action plan
  console.log('\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('STEP 5: ACTION CHECKLIST');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const checklist = [
    '[ ] Create your monetization product (10-30 min)',
    '[ ] Set up payment link (Gumroad/Stripe/PayPal)',
    '[ ] Update Twitter bio with offer',
    '[ ] Post thread to Twitter',
    '[ ] Post to LinkedIn',
    '[ ] Pin thread to profile',
    '[ ] Check replies every 15 min',
    '[ ] Respond to ALL comments (boosts algorithm)',
    '[ ] Track clicks/sales',
    '[ ] Add "X people bought" social proof after first sale'
  ];

  checklist.forEach(item => console.log(item));

  // Timing tips
  console.log('\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('⏰ BEST TIMES TO POST');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  console.log('Twitter:');
  console.log('• 8-10 AM EST (morning scroll)');
  console.log('• 12-1 PM EST (lunch break)');
  console.log('• 5-6 PM EST (evening commute)');
  console.log('');
  console.log('LinkedIn:');
  console.log('• 7-9 AM EST (start of workday)');
  console.log('• 12-1 PM EST (lunch)');
  console.log('• Tuesday-Thursday (best days)');

  console.log('\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('💡 VIRALITY HACKS');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const hacks = [
    '1. Reply to your own thread immediately (starts engagement)',
    '2. Ask a question at the end (triggers replies)',
    '3. Tag 1-2 relevant bigger accounts (not spammy)',
    '4. Share in relevant Discord/Slack communities',
    '5. Cross-post to Reddit (different format)',
    '6. Like + reply to every comment in first hour',
    '7. Quote tweet your own thread after 2 hours',
    '8. Add to newsletter/blog after 24 hours'
  ];

  hacks.forEach(hack => console.log(hack));

  console.log('\n\n🚀 GO CREATE AND MONETIZE!\n');

  rl.close();
}

function generateContent(formula, topic, credibility) {
  const twitterTemplates = {
    1: `I analyzed [number] ${topic} and found [X] patterns that actually work.

Here's what I discovered: 🧵

1/ [First insight]

2/ [Second insight]

3/ [Third insight]

4/ [Fourth insight]

5/ [Fifth insight]

Want the full breakdown with examples?

I created a detailed guide with all the data.

Link in bio 👆`,

    2: `How I went from [starting point] to ${credibility} with ${topic}.

Full breakdown: 🧵

1/ Where I started:
[Describe humble beginnings]

2/ The turning point:
[What changed everything]

3/ What actually worked:
[Strategy that made the difference]

4/ What didn't work:
[Failed attempts - builds credibility]

5/ Where I am now:
${credibility}

6/ What I'd do differently:
[Hindsight wisdom]

Want my full playbook?

I put everything in a guide. Link in bio.`,

    7: `Here's exactly how I ${credibility} with ${topic}.

No BS, just the actual process: 🧵

1/ The Setup (Week 1)
[What you did to prepare]

2/ The Strategy (Week 2-4)
[Your approach]

3/ The Execution (Month 2)
[How you did it]

4/ The Results
${credibility}

5/ The Tools I Used
[List 3-5 tools]

6/ What I'd Do Differently
[Lessons learned]

Full breakdown with screenshots and templates in my guide.

Link in bio.`
  };

  const linkedinTemplate = `I want to share something I learned about ${topic}.

After ${credibility}, here's what actually matters:

→ [Key point 1]
→ [Key point 2]
→ [Key point 3]
→ [Key point 4]
→ [Key point 5]

The biggest surprise?

[Counterintuitive insight]

If you're working on ${topic}, these insights will save you months of trial and error.

I've documented everything in a detailed guide (link in comments).

What's been your experience with ${topic}?`;

  return {
    twitter: twitterTemplates[1] || twitterTemplates[7],
    linkedin: linkedinTemplate
  };
}

function generateMonetizationGuide(method, topic, credibility) {
  if (method.name === 'Gumroad Product in Bio') {
    return `GUMROAD QUICK SETUP:

1. Go to: https://gumroad.com
2. Click "Create Product"
3. Product name: "${topic} - Complete Guide"
4. Description:

   "Everything I learned ${credibility}.

   Includes:
   • Full breakdown of my process
   • Templates and checklists
   • Tools and resources
   • Common mistakes to avoid
   • Quick-start guide

   Save months of trial and error. Get results faster."

5. Price: $9.99 (flash sale) or $19.99
6. Upload your PDF/templates
7. Get product URL
8. Update Twitter bio: "Free thread 👇 | Full guide 👉 [link]"

Create the guide:
- Expand on thread points
- Add screenshots/examples
- Include templates/checklist
- 10-15 pages PDF
- Time needed: 30-45 minutes`;
  }

  if (method.name === 'DM for Full Guide') {
    return `DM-TO-PAY SETUP:

1. Add to your final thread tweet:
   "DM me 'GUIDE' for the full breakdown with templates"

2. When someone DMs:
   "Hey! The complete guide is $${topic.includes('template') ? '9.99' : '19.99'}.

   You'll get:
   • [Benefit 1]
   • [Benefit 2]
   • [Benefit 3]

   Payment: [Gumroad link or PayPal.me link]

   I'll send it over immediately after payment!"

3. After payment:
   Send PDF via DM or email

4. Set up auto-responder (optional):
   Use Twitter automation tools or just respond manually

Conversion rate: ~10-20% of DMs convert
If you get 50 DMs, that's 5-10 sales = $50-200`;
  }

  return `Follow the setup instructions for ${method.name} above!`;
}

main().catch(console.error);
