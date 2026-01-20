import { notFound } from "next/navigation";
import { Metadata } from "next";
import { getPostBySlug, getPostSlugs, getRelatedPosts } from "@/lib/posts";
import { siteConfig } from "@/site.config";
import { generateBlogPostingSchema, generateBreadcrumbSchema } from "@/lib/schema";
import { formatDate, categoryToName } from "@/lib/utils";
import { AffiliateDisclosure } from "@/components/mdx/AffiliateDisclosure";
import { TableOfContents } from "@/components/mdx/TableOfContents";
import { RelatedPosts } from "@/components/ui/RelatedPosts";
import { MDXContent } from "./mdx-content";
import Link from "next/link";

interface PostPageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const slugs = getPostSlugs();
  return slugs.map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: PostPageProps): Promise<Metadata> {
  const { slug } = await params;
  const post = getPostBySlug(slug);

  if (!post) {
    return {
      title: "Post Not Found",
    };
  }

  const { frontmatter } = post;

  return {
    title: frontmatter.title,
    description: frontmatter.description,
    keywords: frontmatter.tags,
    authors: [{ name: frontmatter.author || `${siteConfig.name} Team` }],
    openGraph: {
      title: frontmatter.title,
      description: frontmatter.description,
      type: "article",
      publishedTime: frontmatter.date,
      modifiedTime: frontmatter.lastModified || frontmatter.date,
      authors: [frontmatter.author || `${siteConfig.name} Team`],
      tags: frontmatter.tags,
      images: [
        {
          url: frontmatter.heroImage.startsWith("http")
            ? frontmatter.heroImage
            : `${siteConfig.url}${frontmatter.heroImage}`,
          width: 1200,
          height: 630,
          alt: frontmatter.title,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title: frontmatter.title,
      description: frontmatter.description,
      images: [
        frontmatter.heroImage.startsWith("http")
          ? frontmatter.heroImage
          : `${siteConfig.url}${frontmatter.heroImage}`,
      ],
    },
  };
}

export default async function PostPage({ params }: PostPageProps) {
  const { slug } = await params;
  const post = getPostBySlug(slug);

  if (!post) {
    notFound();
  }

  const { frontmatter, content, readingTime } = post;
  const relatedPosts = getRelatedPosts(slug);

  const blogPostingSchema = generateBlogPostingSchema(frontmatter, slug, content);
  const breadcrumbSchema = generateBreadcrumbSchema([
    { name: "Home", url: siteConfig.url },
    { name: categoryToName(frontmatter.category), url: `${siteConfig.url}/category/${frontmatter.category}` },
    { name: frontmatter.title, url: `${siteConfig.url}/posts/${slug}` },
  ]);

  return (
    <article className="animate-fade-in">
      {/* Schema.org structured data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(blogPostingSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />

      {/* Hero Section */}
      <header className="bg-gradient-to-br from-pink-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-purple-950/20">
        <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
          {/* Breadcrumb */}
          <nav className="mb-4 text-sm text-gray-500 dark:text-gray-400">
            <Link href="/" className="hover:text-pink-600 dark:hover:text-pink-400">
              Home
            </Link>
            <span className="mx-2">/</span>
            <Link
              href={`/category/${frontmatter.category}`}
              className="hover:text-pink-600 dark:hover:text-pink-400"
            >
              {categoryToName(frontmatter.category)}
            </Link>
            <span className="mx-2">/</span>
            <span className="text-gray-900 dark:text-white">Article</span>
          </nav>

          {/* Category & Meta */}
          <div className="mb-4 flex flex-wrap items-center gap-3">
            <Link
              href={`/category/${frontmatter.category}`}
              className="rounded-full bg-pink-100 px-3 py-1 text-sm font-medium text-pink-700 dark:bg-pink-900/30 dark:text-pink-300"
            >
              {categoryToName(frontmatter.category)}
            </Link>
            <span className="text-sm text-gray-500 dark:text-gray-400">
              <time dateTime={frontmatter.date}>{formatDate(frontmatter.date)}</time>
            </span>
            <span className="text-sm text-gray-500 dark:text-gray-400">&middot;</span>
            <span className="text-sm text-gray-500 dark:text-gray-400">{readingTime}</span>
          </div>

          {/* Title */}
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white sm:text-4xl md:text-5xl">
            {frontmatter.title}
          </h1>

          {/* Description */}
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
            {frontmatter.description}
          </p>

          {/* Tags */}
          {frontmatter.tags && frontmatter.tags.length > 0 && (
            <div className="mt-6 flex flex-wrap gap-2">
              {frontmatter.tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-600 dark:bg-gray-800 dark:text-gray-300"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </header>

      {/* Content */}
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="lg:grid lg:grid-cols-12 lg:gap-8">
          {/* Main Content */}
          <div className="lg:col-span-8">
            {/* Affiliate Disclosure (only for monetized posts) */}
            {frontmatter.monetized && <AffiliateDisclosure />}

            {/* MDX Content */}
            <div className="prose prose-lg max-w-none dark:prose-invert prose-headings:font-bold prose-a:text-pink-600 prose-a:no-underline hover:prose-a:underline dark:prose-a:text-pink-400">
              <MDXContent content={content} />
            </div>

            {/* Related Posts */}
            <RelatedPosts posts={relatedPosts} />
          </div>

          {/* Sidebar */}
          <aside className="hidden lg:col-span-4 lg:block">
            <div className="sticky top-24 space-y-6">
              {/* Table of Contents */}
              <TableOfContents content={content} />

              {/* Share buttons (placeholder) */}
              <div className="rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-800">
                <h4 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                  Share This Article
                </h4>
                <div className="flex gap-2">
                  <a
                    href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(frontmatter.title)}&url=${encodeURIComponent(`${siteConfig.url}/posts/${slug}`)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="rounded-lg bg-gray-100 p-2 text-gray-600 transition-colors hover:bg-pink-100 hover:text-pink-600 dark:bg-gray-700 dark:text-gray-400 dark:hover:bg-pink-900/30 dark:hover:text-pink-400"
                    aria-label="Share on Twitter"
                  >
                    <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                    </svg>
                  </a>
                  <a
                    href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(`${siteConfig.url}/posts/${slug}`)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="rounded-lg bg-gray-100 p-2 text-gray-600 transition-colors hover:bg-pink-100 hover:text-pink-600 dark:bg-gray-700 dark:text-gray-400 dark:hover:bg-pink-900/30 dark:hover:text-pink-400"
                    aria-label="Share on Facebook"
                  >
                    <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                    </svg>
                  </a>
                  <a
                    href={`https://pinterest.com/pin/create/button/?url=${encodeURIComponent(`${siteConfig.url}/posts/${slug}`)}&description=${encodeURIComponent(frontmatter.title)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="rounded-lg bg-gray-100 p-2 text-gray-600 transition-colors hover:bg-pink-100 hover:text-pink-600 dark:bg-gray-700 dark:text-gray-400 dark:hover:bg-pink-900/30 dark:hover:text-pink-400"
                    aria-label="Share on Pinterest"
                  >
                    <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 0c-6.627 0-12 5.372-12 12 0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738.098.119.112.224.083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.631-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146 1.124.347 2.317.535 3.554.535 6.627 0 12-5.373 12-12 0-6.628-5.373-12-12-12z" />
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </article>
  );
}
