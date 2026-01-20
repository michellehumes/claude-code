import Link from "next/link";
import { formatDate, categoryToName } from "@/lib/utils";
import type { PostMeta } from "@/lib/posts";

interface RelatedPostsProps {
  posts: PostMeta[];
  title?: string;
}

export function RelatedPosts({ posts, title = "Related Articles" }: RelatedPostsProps) {
  if (posts.length === 0) {
    return null;
  }

  return (
    <section className="mt-12 border-t border-gray-200 pt-8 dark:border-gray-700">
      <h2 className="mb-6 text-2xl font-bold text-gray-900 dark:text-white">
        {title}
      </h2>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {posts.map((post) => (
          <article key={post.slug} className="group">
            {/* Thumbnail */}
            <Link
              href={`/posts/${post.slug}`}
              className="mb-3 block aspect-video overflow-hidden rounded-lg bg-gradient-to-br from-pink-100 to-purple-100 dark:from-pink-900/30 dark:to-purple-900/30"
            >
              <div className="flex h-full items-center justify-center">
                <svg
                  className="h-8 w-8 text-pink-300 dark:text-pink-700"
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
            </Link>

            {/* Meta */}
            <div className="mb-1 flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
              <span className="font-medium text-pink-600 dark:text-pink-400">
                {categoryToName(post.frontmatter.category)}
              </span>
              <span aria-hidden="true">&middot;</span>
              <time dateTime={post.frontmatter.date}>
                {formatDate(post.frontmatter.date, { month: "short", day: "numeric" })}
              </time>
            </div>

            {/* Title */}
            <h3 className="line-clamp-2 font-medium text-gray-900 transition-colors group-hover:text-pink-600 dark:text-white dark:group-hover:text-pink-400">
              <Link href={`/posts/${post.slug}`}>{post.frontmatter.title}</Link>
            </h3>
          </article>
        ))}
      </div>
    </section>
  );
}

export default RelatedPosts;
