import { notFound } from 'next/navigation'
import { getAllArticles, getArticleBySlug } from '@/lib/articles'
import Breadcrumb from '@/components/Breadcrumb'
import type { Metadata } from 'next'

interface PageProps {
  params: { slug: string }
}

export async function generateStaticParams() {
  return getAllArticles().map((article) => ({ slug: article.slug }))
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const article = getArticleBySlug(params.slug)
  if (!article) return {}

  return {
    title: `${article.title} | ToolShed Tested`,
    description: article.description,
    openGraph: {
      title: article.title,
      description: article.description,
      type: 'article',
      publishedTime: article.date,
      authors: [article.author],
    },
  }
}

export default function ArticlePage({ params }: PageProps) {
  const article = getArticleBySlug(params.slug)
  if (!article) notFound()

  // Build Product schema for review-type pages with aggregateRating
  const productSchema: Record<string, unknown> = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: article.title,
    description: article.description,
    review: {
      '@type': 'Review',
      author: {
        '@type': 'Person',
        name: article.author,
      },
      datePublished: article.date,
      reviewBody: article.description,
    },
  }

  // Only add aggregateRating on review pages where a numeric rating exists
  if (article.type === 'review' && article.rating) {
    productSchema.aggregateRating = {
      '@type': 'AggregateRating',
      ratingValue: article.rating,
      bestRating: '5',
      worstRating: '1',
      ratingCount: '1',
      reviewCount: '1',
    }
  }

  // BreadcrumbList schema
  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: 'https://www.toolshedtested.com/',
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: article.categoryLabel,
        item: `https://www.toolshedtested.com/category/${article.category}`,
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: article.title,
      },
    ],
  }

  // Only render Product schema on review pages
  const showProductSchema = article.type === 'review'

  return (
    <>
      {showProductSchema && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(productSchema) }}
        />
      )}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />

      <article>
        <Breadcrumb
          items={[
            { name: 'Home', href: '/' },
            { name: article.categoryLabel, href: `/category/${article.category}` },
            { name: article.title },
          ]}
        />

        <h1>{article.title}</h1>
        <p className="article-meta">
          By {article.author} &middot; {article.date}
        </p>
        <p className="article-description">{article.description}</p>
      </article>
    </>
  )
}
