import { Metadata } from "next";
import { siteConfig } from "@/site.config";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: `Privacy policy for ${siteConfig.name}. Learn how we collect, use, and protect your personal information.`,
};

export default function PrivacyPage() {
  return (
    <div className="animate-fade-in">
      <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white sm:text-4xl">
          Privacy Policy
        </h1>
        <p className="mt-4 text-sm text-gray-500 dark:text-gray-400">
          Last updated: {new Date().toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}
        </p>

        <div className="prose prose-lg mt-8 max-w-none dark:prose-invert">
          <h2>Information We Collect</h2>
          <p>
            {siteConfig.name} collects information you provide directly, such as when you subscribe to our newsletter or contact us. We also automatically collect certain information when you visit our website, including:
          </p>
          <ul>
            <li>Device and browser information</li>
            <li>IP address and general location</li>
            <li>Pages visited and time spent on site</li>
            <li>Referring website</li>
          </ul>

          <h2>How We Use Your Information</h2>
          <p>We use the information we collect to:</p>
          <ul>
            <li>Provide and improve our content</li>
            <li>Send newsletters and updates (if you&apos;ve subscribed)</li>
            <li>Analyze website traffic and usage patterns</li>
            <li>Respond to your inquiries</li>
          </ul>

          <h2>Cookies and Tracking</h2>
          <p>
            We use cookies and similar technologies to enhance your browsing experience, analyze traffic, and for marketing purposes. You can control cookies through your browser settings.
          </p>

          <h2>Third-Party Services</h2>
          <p>
            Our website may contain links to Amazon.com and other third-party websites. When you click on these links, you&apos;re subject to the privacy policies of those sites. We use Amazon Associates affiliate links to earn commissions from qualifying purchases.
          </p>

          <h2>Analytics</h2>
          <p>
            We may use analytics services like Google Analytics to understand how visitors use our website. These services may collect information about your visits to our site and other sites.
          </p>

          <h2>Data Security</h2>
          <p>
            We take reasonable measures to protect your personal information. However, no internet transmission is completely secure, and we cannot guarantee absolute security.
          </p>

          <h2>Your Rights</h2>
          <p>
            Depending on your location, you may have rights regarding your personal information, including access, correction, deletion, and data portability. Contact us to exercise these rights.
          </p>

          <h2>Children&apos;s Privacy</h2>
          <p>
            Our website is not directed to children under 13. We do not knowingly collect personal information from children.
          </p>

          <h2>Changes to This Policy</h2>
          <p>
            We may update this privacy policy from time to time. We&apos;ll notify you of significant changes by posting the new policy on this page.
          </p>

          <h2>Contact Us</h2>
          <p>
            If you have questions about this privacy policy, please <a href="/contact">contact us</a>.
          </p>
        </div>
      </div>
    </div>
  );
}
