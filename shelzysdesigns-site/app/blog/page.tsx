import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Blog | Shelzy's Designs",
  description:
    "Tips, guides, and reviews on the best digital templates, planners, and spreadsheets for budgeting, wedding planning, business, and productivity.",
};

const posts = [
  {
    slug: "best-budget-spreadsheet-templates-2026",
    title: "Best Budget Spreadsheet Templates for 2026",
    excerpt:
      "Take control of your finances with these top-rated budget spreadsheet templates. From zero-based budgeting to the 50/30/20 method, find the perfect template for your money goals.",
    date: "March 15, 2026",
    category: "Budget & Finance",
  },
  {
    slug: "best-wedding-planning-spreadsheet-templates",
    title: "Best Wedding Planning Spreadsheet Templates",
    excerpt:
      "Planning a wedding doesn't have to be overwhelming. These spreadsheet templates cover everything from budget tracking to guest lists, vendor management, and day-of timelines.",
    date: "March 10, 2026",
    category: "Wedding",
  },
  {
    slug: "adhd-planner-templates-adults",
    title: "ADHD Planner Templates for Adults",
    excerpt:
      "Designed with neurodivergent brains in mind, these planner templates use visual cues, simplified layouts, and flexible structures to help adults with ADHD stay on track.",
    date: "March 5, 2026",
    category: "Planners",
  },
  {
    slug: "small-business-planner-spreadsheet",
    title: "Small Business Planner Spreadsheet Guide",
    excerpt:
      "Run your small business like a pro with these all-in-one planner spreadsheets. Track revenue, expenses, inventory, clients, and goals in one organized dashboard.",
    date: "February 28, 2026",
    category: "Business",
  },
  {
    slug: "etsy-seller-dashboard-templates",
    title: "Etsy Seller Dashboard Templates",
    excerpt:
      "Monitor your Etsy shop performance with purpose-built dashboard templates. Track sales, fees, profit margins, and bestsellers to grow your handmade business.",
    date: "February 20, 2026",
    category: "Business",
  },
];

export default function BlogPage() {
  return (
    <>
      {/* Hero */}
      <section className="bg-light-gray py-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="font-heading text-4xl md:text-5xl font-bold text-charcoal mb-4">
            Blog
          </h1>
          <p className="text-text-light text-lg max-w-2xl mx-auto">
            Tips, guides, and template reviews to help you get more organized and productive.
          </p>
        </div>
      </section>

      {/* Posts */}
      <section className="py-16">
        <div className="max-w-[800px] mx-auto px-4">
          <div className="space-y-8">
            {posts.map((post) => (
              <article
                key={post.slug}
                className="border border-mid-gray rounded-xl p-6 hover:border-pink hover:shadow-md transition-all"
              >
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-xs font-medium text-pink uppercase tracking-wide">
                    {post.category}
                  </span>
                  <span className="text-xs text-text-light">{post.date}</span>
                </div>
                <Link href={`/blog/${post.slug}`}>
                  <h2 className="font-heading text-xl font-bold text-charcoal hover:text-pink transition-colors mb-2">
                    {post.title}
                  </h2>
                </Link>
                <p className="text-text-light leading-relaxed">{post.excerpt}</p>
                <Link
                  href={`/blog/${post.slug}`}
                  className="inline-block mt-3 text-pink font-medium hover:underline"
                >
                  Read More
                </Link>
              </article>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
