import { getAllPostsMeta, getPostsByCategory } from "@/lib/posts";
import { siteConfig } from "@/site.config";
import { PostCard } from "@/components/ui/PostCard";
import { CategoryCard } from "@/components/ui/CategoryCard";
import { Newsletter } from "@/components/ui/Newsletter";
import Link from "next/link";

export default function HomePage() {
  const allPosts = getAllPostsMeta();
  const latestPosts = allPosts.slice(0, 7);
  const featuredPost = latestPosts[0];
  const remainingPosts = latestPosts.slice(1, 7);

  // Get post counts per category
  const categoryPostCounts = siteConfig.categories.map((cat) => ({
    category: cat,
    count: getPostsByCategory(cat.slug).length,
  }));

  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-pink-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-purple-950/20">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
          <div className="text-center">
            <h1 className="bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-4xl font-bold tracking-tight text-transparent sm:text-5xl md:text-6xl">
              {siteConfig.tagline}
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-600 dark:text-gray-400">
              {siteConfig.description}
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              {siteConfig.categories.slice(0, 3).map((category) => (
                <Link
                  key={category.slug}
                  href={`/category/${category.slug}`}
                  className="rounded-full border border-pink-200 bg-white px-6 py-2 text-sm font-medium text-pink-600 transition-all hover:border-pink-300 hover:bg-pink-50 dark:border-pink-800 dark:bg-gray-800 dark:text-pink-400 dark:hover:border-pink-700 dark:hover:bg-gray-700"
                >
                  {category.name}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Latest Posts Section */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mb-8 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Latest Articles
          </h2>
          <Link
            href="/posts"
            className="text-sm font-medium text-pink-600 hover:text-pink-700 dark:text-pink-400 dark:hover:text-pink-300"
          >
            View all articles &rarr;
          </Link>
        </div>

        {allPosts.length > 0 ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {/* Featured Post */}
            {featuredPost && (
              <PostCard post={featuredPost} featured />
            )}

            {/* Remaining Posts */}
            {remainingPosts.map((post) => (
              <PostCard key={post.slug} post={post} />
            ))}
          </div>
        ) : (
          <div className="rounded-lg border border-gray-200 bg-gray-50 p-12 text-center dark:border-gray-700 dark:bg-gray-800">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1}
                d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"
              />
            </svg>
            <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">
              No articles yet
            </h3>
            <p className="mt-2 text-gray-500 dark:text-gray-400">
              Check back soon for beauty tips, trends, and product reviews!
            </p>
          </div>
        )}
      </section>

      {/* Categories Section */}
      <section className="bg-gray-50 dark:bg-gray-900">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <h2 className="mb-8 text-center text-2xl font-bold text-gray-900 dark:text-white">
            Explore by Category
          </h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {categoryPostCounts.map(({ category, count }) => (
              <CategoryCard
                key={category.slug}
                category={category}
                postCount={count}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <Newsletter />
      </section>
    </div>
  );
}
