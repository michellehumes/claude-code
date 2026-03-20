import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "FAQ | Shelzy's Designs",
  description:
    "Frequently asked questions about Shelzy's Designs digital templates, planners, and trackers. Learn about downloads, compatibility, refunds, and more.",
};

const faqSections = [
  {
    title: "Ordering & Downloads",
    items: [
      {
        q: "How do I download my template after purchasing?",
        a: "After completing your purchase on Etsy, you'll receive a download link immediately. You can also access your files anytime from your Etsy account under Purchases & Reviews.",
      },
      {
        q: "What file formats do your templates come in?",
        a: "Most of our templates are Google Sheets files. Some products also include Excel (.xlsx) versions. The file format is always listed in the product description.",
      },
      {
        q: "Can I use the template more than once?",
        a: "Yes! Once you download a template, you can make as many copies as you need for personal use. Simply duplicate the file in Google Drive to start fresh.",
      },
      {
        q: "Do I need to install any software?",
        a: "No installation required. Our Google Sheets templates work right in your browser. All you need is a free Google account.",
      },
      {
        q: "How long do I have access to my downloads?",
        a: "Forever! Once purchased, the template is yours to keep. You can re-download it from your Etsy account at any time.",
      },
      {
        q: "Can I buy templates as a gift for someone else?",
        a: "Absolutely! After purchasing, you can share the Google Sheets link with the recipient. Just make sure they make their own copy so they can edit it.",
      },
    ],
  },
  {
    title: "Compatibility",
    items: [
      {
        q: "Do the templates work on mobile devices?",
        a: "Yes, all our Google Sheets templates work on mobile through the Google Sheets app (iOS and Android). However, we recommend using a computer or tablet for the best editing experience.",
      },
      {
        q: "Are the templates compatible with Excel?",
        a: "Many of our templates include an Excel version. Google Sheets templates can also be downloaded as .xlsx files, though some formatting may differ slightly.",
      },
      {
        q: "Do I need a Google account to use the templates?",
        a: "Yes, a free Google account is required to use Google Sheets templates. If you prefer Excel, check the product listing for Excel-compatible versions.",
      },
    ],
  },
  {
    title: "Refunds & Policies",
    items: [
      {
        q: "What is your refund policy?",
        a: "Because these are digital products with instant access, we generally do not offer refunds. However, if you experience a technical issue, please contact us and we'll make it right.",
      },
      {
        q: "Can I customize the templates?",
        a: "Yes! All templates are fully editable. You can change colors, add or remove sections, and adjust formulas to fit your needs. Each template includes instructions to help you get started.",
      },
      {
        q: "Can I resell or redistribute the templates?",
        a: "No. Our templates are for personal use only. You may not resell, share publicly, or redistribute them in any form. Commercial licenses are not currently available.",
      },
    ],
  },
  {
    title: "About Shelzy's Designs",
    items: [
      {
        q: "Who is behind Shelzy's Designs?",
        a: "Shelzy's Designs is a small, independent shop creating beautiful and functional digital templates. Every product is designed with care to help you stay organized and reach your goals.",
      },
      {
        q: "How often do you release new templates?",
        a: "We release new templates regularly — usually 2-4 new products per month. Follow us on Instagram or join our email list to be the first to know about new drops.",
      },
      {
        q: "Do you take custom template requests?",
        a: "We love hearing what our customers need! While we can't guarantee every request, we use your feedback to guide future products. Send us a message on Etsy with your ideas.",
      },
      {
        q: "How can I contact you for support?",
        a: "The best way to reach us is through Etsy messages on our shop page. We typically respond within 24 hours. You can also reach out via Instagram DM.",
      },
    ],
  },
];

// Build JSON-LD structured data for all FAQ items
const allFaqItems = faqSections.flatMap((section) => section.items);
const faqJsonLd = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: allFaqItems.map((item) => ({
    "@type": "Question",
    name: item.q,
    acceptedAnswer: {
      "@type": "Answer",
      text: item.a,
    },
  })),
};

export default function FAQPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
      />

      {/* Hero */}
      <section className="bg-light-gray py-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="font-heading text-4xl md:text-5xl font-bold text-charcoal mb-4">
            Frequently Asked Questions
          </h1>
          <p className="text-text-light text-lg max-w-2xl mx-auto">
            Everything you need to know about our digital templates, downloads, and policies.
          </p>
        </div>
      </section>

      {/* FAQ Content */}
      <section className="py-16">
        <div className="max-w-[800px] mx-auto px-4">
          {faqSections.map((section) => (
            <div key={section.title} className="mb-12">
              <h2 className="font-heading text-2xl font-bold text-charcoal mb-6 pb-2 border-b border-mid-gray">
                {section.title}
              </h2>
              <div className="space-y-6">
                {section.items.map((item) => (
                  <div key={item.q}>
                    <h3 className="font-heading text-lg font-semibold text-charcoal mb-2">
                      {item.q}
                    </h3>
                    <p className="text-text-light leading-relaxed">{item.a}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
