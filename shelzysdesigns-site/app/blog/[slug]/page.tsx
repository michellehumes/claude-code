import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

interface BlogPost {
  title: string;
  date: string;
  category: string;
  excerpt: string;
  content: string;
}

const posts: Record<string, BlogPost> = {
  "best-budget-spreadsheet-templates-2026": {
    title: "Best Budget Spreadsheet Templates for 2026",
    date: "March 15, 2026",
    category: "Budget & Finance",
    excerpt:
      "Take control of your finances with these top-rated budget spreadsheet templates.",
    content: `
      <p>Managing your money shouldn't be complicated. Whether you're paying off debt, saving for a big purchase, or just trying to understand where your paycheck goes, a good budget spreadsheet is the foundation of financial wellness.</p>

      <h2>Why Use a Budget Spreadsheet?</h2>
      <p>Apps come and go, but a spreadsheet gives you full control over your data. You can customize categories, add your own formulas, and see everything at a glance — no subscription fees required.</p>

      <h2>Top Budget Templates to Try</h2>

      <h3>1. Zero-Based Budget Template</h3>
      <p>The zero-based budgeting method assigns every dollar a job. This template includes pre-built categories for housing, food, transportation, and savings, with automatic calculations that ensure your income minus expenses equals zero.</p>

      <h3>2. 50/30/20 Budget Tracker</h3>
      <p>Based on the popular 50/30/20 rule — 50% needs, 30% wants, 20% savings — this template automatically categorizes your spending and shows a visual breakdown of where your money goes each month.</p>

      <h3>3. Annual Budget Overview Dashboard</h3>
      <p>See your entire year at a glance. This template tracks monthly income and expenses across 12 months, with built-in charts showing trends, savings rate, and progress toward annual financial goals.</p>

      <h3>4. Debt Payoff Tracker</h3>
      <p>If you're tackling debt, this template helps you compare the avalanche and snowball methods. Enter your balances, interest rates, and minimum payments, and it calculates your payoff timeline and total interest saved.</p>

      <h2>Tips for Sticking to Your Budget</h2>
      <ul>
        <li>Update your spreadsheet weekly — consistency is key</li>
        <li>Round up expenses to build a small buffer</li>
        <li>Review and adjust categories monthly</li>
        <li>Celebrate milestones like hitting savings goals</li>
      </ul>

      <p>Ready to take control of your finances? Browse our <a href="/collections/budget-finance">budget and finance templates</a> to find the perfect match for your money goals.</p>
    `,
  },
  "best-wedding-planning-spreadsheet-templates": {
    title: "Best Wedding Planning Spreadsheet Templates",
    date: "March 10, 2026",
    category: "Wedding",
    excerpt:
      "Planning a wedding doesn't have to be overwhelming. These spreadsheet templates cover everything you need.",
    content: `
      <p>Wedding planning involves hundreds of decisions, dozens of vendors, and a budget that needs careful tracking. A well-organized spreadsheet can be your best friend through the entire process.</p>

      <h2>Essential Wedding Planning Spreadsheets</h2>

      <h3>1. Wedding Budget Tracker</h3>
      <p>The average wedding costs tens of thousands of dollars, and expenses can spiral quickly without tracking. A wedding budget spreadsheet breaks down costs by category — venue, catering, flowers, photography, attire, and more — with columns for estimated vs. actual spending.</p>

      <h3>2. Guest List Manager</h3>
      <p>Keep track of invitations sent, RSVPs received, meal preferences, plus-ones, and table assignments. A good guest list spreadsheet saves hours of back-and-forth and prevents the dreaded double-invite.</p>

      <h3>3. Vendor Contact Sheet</h3>
      <p>Store all your vendor details in one place: names, phone numbers, emails, contract dates, deposit amounts, and payment schedules. Never lose track of who you've booked or what you owe.</p>

      <h3>4. Wedding Timeline Planner</h3>
      <p>From 12 months out to the day-of schedule, a timeline template keeps you on track. It breaks the planning process into manageable monthly tasks so nothing falls through the cracks.</p>

      <h2>Why Spreadsheets Beat Wedding Apps</h2>
      <ul>
        <li>No monthly subscription fees</li>
        <li>Fully customizable to your wedding style</li>
        <li>Easy to share with your partner and wedding party</li>
        <li>Works offline — no app crashes on your big day</li>
      </ul>

      <p>Check out our <a href="/collections/wedding">wedding planning templates</a> to find everything you need for your big day.</p>
    `,
  },
  "adhd-planner-templates-adults": {
    title: "ADHD Planner Templates for Adults",
    date: "March 5, 2026",
    category: "Planners",
    excerpt:
      "Designed with neurodivergent brains in mind, these planner templates help adults with ADHD stay on track.",
    content: `
      <p>Traditional planners aren't always designed for how ADHD brains work. Overwhelming layouts, tiny boxes, and rigid structures can actually make it harder to stay organized. That's why ADHD-friendly planner templates are a game-changer.</p>

      <h2>What Makes a Planner ADHD-Friendly?</h2>
      <ul>
        <li><strong>Visual cues:</strong> Color coding and icons help your brain quickly identify priorities</li>
        <li><strong>Simplified layouts:</strong> Less clutter means less overwhelm</li>
        <li><strong>Flexible structure:</strong> No guilt-inducing daily schedules — focus on what matters</li>
        <li><strong>Built-in rewards:</strong> Habit trackers and progress bars provide dopamine hits</li>
        <li><strong>Brain dump sections:</strong> Capture random thoughts before they disappear</li>
      </ul>

      <h2>Best ADHD Planner Templates</h2>

      <h3>1. Weekly Focus Planner</h3>
      <p>Instead of hour-by-hour schedules, this planner uses a "top 3 priorities" approach. Pick your three most important tasks each day, and everything else is bonus. Includes a weekly reflection section to celebrate wins.</p>

      <h3>2. Habit Tracker with Visual Progress</h3>
      <p>A colorful, satisfying habit tracker that fills in as you complete tasks. The visual progress is incredibly motivating for ADHD brains that thrive on immediate feedback.</p>

      <h3>3. Brain Dump to Action Plan</h3>
      <p>Start with a messy brain dump, then use the built-in sorting system to organize thoughts into actionable tasks, future ideas, and things to delegate. Perfect for those moments when everything feels urgent.</p>

      <h2>Tips for Using Planners with ADHD</h2>
      <ul>
        <li>Keep it simple — don't try to track everything at once</li>
        <li>Use it at the same time each day to build the habit</li>
        <li>Forgive missed days — just pick up where you left off</li>
        <li>Pair planning with something enjoyable (music, coffee, etc.)</li>
      </ul>

      <p>Browse our <a href="/collections/planners">planner templates</a> to find one that works with your brain, not against it.</p>
    `,
  },
  "small-business-planner-spreadsheet": {
    title: "Small Business Planner Spreadsheet Guide",
    date: "February 28, 2026",
    category: "Business",
    excerpt:
      "Run your small business like a pro with these all-in-one planner spreadsheets.",
    content: `
      <p>Running a small business means wearing a lot of hats. Between managing finances, tracking inventory, following up with clients, and planning for growth, it's easy to lose track of the big picture. A well-designed business planner spreadsheet keeps everything organized in one place.</p>

      <h2>What to Track in Your Business Planner</h2>

      <h3>1. Revenue & Expense Tracking</h3>
      <p>Log every dollar in and out. Categorize income by source (products, services, affiliates) and expenses by type (materials, marketing, software, shipping). Monthly and yearly summaries help you spot trends and make smarter decisions.</p>

      <h3>2. Client & Order Management</h3>
      <p>Keep a running list of clients, order details, delivery dates, and payment status. Never miss a follow-up or forget an outstanding invoice again.</p>

      <h3>3. Inventory Tracker</h3>
      <p>If you sell physical or digital products, tracking inventory prevents overselling and helps you plan restocks. Include columns for SKU, quantity on hand, reorder point, and supplier info.</p>

      <h3>4. Goal Setting & KPIs</h3>
      <p>Set quarterly goals and track key performance indicators like revenue growth, customer acquisition cost, and conversion rates. Having these numbers visible keeps you focused on what moves the needle.</p>

      <h2>Why Spreadsheets Work for Small Business</h2>
      <ul>
        <li>No expensive software subscriptions needed</li>
        <li>Fully customizable to your specific business model</li>
        <li>Easy to share with business partners or accountants</li>
        <li>Portable — access from any device via Google Sheets</li>
      </ul>

      <p>Explore our <a href="/collections/business">business templates</a> to find the right tools for your growing business.</p>
    `,
  },
  "etsy-seller-dashboard-templates": {
    title: "Etsy Seller Dashboard Templates",
    date: "February 20, 2026",
    category: "Business",
    excerpt:
      "Monitor your Etsy shop performance with purpose-built dashboard templates.",
    content: `
      <p>Etsy's built-in analytics are helpful, but they don't give you the full picture. A dedicated seller dashboard spreadsheet lets you track the metrics that matter most to your shop's growth and profitability.</p>

      <h2>Key Metrics Every Etsy Seller Should Track</h2>

      <h3>1. Sales & Revenue</h3>
      <p>Track daily, weekly, and monthly sales. Break down revenue by product to identify your bestsellers and underperformers. Knowing which products drive your income helps you focus your energy where it counts.</p>

      <h3>2. Fees & Profit Margins</h3>
      <p>Etsy fees can eat into your profits if you're not careful. Track listing fees, transaction fees, payment processing fees, and advertising costs. Calculate your true profit margin per product — you might be surprised which items are actually most profitable.</p>

      <h3>3. Traffic & Conversion</h3>
      <p>Monitor your shop views, listing views, and conversion rate. If you're getting traffic but no sales, your listings might need better photos or descriptions. If traffic is low, it's time to work on SEO or marketing.</p>

      <h3>4. Inventory & Restocking</h3>
      <p>For shops with physical products or limited digital bundles, track inventory levels and set reorder alerts. Running out of stock means lost sales and lower search ranking.</p>

      <h2>Building Your Dashboard</h2>
      <p>A great Etsy dashboard combines all these metrics on a single overview page with charts and conditional formatting. At a glance, you can see:</p>
      <ul>
        <li>This month's revenue vs. last month</li>
        <li>Top 5 bestselling products</li>
        <li>Profit after all fees</li>
        <li>Conversion rate trend</li>
        <li>Upcoming tasks and deadlines</li>
      </ul>

      <p>Ready to level up your Etsy business? Check out our <a href="/collections/business">Etsy seller templates</a> designed specifically for handmade and digital product shops.</p>
    `,
  },
};

