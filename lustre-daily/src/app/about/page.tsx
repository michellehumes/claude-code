import { Metadata } from "next";
import { siteConfig } from "@/site.config";
import Link from "next/link";

export const metadata: Metadata = {
  title: "About Us",
  description: `Learn about ${siteConfig.name} - your trusted source for beauty tips, product reviews, and the latest trends in makeup, hair, and skincare.`,
};

export default function AboutPage() {
  return (
    <div className="animate-fade-in">
      {/* Hero */}
      <section className="bg-gradient-to-br from-pink-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-purple-950/20">
        <div className="mx-auto max-w-4xl px-4 py-16 sm:px-6 lg:px-8">
          <h1 className="text-center text-4xl font-bold text-gray-900 dark:text-white sm:text-5xl">
            About {siteConfig.name}
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-center text-lg text-gray-600 dark:text-gray-400">
            Your trusted guide to discovering the best in beauty
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="prose prose-lg max-w-none dark:prose-invert">
          <h2>Our Story</h2>
          <p>
            {siteConfig.name} was born from a simple belief: everyone deserves access to honest, expert beauty advice without the fluff. We&apos;re passionate about helping you discover products that actually work and trends that suit your unique style.
          </p>

          <h2>What We Do</h2>
          <p>
            We research, test, and curate the best beauty products across makeup, skincare, and hair care. Our team stays on top of the latest trends, ingredient innovations, and industry news so you don&apos;t have to.
          </p>
          <p>
            Whether you&apos;re looking for the perfect everyday foundation, searching for solutions for specific skin concerns, or just want to stay inspired by the latest beauty trends, we&apos;ve got you covered.
          </p>

          <h2>Our Approach</h2>
          <ul>
            <li>
              <strong>Honest Reviews:</strong> We tell it like it is. If a product doesn&apos;t deliver, we&apos;ll let you know.
            </li>
            <li>
              <strong>Research-Backed:</strong> We dive deep into ingredients, formulations, and the science behind beauty products.
            </li>
            <li>
              <strong>Inclusive Beauty:</strong> Beauty comes in all forms. We celebrate diversity and recommend products for all skin types, tones, and concerns.
            </li>
            <li>
              <strong>Value-Conscious:</strong> Great beauty doesn&apos;t have to break the bank. We feature products at every price point.
            </li>
          </ul>

          <h2>Transparency</h2>
          <p>
            We believe in full transparency. When you click on product links on our site, we may earn a commission from Amazon at no extra cost to you. This helps us keep creating the content you love. Learn more in our{" "}
            <Link href="/affiliate-disclosure">Affiliate Disclosure</Link>.
          </p>
          <p>
            Our editorial opinions are our own. We never let affiliate partnerships influence our recommendations. If we feature a product, it&apos;s because we genuinely think it&apos;s worth your attention.
          </p>

          <h2>Join Our Community</h2>
          <p>
            Beauty is more fun together! Follow us on social media for daily inspiration, behind-the-scenes content, and community discussions:
          </p>
          <ul>
            <li>
              <a href={siteConfig.social.instagram} target="_blank" rel="noopener noreferrer">
                Instagram
              </a>
            </li>
            <li>
              <a href={siteConfig.social.pinterest} target="_blank" rel="noopener noreferrer">
                Pinterest
              </a>
            </li>
            <li>
              <a href={siteConfig.social.tiktok} target="_blank" rel="noopener noreferrer">
                TikTok
              </a>
            </li>
          </ul>

          <h2>Get in Touch</h2>
          <p>
            Have questions, suggestions, or just want to say hi? We&apos;d love to hear from you!{" "}
            <Link href="/contact">Contact us</Link>.
          </p>
        </div>
      </section>
    </div>
  );
}
