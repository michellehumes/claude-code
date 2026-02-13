import { getAllPostsMeta, getPostsByCategory, getMonetizedPosts } from "@/lib/posts";
import { siteConfig } from "@/site.config";
import { PostCard } from "@/components/ui/PostCard";
import { CategoryCard } from "@/components/ui/CategoryCard";
import { Newsletter } from "@/components/ui/Newsletter";
import Link from "next/link";

export default function HomePage() {
  const allPosts = getAllPostsMeta();
  const latestPosts = allPosts.slice(0, 6);
  const featuredPost = latestPosts[0];
  const remainingPosts = latestPosts.slice(1, 6);

  // Popular monetized posts (editor's picks for affiliate clicks)
  const shopPosts = getMonetizedPosts().slice(0, 4);

  // Get post counts per category
  const categoryPostCounts = siteConfig.categories.map((cat) => ({
    category: cat,
    count: getPostsByCategory(cat.slug).length,
  }));

  return (
    <div className="animate-fade-in">
      {/* Hero Section - More compelling with clear value prop */}
      <section className="bg-gradient-to-br from-pink-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-purple-950/20">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-20 lg:px-8">
          <div className="text-center">
            <p className="mb-3 text-sm font-semibold uppercase tracking-wider text-pink-600 dark:text-pink-400">
              Trusted by thousands of beauty enthusiasts
            </p>
            <h1 className="bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-4xl font-bold tracking-tight text-transparent sm:text-5xl md:text-6xl">
              {siteConfig.tagline}
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-600 dark:text-gray-400">
              We test the products so you don&apos;t have to. Discover expert-reviewed makeup, skincare, and hair care picks — all available on Amazon.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              {siteConfig.categories.map((category) => (
                <Link
                  key={category.slug}
                  href={`/category/${category.slug}`}
                  className="rounded-full border border-pink-200 bg-white px-6 py-2.5 text-sm font-medium text-pink-600 transition-all hover:border-pink-400 hover:bg-pink-50 hover:shadow-md dark:border-pink-800 dark:bg-gray-800 dark:text-pink-400 dark:hover:border-pink-700 dark:hover:bg-gray-700"
                >
                  {category.name}
                </Link>
              ))}
              <Link
                href="/posts"
                className="rounded-full bg-gradient-to-r from-pink-500 to-purple-600 px-6 py-2.5 text-sm font-medium text-white transition-all hover:from-pink-600 hover:to-purple-700 hover:shadow-md"
              >
                Browse All Articles
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Latest Posts Section */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Latest Articles
            </h2>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              Fresh beauty content published regularly
            </p>
          </div>
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
            <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">
              No articles yet
            </h3>
            <p className="mt-2 text-gray-500 dark:text-gray-400">
              Check back soon for beauty tips, trends, and product reviews!
            </p>
          </div>
        )}
      </section>

      {/* Shop Our Picks - Dedicated section for affiliate content */}
      {shopPosts.length > 0 && (
        <section className="bg-gradient-to-r from-pink-50 to-purple-50 dark:from-gray-900 dark:to-gray-900">
          <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
            <div className="mb-8 text-center">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Shop Our Top Picks
              </h2>
              <p className="mt-2 text-gray-600 dark:text-gray-400">
                Editor-tested products we genuinely recommend. Every pick is linked to Amazon for easy shopping.
              </p>
            </div>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {shopPosts.map((post) => (
                <article key={post.slug} className="group overflow-hidden rounded-xl border border-pink-200 bg-white shadow-sm transition-all hover:shadow-lg dark:border-gray-700 dark:bg-gray-800">
                  <Link href={`/posts/${post.slug}`} className="block">
                    <div className="relative aspect-video overflow-hidden bg-gradient-to-br from-pink-100 to-purple-100 dark:from-pink-900/30 dark:to-purple-900/30">
                      <div className="absolute inset-0 flex items-center justify-center">
                        <svg className="h-10 w-10 text-pink-300 dark:text-pink-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                        </svg>
                      </div>
                      <span className="absolute right-3 top-3 rounded-full bg-pink-500 px-2.5 py-0.5 text-xs font-medium text-white">
                        Shop
                      </span>
                    </div>
                    <div className="p-4">
                      <h3 className="line-clamp-2 font-semibold text-gray-900 transition-colors group-hover:text-pink-600 dark:text-white dark:group-hover:text-pink-400">
                        {post.frontmatter.title}
                      </h3>
                      <p className="mt-1.5 line-clamp-2 text-sm text-gray-500 dark:text-gray-400">
                        {post.frontmatter.description}
                      </p>
                      <span className="mt-3 inline-flex items-center gap-1 text-sm font-medium text-pink-600 dark:text-pink-400">
                        See Our Picks
                        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                        </svg>
                      </span>
                    </div>
                  </Link>
                </article>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Categories Section */}
      <section className="bg-white dark:bg-gray-950">
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

      {/* Why Trust Us - Social proof section */}
      <section className="border-y border-gray-200 bg-gray-50 dark:border-gray-800 dark:bg-gray-900">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <div className="grid gap-8 text-center sm:grid-cols-3">
            <div>
              <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-pink-100 dark:bg-pink-900/30">
                <svg className="h-6 w-6 text-pink-600 dark:text-pink-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white">Personally Tested</h3>
              <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                Every product recommendation is based on real testing and honest evaluation.
              </p>
            </div>
            <div>
              <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-pink-100 dark:bg-pink-900/30">
                <svg className="h-6 w-6 text-pink-600 dark:text-pink-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white">Every Budget Welcome</h3>
              <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                From drugstore steals to luxury splurges, we cover products at every price point.
              </p>
            </div>
            <div>
              <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-pink-100 dark:bg-pink-900/30">
                <svg className="h-6 w-6 text-pink-600 dark:text-pink-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white">Updated Regularly</h3>
              <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                Fresh content published every other day with the latest beauty finds and trends.
              </p>
            </div>
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