export async function generateStaticParams() {
  return Object.keys(posts).map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const post = posts[slug];
  if (!post) return {};
  return {
    title: `${post.title} | Shelzy's Designs`,
    description: post.excerpt,
  };
}

export default async function BlogPostPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = posts[slug];

  if (!post) {
    notFound();
  }

  return (
    <>
      {/* Hero */}
      <section className="bg-light-gray py-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <span className="text-sm font-medium text-pink uppercase tracking-wide">
              {post.category}
            </span>
            <span className="text-sm text-text-light">{post.date}</span>
          </div>
          <h1 className="font-heading text-3xl md:text-4xl font-bold text-charcoal max-w-3xl mx-auto">
            {post.title}
          </h1>
        </div>
      </section>

      {/* Content */}
      <section className="py-16">
        <div className="max-w-[800px] mx-auto px-4">
          <div
            className="prose prose-lg max-w-none text-text-light [&_h2]:font-heading [&_h2]:text-charcoal [&_h2]:text-2xl [&_h2]:font-bold [&_h2]:mt-8 [&_h2]:mb-4 [&_h3]:font-heading [&_h3]:text-charcoal [&_h3]:text-xl [&_h3]:font-semibold [&_h3]:mt-6 [&_h3]:mb-2 [&_p]:mb-4 [&_p]:leading-relaxed [&_ul]:mb-4 [&_ul]:list-disc [&_ul]:pl-6 [&_li]:mb-2 [&_a]:text-pink [&_a]:underline [&_strong]:text-charcoal"
            dangerouslySetInnerHTML={{ __html: post.content }}
          />

          <div className="mt-12 pt-8 border-t border-mid-gray">
            <Link
              href="/blog"
              className="text-pink font-medium hover:underline"
            >
              &larr; Back to Blog
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
