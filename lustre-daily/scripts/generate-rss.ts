#!/usr/bin/env npx ts-node

/**
 * RSS Feed Generation Script
 * Generates feed.xml for RSS subscribers
 */

import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { Feed } from "feed";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://lustredaily.com";
const siteName = "LustreDaily";
const siteDescription =
  "Discover the latest beauty trends, expert tips, and top-rated makeup, hair, and skincare products.";

interface PostFrontmatter {
  title: string;
  description: string;
  date: string;
  category: string;
  tags: string[];
  heroImage: string;
  monetized: boolean;
}

// Load all posts
function loadPosts(): { slug: string; frontmatter: PostFrontmatter; content: string }[] {
  const postsDir = path.join(process.cwd(), "content/posts");

  if (!fs.existsSync(postsDir)) {
    return [];
  }

  const files = fs.readdirSync(postsDir).filter((f) => f.endsWith(".mdx"));

  return files
    .map((file) => {
      const filePath = path.join(postsDir, file);
      const fileContents = fs.readFileSync(filePath, "utf8");
      const { data, content } = matter(fileContents);

      return {
        slug: file.replace(/\.mdx$/, ""),
        frontmatter: data as PostFrontmatter,
        content,
      };
    })
    .sort((a, b) => {
      return new Date(b.frontmatter.date).getTime() - new Date(a.frontmatter.date).getTime();
    });
}

// Generate RSS feed
function generateRssFeed(): void {
  console.log("Generating RSS feed...\n");

  const posts = loadPosts();
  const latestPosts = posts.slice(0, 20); // Latest 20 posts

  const feed = new Feed({
    title: siteName,
    description: siteDescription,
    id: siteUrl,
    link: siteUrl,
    language: "en",
    image: `${siteUrl}/images/logo.png`,
    favicon: `${siteUrl}/favicon.ico`,
    copyright: `Copyright ${new Date().getFullYear()} ${siteName}`,
    updated: new Date(),
    feedLinks: {
      rss2: `${siteUrl}/feed.xml`,
      json: `${siteUrl}/feed.json`,
      atom: `${siteUrl}/atom.xml`,
    },
    author: {
      name: siteName,
      email: "hello@lustredaily.com",
      link: siteUrl,
    },
  });

  // Add posts to feed
  latestPosts.forEach((post) => {
    const postUrl = `${siteUrl}/posts/${post.slug}`;
    const imageUrl = post.frontmatter.heroImage.startsWith("http")
      ? post.frontmatter.heroImage
      : `${siteUrl}${post.frontmatter.heroImage}`;

    feed.addItem({
      title: post.frontmatter.title,
      id: postUrl,
      link: postUrl,
      description: post.frontmatter.description,
      content: `<p>${post.frontmatter.description}</p><p><a href="${postUrl}">Read more</a></p>`,
      author: [
        {
          name: siteName,
          link: siteUrl,
        },
      ],
      date: new Date(post.frontmatter.date),
      image: imageUrl,
      category: [
        {
          name: post.frontmatter.category,
        },
      ],
    });
  });

  // Add categories
  const categories = ["Makeup", "Hair", "Skincare", "Trends"];
  categories.forEach((cat) => {
    feed.addCategory(cat);
  });

  // Generate feed files
  const publicDir = path.join(process.cwd(), "public");

  // RSS 2.0
  fs.writeFileSync(path.join(publicDir, "feed.xml"), feed.rss2());
  console.log("Generated: public/feed.xml (RSS 2.0)");

  // Atom
  fs.writeFileSync(path.join(publicDir, "atom.xml"), feed.atom1());
  console.log("Generated: public/atom.xml (Atom 1.0)");

  // JSON Feed
  fs.writeFileSync(path.join(publicDir, "feed.json"), feed.json1());
  console.log("Generated: public/feed.json (JSON Feed)");

  console.log(`\nGenerated feeds with ${latestPosts.length} posts\n`);
}

generateRssFeed();
