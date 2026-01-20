import { notFound } from "next/navigation";
import { Metadata } from "next";
import { getPostsByCategory } from "@/lib/posts";
import { siteConfig } from "@/site.config";
import { PostCard } from "@/components/ui/PostCard";
import { generateItemListSchema } from "@/lib/schema";

interface CategoryPageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return siteConfig.categories.map((category) => ({
    slug: category.slug,
  }));
}

export async function generateMetadata({ params }: CategoryPageProps): Promise<Metadata> {
  const { slug } = await params;
  const category = siteConfig.categories.find((c) => c.slug === slug);

  if (!category) {
    return {
      title: "Category Not Found",
    };
  }

  return {
    title: `${category.name} - Beauty Tips & Product Reviews`,
    description: category.description,
    openGraph: {
      title: `${category.name} | ${siteConfig.name}`,
      description: category.description,
      type: "website",
    },
  };
}

export default async function CategoryPage({ params }: CategoryPageProps) {
  const { slug } = await params;
  const category = siteConfig.categories.find((c) => c.slug === slug);

  if (!category) {
    notFound();
  }

  const posts = getPostsByCategory(slug);
  const itemListSchema = generateItemListSchema(
    posts.map((post, index) => ({
      title: post.frontmatter.title,
      slug: post.slug,
      position: index + 1,
    }))
  );

  return (
    <div className="animate-fade-in">
      {/* Schema.org structured data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(itemListSchema) }}
      />

      {/* Header */}
      <section className="bg-gradient-to-br from-pink-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-purple-950/20">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <nav className="mb-4 text-sm text-gray-500 dark:text-gray-400">
            <a href="/" className="hover:text-pink-600 dark:hover:text-pink-400">
              Home
            </a>
            <span className="mx-2">/</span>
            <span className="text-gray-900 dark:text-white">{category.name}</span>
          </nav>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white sm:text-4xl">
            {category.name}
          </h1>
          <p className="mt-3 max-w-2xl text-lg text-gray-600 dark:text-gray-400">
            {category.description}
          </p>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-500">
            {posts.length} article{posts.length !== 1 ? "s" : ""}
          </p>
        </div>
      </section>

      {/* Posts Grid */}
      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        {posts.length > 0 ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {posts.map((post) => (
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
              Check back soon for {category.name.toLowerCase()} content!
            </p>
          </div>
        )}
      </section>
    </div>
  );
}
