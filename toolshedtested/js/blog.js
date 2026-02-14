// ========================================
// Blog Posts Data
// ========================================
const blogPosts = [
    {
        id: 1,
        slug: "best-cordless-drills-2026",
        title: "Best Cordless Drills 2026: 7 Models Tested Head-to-Head",
        category: "buying-guide",
        date: "2026-02-13",
        readTime: "12 min read",
        author: "Shelzy Perkins",
        excerpt: "After 60+ hours drilling through hardwood, metal, and concrete, here are the 7 cordless drills that earned our recommendation — and 3 that disappointed us.",
        image: "https://images.unsplash.com/photo-1504148455328-c376907d081c?w=800&h=500&fit=crop"
    },
    {
        id: 2,
        slug: "dewalt-vs-milwaukee-2026",
        title: "DeWalt vs Milwaukee: Which Brand Wins in 2026?",
        category: "comparison",
        date: "2026-02-11",
        readTime: "15 min read",
        author: "Shelzy Perkins",
        excerpt: "We put DeWalt and Milwaukee's top sellers head-to-head in 8 categories. The results surprised us — one brand dominated power while the other won on value.",
        image: "https://images.unsplash.com/photo-1581783898377-1c85bf937427?w=800&h=500&fit=crop"
    },
    {
        id: 3,
        slug: "how-to-choose-first-power-tool-set",
        title: "How to Choose Your First Power Tool Set (Without Wasting Money)",
        category: "how-to",
        date: "2026-02-09",
        readTime: "10 min read",
        author: "Shelzy Perkins",
        excerpt: "Most beginners buy tools they don't need and skip ones they'll use daily. Here's the exact 5-tool starter kit I recommend after 20 years in the trade.",
        image: "https://images.unsplash.com/photo-1530124566582-a45a7e3f2783?w=800&h=500&fit=crop"
    },
    {
        id: 4,
        slug: "best-circular-saws-under-150",
        title: "Best Circular Saws Under $150: 5 Budget Picks That Cut Like Pros",
        category: "buying-guide",
        date: "2026-02-07",
        readTime: "11 min read",
        author: "Shelzy Perkins",
        excerpt: "You don't need to spend $300+ for a great circular saw. We tested 12 budget models and found 5 that deliver professional-grade cuts for under $150.",
        image: "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=800&h=500&fit=crop"
    },
    {
        id: 5,
        slug: "impact-driver-vs-drill-difference",
        title: "Impact Driver vs Drill: What's the Difference and Which Do You Need?",
        category: "how-to",
        date: "2026-02-05",
        readTime: "8 min read",
        author: "Shelzy Perkins",
        excerpt: "This is the #1 question we get asked. Here's the simple breakdown of when you need a drill, when you need an impact driver, and when you need both.",
        image: "https://images.unsplash.com/photo-1426927308491-6380b6a9936f?w=800&h=500&fit=crop"
    },
    {
        id: 6,
        slug: "best-random-orbital-sanders-2026",
        title: "Best Random Orbital Sanders 2026: Tested for Smooth Finishes",
        category: "review",
        date: "2026-02-03",
        readTime: "13 min read",
        author: "Shelzy Perkins",
        excerpt: "We sanded 200+ square feet of hardwood with each sander to find the ones that deliver glass-smooth finishes without the arm fatigue. Here are our top 6 picks.",
        image: "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800&h=500&fit=crop"
    },
    {
        id: 7,
        slug: "cordless-tool-battery-guide",
        title: "The Complete Guide to Cordless Tool Batteries: 18V vs 20V, Ah Ratings Explained",
        category: "how-to",
        date: "2026-02-01",
        readTime: "9 min read",
        author: "Shelzy Perkins",
        excerpt: "18V or 20V MAX? 2.0Ah or 5.0Ah? We cut through the marketing jargon and explain what actually matters when choosing cordless tool batteries.",
        image: "https://images.unsplash.com/photo-1513828583688-c52646db42da?w=800&h=500&fit=crop"
    },
    {
        id: 8,
        slug: "best-angle-grinders-for-diy",
        title: "Best Angle Grinders for DIY 2026: Top 5 Tested for Home Use",
        category: "buying-guide",
        date: "2026-01-30",
        readTime: "11 min read",
        author: "Shelzy Perkins",
        excerpt: "Angle grinders are the most versatile tool in your workshop — if you pick the right one. We tested 10 models over 40 hours to find the best for DIYers.",
        image: "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=800&h=500&fit=crop"
    },
    {
        id: 9,
        slug: "ryobi-vs-dewalt-for-homeowners",
        title: "Ryobi vs DeWalt: Best Value for Homeowners in 2026?",
        category: "comparison",
        date: "2026-01-28",
        readTime: "14 min read",
        author: "Shelzy Perkins",
        excerpt: "Ryobi costs half the price but is it half the tool? We compared both ecosystems across 6 tool categories to find which brand gives homeowners the best bang for their buck.",
        image: "https://images.unsplash.com/photo-1590479773265-7464e5d48118?w=800&h=500&fit=crop"
    },
    {
        id: 10,
        slug: "workshop-setup-guide-beginners",
        title: "Home Workshop Setup Guide: Essential Tools and Layout Tips for Beginners",
        category: "tips",
        date: "2026-01-26",
        readTime: "16 min read",
        author: "Shelzy Perkins",
        excerpt: "Setting up your first workshop? Here's everything you need — from essential tools and workbench plans to electrical requirements and storage solutions.",
        image: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&h=500&fit=crop"
    }
];

