// Site Configuration
// Change brand name and other settings here - this is the single source of truth

export const siteConfig = {
  // Brand
  name: "Shelzy's Beauty",
  tagline: "Honest Reviews. Real Results. Beauty That Works.",
  description: "Expert-tested beauty product reviews, skincare routines, hair care tips, and makeup tutorials. Find the best products on Amazon with honest reviews from real beauty enthusiasts.",

  // URLs
  url: process.env.NEXT_PUBLIC_SITE_URL || "https://shelzysbeauty.com",

  // Amazon Affiliate
  amazonAssociateTag: process.env.AMAZON_ASSOC_TAG || "shelzysbeauty-20",

  // Social (placeholders)
  social: {
    instagram: "https://instagram.com/shelzysbeauty",
    pinterest: "https://pinterest.com/shelzysbeauty",
    tiktok: "https://tiktok.com/@shelzysbeauty",
    twitter: "https://twitter.com/shelzysbeauty",
  },

  // Categories
  categories: [
    { slug: "makeup", name: "Makeup", description: "Foundation to finishing touches - master your makeup game" },
    { slug: "skincare", name: "Skincare", description: "Routines and products for glowing, healthy skin" },
    { slug: "hair", name: "Hair", description: "Cuts, colors, and care for your best hair days" },
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
  contactEmail: "hello@shelzysbeauty.com",

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
