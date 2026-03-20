import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

interface Product {
  name: string;
  description: string;
  price: string;
  etsyUrl: string;
}

interface Collection {
  title: string;
  description: string;
  products: Product[];
}

const ETSY_SHOP = "https://www.etsy.com/shop/ShelzysDesignsStore";

const collections: Record<string, Collection> = {
  templates: {
    title: "Templates",
    description:
      "Ready-to-use digital spreadsheet templates for every area of your life. From budgeting to meal planning, just download, duplicate, and start using.",
    products: [
      { name: "Budget Tracker Spreadsheet", description: "Track income, expenses, and savings goals with automatic calculations and visual charts.", price: "$0.90", etsyUrl: ETSY_SHOP },
      { name: "Meal Planning Template", description: "Plan your weekly meals, generate grocery lists, and track nutrition all in one place.", price: "$0.69", etsyUrl: ETSY_SHOP },
      { name: "Habit Tracker Template", description: "Build better habits with daily tracking, streaks, and monthly progress reports.", price: "$0.69", etsyUrl: ETSY_SHOP },
      { name: "Goal Setting Worksheet", description: "Break big goals into actionable steps with timelines, milestones, and accountability check-ins.", price: "$0.69", etsyUrl: ETSY_SHOP },
    ],
  },
  planners: {
    title: "Planners",
    description:
      "Digital planners designed to keep you organized and productive. Perfect for daily planning, weekly reviews, and long-term goal tracking.",
    products: [
      { name: "ADHD-Friendly Weekly Planner", description: "Simplified layout with visual cues, top-3 priorities, and brain dump sections designed for neurodivergent minds.", price: "$0.69", etsyUrl: ETSY_SHOP },
      { name: "Daily Planner Template", description: "Structure your day with time blocks, task lists, and gratitude prompts.", price: "$0.69", etsyUrl: ETSY_SHOP },
      { name: "Weekly Review Planner", description: "Reflect on your week, celebrate wins, and set intentions for the week ahead.", price: "$0.69", etsyUrl: ETSY_SHOP },
      { name: "Quarterly Goal Planner", description: "Map out 90-day goals with monthly milestones and weekly action items.", price: "$0.90", etsyUrl: ETSY_SHOP },
    ],
  },
  wedding: {
    title: "Wedding",
    description:
      "Everything you need to plan your dream wedding. Budget trackers, guest list managers, vendor contacts, and day-of timelines.",
    products: [
      { name: "Wedding Planner Dashboard", description: "All-in-one wedding planning spreadsheet with budget, guest list, vendor tracking, and timeline.", price: "$0.90", etsyUrl: ETSY_SHOP },
      { name: "Bachelorette Party Planner", description: "Plan the ultimate bach party with guest lists, activities, itineraries, and budget tracking.", price: "$0.69", etsyUrl: ETSY_SHOP },
      { name: "Bridal Shower Planner", description: "Everything you need for the perfect shower — games, decor checklist, menu planning, and RSVPs.", price: "$0.69", etsyUrl: ETSY_SHOP },
      { name: "Wedding Guest List Manager", description: "Track invitations, RSVPs, meal preferences, plus-ones, and table assignments.", price: "$0.69", etsyUrl: ETSY_SHOP },
    ],
  },
  bundles: {
    title: "Bundles",
    description:
      "Get more for less with our curated template bundles. Each bundle combines our most popular templates at a discounted price.",
    products: [
      { name: "Ultimate Wedding Bundle", description: "Includes Wedding Planner Dashboard, Guest List Manager, Bachelorette Planner, and Bridal Shower Planner.", price: "$1.99", etsyUrl: ETSY_SHOP },
      { name: "Business Starter Bundle", description: "Small Business Planner, Etsy Seller Dashboard, and Client Manager — everything to launch your business.", price: "$1.99", etsyUrl: ETSY_SHOP },
      { name: "Life Organization Bundle", description: "Budget Tracker, Meal Planner, Habit Tracker, and Weekly Planner for a totally organized life.", price: "$1.99", etsyUrl: ETSY_SHOP },
      { name: "Planner Power Pack", description: "Daily Planner, Weekly Review, Quarterly Goals, and ADHD-Friendly Planner bundled together.", price: "$1.99", etsyUrl: ETSY_SHOP },
    ],
  },
  "budget-finance": {
    title: "Budget & Finance",
    description:
      "Take control of your money with spreadsheet templates for budgeting, debt payoff, savings tracking, and financial goal planning.",
    products: [
      { name: "Zero-Based Budget Template", description: "Assign every dollar a job with this comprehensive zero-based budgeting spreadsheet.", price: "$0.90", etsyUrl: ETSY_SHOP },
      { name: "50/30/20 Budget Tracker", description: "Automatically categorize spending into needs, wants, and savings using the popular 50/30/20 rule.", price: "$0.90", etsyUrl: ETSY_SHOP },
      { name: "Debt Payoff Tracker", description: "Compare avalanche and snowball methods. See your payoff timeline and total interest saved.", price: "$0.69", etsyUrl: ETSY_SHOP },
      { name: "Savings Goal Tracker", description: "Set savings targets, track contributions, and watch your progress with visual charts.", price: "$0.69", etsyUrl: ETSY_SHOP },
    ],
  },
  business: {
    title: "Business",
    description:
      "Tools for entrepreneurs, freelancers, and Etsy sellers. Track revenue, manage clients, monitor shop analytics, and plan for growth.",
    products: [
      { name: "Etsy Seller Dashboard", description: "Track sales, fees, profit margins, and bestsellers. Built specifically for Etsy shop owners.", price: "$0.90", etsyUrl: ETSY_SHOP },
      { name: "Small Business Planner", description: "All-in-one business management spreadsheet with revenue tracking, client management, and goal setting.", price: "$0.90", etsyUrl: ETSY_SHOP },
      { name: "Freelancer Invoice Tracker", description: "Track clients, invoices, payments, and outstanding balances. Never chase a late payment again.", price: "$0.69", etsyUrl: ETSY_SHOP },
      { name: "Social Media Content Calendar", description: "Plan and schedule social media posts across platforms with content ideas and analytics tracking.", price: "$0.69", etsyUrl: ETSY_SHOP },
    ],
  },
};

export async function generateStaticParams() {
  return Object.keys(collections).map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const collection = collections[slug];
  if (!collection) return {};
  return {
    title: `${collection.title} | Shelzy's Designs`,
    description: collection.description,
  };
}

export default async function CollectionPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const collection = collections[slug];

  if (!collection) {
    notFound();
  }

  return (
    <>
      {/* Hero */}
      <section className="bg-light-gray py-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="font-heading text-4xl md:text-5xl font-bold text-charcoal mb-4">
            {collection.title}
          </h1>
          <p className="text-text-light text-lg max-w-2xl mx-auto">
            {collection.description}
          </p>
        </div>
      </section>

      {/* Products */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {collection.products.map((product) => (
              <div
                key={product.name}
                className="bg-white border border-mid-gray rounded-xl p-6 flex flex-col"
              >
                <h3 className="font-heading text-lg font-semibold text-charcoal mb-2">
                  {product.name}
                </h3>
                <p className="text-text-light text-sm flex-1 mb-4">
                  {product.description}
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-charcoal">
                    {product.price}
                  </span>
                  <Link
                    href={product.etsyUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-pink text-white px-4 py-2 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity"
                  >
                    Shop on Etsy
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
