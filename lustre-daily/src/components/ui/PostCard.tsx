import Link from "next/link";
import { formatDate, categoryToName } from "@/lib/utils";
import type { PostMeta } from "@/lib/posts";
import { cn } from "@/lib/utils";

interface PostCardProps {
  post: PostMeta;
  featured?: boolean;
}

export function PostCard({ post, featured = false }: PostCardProps) {
  const { slug, frontmatter, readingTime } = post;

  return (
    <article
      className={cn(
        "group overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-all hover:shadow-md dark:border-gray-700 dark:bg-gray-800",
        featured && "md:col-span-2 md:grid md:grid-cols-2"
      )}
    >
      {/* Hero Image */}
      <Link
        href={`/posts/${slug}`}
        className={cn(
          "relative block aspect-video overflow-hidden bg-gradient-to-br from-pink-100 to-purple-100 dark:from-pink-900/30 dark:to-purple-900/30",
          featured && "md:aspect-auto md:h-full"
        )}
      >
        {/* Placeholder image with gradient */}
        <div className="absolute inset-0 flex items-center justify-center">
          <svg
            className="h-16 w-16 text-pink-300 dark:text-pink-700"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1}
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
        </div>

        {/* Category badge */}
        <span className="absolute left-4 top-4 rounded-full bg-white/90 px-3 py-1 text-xs font-medium text-gray-700 backdrop-blur dark:bg-gray-900/90 dark:text-gray-300">
          {categoryToName(frontmatter.category)}
        </span>

        {/* Monetized indicator (subtle) */}
        {frontmatter.monetized && (
          <span className="absolute right-4 top-4 rounded-full bg-pink-500/90 px-2 py-0.5 text-[10px] font-medium text-white backdrop-blur">
            Shop
          </span>
        )}
      </Link>

      {/* Content */}
      <div className="p-5">
        {/* Meta */}
        <div className="mb-2 flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
          <time dateTime={frontmatter.date}>{formatDate(frontmatter.date)}</time>
          <span aria-hidden="true">&middot;</span>
          <span>{readingTime}</span>
        </div>

        {/* Title */}
        <h3
          className={cn(
            "font-semibold text-gray-900 transition-colors group-hover:text-pink-600 dark:text-white dark:group-hover:text-pink-400",
            featured ? "text-xl md:text-2xl" : "text-lg"
          )}
        >
          <Link href={`/posts/${slug}`}>{frontmatter.title}</Link>
        </h3>

        {/* Description */}
        <p
          className={cn(
            "mt-2 text-gray-600 dark:text-gray-300",
            featured ? "text-base" : "line-clamp-2 text-sm"
          )}
        >
          {frontmatter.description}
        </p>

        {/* Tags */}
        {frontmatter.tags && frontmatter.tags.length > 0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {frontmatter.tags.slice(0, 3).map((tag) => (
              <span
                key={tag}
                className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs text-gray-600 dark:bg-gray-700 dark:text-gray-300"
              >
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* Read more link */}
        <Link
          href={`/posts/${slug}`}
          className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-pink-600 hover:text-pink-700 dark:text-pink-400 dark:hover:text-pink-300"
        >
          Read more
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </Link>
      </div>
    </article>
  );
}

export default PostCard;
