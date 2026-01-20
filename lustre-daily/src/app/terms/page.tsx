import { Metadata } from "next";
import { siteConfig } from "@/site.config";

export const metadata: Metadata = {
  title: "Terms of Use",
  description: `Terms of use for ${siteConfig.name}. By using our website, you agree to these terms and conditions.`,
};

export default function TermsPage() {
  return (
    <div className="animate-fade-in">
      <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white sm:text-4xl">
          Terms of Use
        </h1>
        <p className="mt-4 text-sm text-gray-500 dark:text-gray-400">
          Last updated: {new Date().toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}
        </p>

        <div className="prose prose-lg mt-8 max-w-none dark:prose-invert">
          <h2>Acceptance of Terms</h2>
          <p>
            By accessing and using {siteConfig.name}, you accept and agree to be bound by these Terms of Use. If you do not agree to these terms, please do not use our website.
          </p>

          <h2>Use of Content</h2>
          <p>
            All content on {siteConfig.name}, including text, images, graphics, and videos, is protected by copyright and other intellectual property laws. You may not:
          </p>
          <ul>
            <li>Copy, reproduce, or distribute our content without permission</li>
            <li>Use our content for commercial purposes without authorization</li>
            <li>Modify or create derivative works from our content</li>
          </ul>
          <p>
            You may share our content through social media using the sharing features provided, with proper attribution.
          </p>

          <h2>Affiliate Disclosure</h2>
          <p>
            {siteConfig.name} participates in affiliate programs, including the Amazon Services LLC Associates Program. When you click on affiliate links and make purchases, we may earn commissions. See our <a href="/affiliate-disclosure">Affiliate Disclosure</a> for more details.
          </p>

          <h2>Product Recommendations</h2>
          <p>
            Our product recommendations are based on our research and opinions. Individual results may vary. We recommend researching products thoroughly before purchasing. We do not guarantee product performance or suitability for your specific needs.
          </p>

          <h2>No Medical Advice</h2>
          <p>
            Content on {siteConfig.name} is for informational purposes only and should not be considered medical advice. For skincare concerns, allergies, or health conditions, please consult a qualified healthcare professional or dermatologist.
          </p>

          <h2>User Conduct</h2>
          <p>When using our website, you agree not to:</p>
          <ul>
            <li>Violate any applicable laws or regulations</li>
            <li>Post harmful, offensive, or misleading content</li>
            <li>Attempt to gain unauthorized access to our systems</li>
            <li>Interfere with other users&apos; enjoyment of the website</li>
          </ul>

          <h2>External Links</h2>
          <p>
            Our website contains links to third-party websites, including Amazon.com. We are not responsible for the content, privacy practices, or terms of these external sites.
          </p>

          <h2>Disclaimer of Warranties</h2>
          <p>
            {siteConfig.name} is provided &quot;as is&quot; without warranties of any kind. We do not guarantee the accuracy, completeness, or timeliness of our content.
          </p>

          <h2>Limitation of Liability</h2>
          <p>
            {siteConfig.name} shall not be liable for any damages arising from the use of our website or reliance on our content.
          </p>

          <h2>Changes to Terms</h2>
          <p>
            We reserve the right to modify these terms at any time. Continued use of the website after changes constitutes acceptance of the new terms.
          </p>

          <h2>Contact</h2>
          <p>
            Questions about these terms? <a href="/contact">Contact us</a>.
          </p>
        </div>
      </div>
    </div>
  );
}
