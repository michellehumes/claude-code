import fs from "fs";
import path from "path";
import matter from "gray-matter";
import readingTime from "reading-time";
import { siteConfig } from "@/site.config";

const postsDirectory = path.join(process.cwd(), "content/posts");

export interface PostFrontmatter {
  title: string;
  description: string;
  date: string;
  category: "makeup" | "hair" | "skincare" | "trends";
  tags: string[];
  heroImage: string;
  monetized: boolean;
  author?: string;
  lastModified?: string;
}

export interface Post {
  slug: string;
  frontmatter: PostFrontmatter;
  content: string;
  readingTime: string;
}

export interface PostMeta {
  slug: string;
  frontmatter: PostFrontmatter;
  readingTime: string;
}

/**
 * Get all post slugs
 */
export function getPostSlugs(): string[] {
  if (!fs.existsSync(postsDirectory)) {
    return [];
  }
  return fs
    .readdirSync(postsDirectory)
    .filter((file) => file.endsWith(".mdx"))
    .map((file) => file.replace(/\.mdx$/, ""));
}

/**
 * Get a single post by slug
 */
export function getPostBySlug(slug: string): Post | null {
  const fullPath = path.join(postsDirectory, `${slug}.mdx`);

  if (!fs.existsSync(fullPath)) {
    return null;
  }

  const fileContents = fs.readFileSync(fullPath, "utf8");
  const { data, content } = matter(fileContents);
  const stats = readingTime(content);

  return {
    slug,
    frontmatter: data as PostFrontmatter,
    content,
    readingTime: stats.text,
  };
}

/**
 * Get all posts with metadata (no content for performance)
 */
export function getAllPostsMeta(): PostMeta[] {
  const slugs = getPostSlugs();

  const posts = slugs
    .map((slug) => {
      const fullPath = path.join(postsDirectory, `${slug}.mdx`);
      const fileContents = fs.readFileSync(fullPath, "utf8");
      const { data, content } = matter(fileContents);
      const stats = readingTime(content);

      return {
        slug,
        frontmatter: data as PostFrontmatter,
        readingTime: stats.text,
      };
    })
    .sort((a, b) => {
      return new Date(b.frontmatter.date).getTime() - new Date(a.frontmatter.date).getTime();
    });

  return posts;
}

/**
 * Get posts by category
 */
export function getPostsByCategory(category: string): PostMeta[] {
  return getAllPostsMeta().filter((post) => post.frontmatter.category === category);
}

/**
 * Get monetized posts
 */
export function getMonetizedPosts(): PostMeta[] {
  return getAllPostsMeta().filter((post) => post.frontmatter.monetized === true);
}

/**
 * Get non-monetized posts
 */
export function getNonMonetizedPosts(): PostMeta[] {
  return getAllPostsMeta().filter((post) => post.frontmatter.monetized === false);
}

/**
 * Get posts by tag
 */
export function getPostsByTag(tag: string): PostMeta[] {
  return getAllPostsMeta().filter((post) =>
    post.frontmatter.tags.map((t) => t.toLowerCase()).includes(tag.toLowerCase())
  );
}

/**
 * Get related posts based on category and tags
 */
export function getRelatedPosts(currentSlug: string, limit: number = siteConfig.relatedPostsCount): PostMeta[] {
  const currentPost = getPostBySlug(currentSlug);
  if (!currentPost) return [];

  const allPosts = getAllPostsMeta().filter((p) => p.slug !== currentSlug);

  // Score posts by relevance
  const scored = allPosts.map((post) => {
    let score = 0;

    // Same category = 10 points
    if (post.frontmatter.category === currentPost.frontmatter.category) {
      score += 10;
    }

    // Matching tags = 3 points each
    const currentTags = currentPost.frontmatter.tags.map((t) => t.toLowerCase());
    const postTags = post.frontmatter.tags.map((t) => t.toLowerCase());
    const matchingTags = postTags.filter((t) => currentTags.includes(t));
    score += matchingTags.length * 3;

    // Same monetization status = 2 points
    if (post.frontmatter.monetized === currentPost.frontmatter.monetized) {
      score += 2;
    }

    return { post, score };
  });

  // Sort by score and return top matches
  return scored
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map((s) => s.post);
}

/**
 * Get all unique tags
 */
export function getAllTags(): string[] {
  const posts = getAllPostsMeta();
  const tagSet = new Set<string>();

  posts.forEach((post) => {
    post.frontmatter.tags.forEach((tag) => tagSet.add(tag));
  });

  return Array.from(tagSet).sort();
}

/**
 * Get posts for a specific date (for validation)
 */
export function getPostsByDate(date: string): PostMeta[] {
  return getAllPostsMeta().filter((post) => post.frontmatter.date === date);
}

/**
 * Paginate posts
 */
export function paginatePosts(
  posts: PostMeta[],
  page: number,
  perPage: number = siteConfig.postsPerPage
): { posts: PostMeta[]; totalPages: number; currentPage: number } {
  const totalPages = Math.ceil(posts.length / perPage);
  const start = (page - 1) * perPage;
  const paginatedPosts = posts.slice(start, start + perPage);

  return {
    posts: paginatedPosts,
    totalPages,
    currentPage: page,
  };
}
