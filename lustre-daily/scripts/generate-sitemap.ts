#!/usr/bin/env npx ts-node

/**
 * Sitemap Generation Script
 * Generates sitemap.xml for SEO
 */

import fs from "fs";
import path from "path";
import matter from "gray-matter";

// Import site config - use require for CommonJS compatibility
const siteConfigPath = path.join(process.cwd(), "site.config.ts");
const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://lustredaily.com";

interface PostFrontmatter {
  title: string;
  date: string;
  category: string;
  lastModified?: string;
}

interface SitemapUrl {
  loc: string;
  lastmod?: string;
  changefreq?: string;
  priority?: string;
}

// Load all posts
function loadPosts(): { slug: string; frontmatter: PostFrontmatter }[] {
  const postsDir = path.join(process.cwd(), "content/posts");

  if (!fs.existsSync(postsDir)) {
    return [];
  }

  const files = fs.readdirSync(postsDir).filter((f) => f.endsWith(".mdx"));

  return files.map((file) => {
    const filePath = path.join(postsDir, file);
    const fileContents = fs.readFileSync(filePath, "utf8");
    const { data } = matter(fileContents);

    return {
      slug: file.replace(/\.mdx$/, ""),
      frontmatter: data as PostFrontmatter,
    };
  });
}

// Generate XML for a single URL
function urlToXml(url: SitemapUrl): string {
  let xml = "  <url>\n";
  xml += `    <loc>${url.loc}</loc>\n`;

  if (url.lastmod) {
    xml += `    <lastmod>${url.lastmod}</lastmod>\n`;
  }

  if (url.changefreq) {
    xml += `    <changefreq>${url.changefreq}</changefreq>\n`;
  }

  if (url.priority) {
    xml += `    <priority>${url.priority}</priority>\n`;
  }

  xml += "  </url>\n";
  return xml;
}

// Generate sitemap
function generateSitemap(): void {
  console.log("Generating sitemap.xml...\n");

  const posts = loadPosts();
  const today = new Date().toISOString().split("T")[0];

  const urls: SitemapUrl[] = [];

  // Homepage
  urls.push({
    loc: siteUrl,
    lastmod: today,
    changefreq: "daily",
    priority: "1.0",
  });

  // Category pages
  const categories = ["makeup", "hair", "skincare", "trends"];
  categories.forEach((category) => {
    urls.push({
      loc: `${siteUrl}/category/${category}`,
      lastmod: today,
      changefreq: "daily",
      priority: "0.8",
    });
  });

  // Static pages
  const staticPages = [
    { path: "/about", priority: "0.7" },
    { path: "/contact", priority: "0.6" },
    { path: "/affiliate-disclosure", priority: "0.5" },
    { path: "/privacy", priority: "0.4" },
    { path: "/terms", priority: "0.4" },
  ];

  staticPages.forEach((page) => {
    urls.push({
      loc: `${siteUrl}${page.path}`,
      changefreq: "monthly",
      priority: page.priority,
    });
  });

  // Blog posts
  posts.forEach((post) => {
    urls.push({
      loc: `${siteUrl}/posts/${post.slug}`,
      lastmod: post.frontmatter.lastModified || post.frontmatter.date,
      changefreq: "monthly",
      priority: "0.7",
    });
  });

  // Generate XML
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
  xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';

  urls.forEach((url) => {
    xml += urlToXml(url);
  });

  xml += "</urlset>\n";

  // Write to public directory
  const outputPath = path.join(process.cwd(), "public/sitemap.xml");
  fs.writeFileSync(outputPath, xml);

  console.log(`Generated sitemap with ${urls.length} URLs`);
  console.log(`Output: ${outputPath}\n`);
}

generateSitemap();
