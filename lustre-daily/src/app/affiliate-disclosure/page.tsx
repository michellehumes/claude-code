import { Metadata } from "next";
import { siteConfig } from "@/site.config";
import { fullDisclosure } from "@/lib/affiliate";

export const metadata: Metadata = {
  title: "Affiliate Disclosure",
  description: `Learn about how ${siteConfig.name} earns commissions through affiliate partnerships with Amazon and other retailers.`,
};

export default function AffiliateDisclosurePage() {
  return (
    <div className="animate-fade-in">
      <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white sm:text-4xl">
          Affiliate Disclosure
        </h1>
        <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
          Transparency is important to us. Here&apos;s how we earn money and how it affects our recommendations.
        </p>

        <div className="prose prose-lg mt-8 max-w-none dark:prose-invert">
          <div className="whitespace-pre-line">{fullDisclosure}</div>

          <h2>How Affiliate Links Work</h2>
          <p>
            When you click on a product link on {siteConfig.name} and make a purchase on Amazon, we may earn a small commission at no additional cost to you. This commission helps us maintain and improve our website, allowing us to continue providing valuable beauty content.
          </p>

          <h2>Our Editorial Standards</h2>
          <p>
            Our product recommendations are based on our own research, testing, and expertise. We never let affiliate relationships influence our editorial content. If a product isn&apos;t worth recommending, we won&apos;t feature it regardless of potential earnings.
          </p>

          <h2>Price Accuracy</h2>
          <p>
            Product prices on Amazon change frequently. We do not guarantee that the prices shown on our site are accurate or up-to-date. Always check the current price on Amazon before making a purchase decision.
          </p>

          <h2>Questions?</h2>
          <p>
            If you have any questions about our affiliate relationships or disclosure practices, please <a href="/contact">contact us</a>.
          </p>
        </div>
      </div>
    </div>
  );
}
