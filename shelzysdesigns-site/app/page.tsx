import Link from "next/link";
import EmailCapture from "@/components/EmailCapture";

const featuredProducts = [
  { name: "Wedding Planner Dashboard", price: "$0.90", category: "Wedding", href: "/collections/wedding" },
  { name: "Budget Tracker Spreadsheet", price: "$0.90", category: "Finance", href: "/collections/budget-finance" },
  { name: "Etsy Seller Dashboard", price: "$0.90", category: "Business", href: "/collections/business" },
  { name: "ADHD Planner Template", price: "$0.69", category: "Planners", href: "/collections/planners" },
  { name: "Bachelorette Party Planner", price: "$0.69", category: "Wedding", href: "/collections/wedding" },
  { name: "Small Business Planner", price: "$0.90", category: "Business", href: "/collections/business" },
];

const collections = [
  { name: "Templates", description: "Ready-to-use spreadsheet templates", href: "/collections/templates" },
  { name: "Planners", description: "Daily, weekly & goal planners", href: "/collections/planners" },
  { name: "Wedding", description: "Everything for your big day", href: "/collections/wedding" },
  { name: "Bundles", description: "Best value multi-template packs", href: "/collections/bundles" },
  { name: "Budget & Finance", description: "Track spending & save more", href: "/collections/budget-finance" },
  { name: "Business", description: "Tools for entrepreneurs", href: "/collections/business" },
];

export default function Home() {
  return (
    <>
      {/* Hero */}
      <section className="bg-light-gray py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="font-heading text-4xl md:text-5xl font-bold text-charcoal mb-4">
            Digital Templates That Actually Make Life Easier
          </h1>
          <p className="text-text-light text-lg max-w-2xl mx-auto mb-8">
            Beautiful spreadsheets, planners, and trackers you can download instantly.
            Budget smarter, plan your wedding, or grow your business — all for under $1.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="https://www.etsy.com/shop/ShelzysDesignsStore"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-pink text-white px-8 py-3 rounded-lg font-medium hover:opacity-90 transition-opacity"
            >
              Shop All Templates
            </Link>
            <Link
              href="/collections/templates"
              className="border border-charcoal text-charcoal px-8 py-3 rounded-lg font-medium hover:bg-charcoal hover:text-white transition-colors"
            >
              Browse Collections
            </Link>
          </div>
        </div>
      </section>

      {/* Collections */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="font-heading text-3xl font-bold text-charcoal text-center mb-10">
            Shop by Category
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {collections.map((col) => (
              <Link
                key={col.name}
                href={col.href}
                className="border border-mid-gray rounded-xl p-6 hover:border-pink hover:shadow-md transition-all group"
              >
                <h3 className="font-heading text-xl font-semibold text-charcoal group-hover:text-pink transition-colors">
                  {col.name}
                </h3>
                <p className="text-text-light mt-1">{col.description}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="bg-light-gray py-16">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="font-heading text-3xl font-bold text-charcoal text-center mb-10">
            Popular Templates
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredProducts.map((product) => (
              <div
                key={product.name}
                className="bg-white rounded-xl p-6 border border-mid-gray"
              >
                <span className="text-xs font-medium text-pink uppercase tracking-wide">
                  {product.category}
                </span>
                <h3 className="font-heading text-lg font-semibold text-charcoal mt-2">
                  {product.name}
                </h3>
                <div className="flex items-center justify-between mt-4">
                  <span className="text-2xl font-bold text-charcoal">{product.price}</span>
                  <Link
                    href={product.href}
                    className="text-pink font-medium hover:underline"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Email Capture */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h2 className="font-heading text-3xl font-bold text-charcoal mb-3">
            Get Free Templates & Updates
          </h2>
          <p className="text-text-light mb-8 max-w-lg mx-auto">
            Join our list for exclusive freebies, new template drops, and planning tips delivered to your inbox.
          </p>
          <EmailCapture />
        </div>
      </section>
    </>
  );
}
