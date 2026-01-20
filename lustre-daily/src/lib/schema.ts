import { siteConfig } from "@/site.config";
import type { PostFrontmatter } from "./posts";

/**
 * Generate Organization schema
 */
export function generateOrganizationSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: siteConfig.name,
    url: siteConfig.url,
    logo: `${siteConfig.url}/images/logo.png`,
    sameAs: Object.values(siteConfig.social),
    description: siteConfig.description,
  };
}

/**
 * Generate WebSite schema with search action
 */
export function generateWebsiteSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: siteConfig.name,
    url: siteConfig.url,
    description: siteConfig.description,
    publisher: {
      "@type": "Organization",
      name: siteConfig.name,
      logo: {
        "@type": "ImageObject",
        url: `${siteConfig.url}/images/logo.png`,
      },
    },
    potentialAction: {
      "@type": "SearchAction",
      target: {
        "@type": "EntryPoint",
        urlTemplate: `${siteConfig.url}/search?q={search_term_string}`,
      },
      "query-input": "required name=search_term_string",
    },
  };
}

/**
 * Generate BlogPosting schema for individual posts
 */
export function generateBlogPostingSchema(
  frontmatter: PostFrontmatter,
  slug: string,
  content: string
) {
  const url = `${siteConfig.url}/posts/${slug}`;
  const wordCount = content.split(/\s+/).length;

  return {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    headline: frontmatter.title,
    description: frontmatter.description,
    image: frontmatter.heroImage.startsWith("http")
      ? frontmatter.heroImage
      : `${siteConfig.url}${frontmatter.heroImage}`,
    datePublished: frontmatter.date,
    dateModified: frontmatter.lastModified || frontmatter.date,
    author: {
      "@type": "Person",
      name: frontmatter.author || `${siteConfig.name} Team`,
      url: `${siteConfig.url}/about`,
    },
    publisher: {
      "@type": "Organization",
      name: siteConfig.name,
      logo: {
        "@type": "ImageObject",
        url: `${siteConfig.url}/images/logo.png`,
      },
    },
    mainEntityOfPage: {
      "@type": "WebPage",
      "@id": url,
    },
    url,
    wordCount,
    keywords: frontmatter.tags.join(", "),
    articleSection: frontmatter.category,
  };
}

/**
 * Generate BreadcrumbList schema
 */
export function generateBreadcrumbSchema(
  items: Array<{ name: string; url: string }>
) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

/**
 * Generate ItemList schema for category pages
 */
export function generateItemListSchema(
  posts: Array<{ title: string; slug: string; position: number }>
) {
  return {
    "@context": "https://schema.org",
    "@type": "ItemList",
    itemListElement: posts.map((post) => ({
      "@type": "ListItem",
      position: post.position,
      url: `${siteConfig.url}/posts/${post.slug}`,
      name: post.title,
    })),
  };
}

/**
 * Generate FAQ schema (for posts with Q&A sections)
 */
export function generateFAQSchema(
  questions: Array<{ question: string; answer: string }>
) {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: questions.map((qa) => ({
      "@type": "Question",
      name: qa.question,
      acceptedAnswer: {
        "@type": "Answer",
        text: qa.answer,
      },
    })),
  };
}

/**
 * Generate Product schema (for product-focused posts)
 */
export function generateProductSchema(product: {
  name: string;
  brand: string;
  description: string;
  url: string;
}) {
  return {
    "@context": "https://schema.org",
    "@type": "Product",
    name: product.name,
    brand: {
      "@type": "Brand",
      name: product.brand,
    },
    description: product.description,
    url: product.url,
    // Note: We don't include price/availability as these change frequently
    // and claiming specific prices violates Amazon Associates guidelines
  };
}
