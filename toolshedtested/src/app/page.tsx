import { getAllArticles } from '@/lib/articles'
import SubscribeForm from '@/components/SubscribeForm'

export default function HomePage() {
  const articles = getAllArticles()
  const reviewCount = articles.length
  const displayCount = Math.floor(reviewCount / 10) * 10 + '+'

  return (
    <main>
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <span className="badge">100% Independent Reviews</span>
          <h1>
            Tools That <span className="highlight">Actually Work</span>
            <br />Tested In Real Conditions
          </h1>
          <p className="hero-subtitle">
            No sponsorships. No bias. Just honest reviews from 500+ hours of
            hands-on testing.
          </p>
        </div>
      </section>

      {/* Trust Stats Section */}
      <section className="trust-stats">
        <div className="stats-grid">
          <div className="stat">
            <span className="stat-number">{displayCount}</span>
            <span className="stat-label">Reviews Published</span>
          </div>
          <div className="stat">
            <span className="stat-number">100%</span>
            <span className="stat-label">Independently Funded</span>
          </div>
          <div className="stat">
            <span className="stat-number">0</span>
            <span className="stat-label">Sponsored Reviews</span>
          </div>
          <div className="stat">
            <span className="stat-number">2025</span>
            <span className="stat-label">Founded</span>
          </div>
        </div>
      </section>

      {/* Latest Reviews */}
      <section className="latest-reviews">
        <h2>Latest Reviews</h2>
        <div className="reviews-grid">
          {articles.map((article) => (
            <a key={article.slug} href={`/${article.slug}`} className="review-card">
              <span className="review-category">{article.categoryLabel}</span>
              <h3>{article.title}</h3>
              <p>{article.description}</p>
              <span className="review-date">{article.date}</span>
            </a>
          ))}
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="newsletter-section">
        <h2>Get Tool Deals & Reviews</h2>
        <p>Join our newsletter for weekly tool deals and honest reviews.</p>
        <SubscribeForm />
      </section>
    </main>
  )
}