// ========================================
// Blog Listing Page Manager
// ========================================
class BlogListManager {
    constructor() {
        this.grid = document.getElementById('blog-grid');
        this.filterBtns = document.querySelectorAll('.blog-filter-btn');
        this.currentFilter = 'all';

        if (this.grid) {
            this.init();
        }
    }

    init() {
        this.renderPosts(blogPosts);
        this.setupFilters();
    }

    setupFilters() {
        this.filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                this.filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.currentFilter = btn.dataset.filter;
                const filtered = this.currentFilter === 'all'
                    ? blogPosts
                    : blogPosts.filter(p => p.category === this.currentFilter);
                this.renderPosts(filtered);
            });
        });
    }

    renderPosts(posts) {
        if (posts.length === 0) {
            this.grid.innerHTML = '<p style="text-align:center; color: var(--text-tertiary); grid-column: 1/-1; padding: 3rem;">No posts found in this category yet. Check back soon!</p>';
            return;
        }

        this.grid.innerHTML = posts.map(post => this.createPostCard(post)).join('');
    }

    createPostCard(post) {
        const dateFormatted = new Date(post.date).toLocaleDateString('en-US', {
            year: 'numeric', month: 'long', day: 'numeric'
        });

        return `
            <article class="blog-card" data-category="${post.category}">
                <img src="${post.image}" alt="${post.title}" class="blog-card-image" loading="lazy">
                <div class="blog-card-body">
                    <div class="blog-card-meta">
                        <span class="blog-card-category">${this.formatCategory(post.category)}</span>
                        <span class="blog-card-date">${dateFormatted}</span>
                        <span class="blog-card-read-time">${post.readTime}</span>
                    </div>
                    <h3 class="blog-card-title">
                        <a href="/blog/${post.slug}.html">${post.title}</a>
                    </h3>
                    <p class="blog-card-excerpt">${post.excerpt}</p>
                    <div class="blog-card-footer">
                        <span class="blog-card-author">By ${post.author}</span>
                        <a href="/blog/${post.slug}.html" class="blog-card-link">Read More &rarr;</a>
                    </div>
                </div>
            </article>
        `;
    }

    formatCategory(cat) {
        const labels = {
            'buying-guide': 'Buying Guide',
            'comparison': 'Comparison',
            'how-to': 'How-To',
            'review': 'Review',
            'tips': 'Tips & Tricks'
        };
        return labels[cat] || cat;
    }
}

// ========================================
// Homepage Latest Articles
// ========================================
class LatestArticlesManager {
    constructor() {
        this.grid = document.getElementById('latest-articles-grid');
        if (this.grid) {
            this.render();
        }
    }

    render() {
        const latest = blogPosts.slice(0, 3);
        this.grid.innerHTML = latest.map(post => {
            const dateFormatted = new Date(post.date).toLocaleDateString('en-US', {
                year: 'numeric', month: 'long', day: 'numeric'
            });
            const categoryLabels = {
                'buying-guide': 'Buying Guide',
                'comparison': 'Comparison',
                'how-to': 'How-To',
                'review': 'Review',
                'tips': 'Tips & Tricks'
            };

            return `
                <article class="blog-card">
                    <img src="${post.image}" alt="${post.title}" class="blog-card-image" loading="lazy">
                    <div class="blog-card-body">
                        <div class="blog-card-meta">
                            <span class="blog-card-category">${categoryLabels[post.category] || post.category}</span>
                            <span class="blog-card-date">${dateFormatted}</span>
                            <span class="blog-card-read-time">${post.readTime}</span>
                        </div>
                        <h3 class="blog-card-title">
                            <a href="/blog/${post.slug}.html">${post.title}</a>
                        </h3>
                        <p class="blog-card-excerpt">${post.excerpt}</p>
                        <div class="blog-card-footer">
                            <span class="blog-card-author">By ${post.author}</span>
                            <a href="/blog/${post.slug}.html" class="blog-card-link">Read More &rarr;</a>
                        </div>
                    </div>
                </article>
            `;
        }).join('');
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    new BlogListManager();
    new LatestArticlesManager();
});
