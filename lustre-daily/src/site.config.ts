// Site Configuration
// Change brand name and other settings here - this is the single source of truth

export const siteConfig = {
  // Brand
  name: "LustreDaily",
  tagline: "Your Daily Dose of Beauty Inspiration",
  description: "Discover the latest beauty trends, expert tips, and top-rated makeup, hair, and skincare products. Your trusted guide to looking and feeling your best.",

  // URLs
  url: process.env.NEXT_PUBLIC_SITE_URL || "https://lustredaily.com",

  // Amazon Affiliate
  amazonAssociateTag: process.env.AMAZON_ASSOC_TAG || "shelzysbeauty-20",

  // Social (placeholders)
  social: {
    instagram: "https://instagram.com/lustredaily",
    pinterest: "https://pinterest.com/lustredaily",
    tiktok: "https://tiktok.com/@lustredaily",
    twitter: "https://twitter.com/lustredaily",
  },

  // Categories
  categories: [
    { slug: "makeup", name: "Makeup", description: "Foundation to finishing touches - master your makeup game" },
    { slug: "hair", name: "Hair", description: "Cuts, colors, and care for your best hair days" },
    { slug: "skincare", name: "Skincare", description: "Routines and products for glowing, healthy skin" },
    { slug: "trends", name: "Trends", description: "What's hot in beauty right now" },
  ],

  // Content settings
  postsPerPage: 12,
  relatedPostsCount: 4,

  // Newsletter (placeholder)
  newsletter: {
    enabled: true,
    provider: "placeholder", // Change to "mailchimp", "convertkit", etc.
    formAction: "#",
  },

  // Contact
  contactEmail: "hello@lustredaily.com",

  // Legal
  copyrightYear: new Date().getFullYear(),

  // Colors (for OG images, etc.)
  colors: {
    primary: "#E91E63",
    secondary: "#9C27B0",
    accent: "#FF4081",
  },
} as const;

export type Category = typeof siteConfig.categories[number];
export type CategorySlug = Category["slug"];
