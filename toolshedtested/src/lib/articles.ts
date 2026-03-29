export interface Article {
  slug: string
  title: string
  description: string
  category: string
  categoryLabel: string
  type: 'review' | 'buying-guide' | 'comparison' | 'how-to'
  rating?: number
  date: string
  author: string
  image?: string
}

export const articles: Article[] = [
  {
    slug: 'best-cordless-drills-2026',
    title: 'Best Cordless Drills 2026: 7 Models Tested Head-to-Head',
    description: 'We tested 7 top cordless drills head-to-head in our workshop. See which drills from DeWalt, Milwaukee, Makita, Bosch, and Ryobi earned our top picks for 2026.',
    category: 'reviews',
    categoryLabel: 'Reviews',
    type: 'review',
    rating: 4.6,
    date: '2026-02-13',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'best-impact-drivers-2026',
    title: 'Best Impact Drivers 2026: Top 5 Tested for Torque, Speed, and Value',
    description: 'We tested the top 5 impact drivers for torque, speed, and value. See which ones made the cut.',
    category: 'reviews',
    categoryLabel: 'Reviews',
    type: 'review',
    rating: 4.7,
    date: '2026-02-10',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'best-circular-saws-under-150',
    title: 'Best Circular Saws Under $150: 5 Budget Picks That Cut Like Pros',
    description: '5 budget circular saws tested. Find out which ones deliver pro-level cuts without the pro-level price.',
    category: 'reviews',
    categoryLabel: 'Reviews',
    type: 'review',
    rating: 4.4,
    date: '2026-02-08',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'best-angle-grinders-for-diy',
    title: 'Best Angle Grinders for DIY 2026: Top 12 Tested for Home Use',
    description: 'We tested 12 angle grinders for DIY use. See the best picks for cutting, grinding, and polishing at home.',
    category: 'reviews',
    categoryLabel: 'Reviews',
    type: 'review',
    rating: 4.5,
    date: '2026-02-05',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'best-pressure-washers-2026',
    title: 'Best Pressure Washers 2026: Top 5 Electric Models Tested for Home Use',
    description: 'Top 5 electric pressure washers tested for cleaning power, portability, and value.',
    category: 'reviews',
    categoryLabel: 'Reviews',
    type: 'review',
    rating: 4.3,
    date: '2026-02-03',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'best-random-orbital-sanders-2026',
    title: 'Best Random Orbital Sanders 2026: Tested for Smooth Finishes',
    description: 'We tested top random orbital sanders for finish quality, comfort, and dust collection.',
    category: 'reviews',
    categoryLabel: 'Reviews',
    type: 'review',
    rating: 4.5,
    date: '2026-01-28',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'best-cordless-brad-nailers-2026',
    title: 'Best Cordless Brad Nailers 2026: Top 5 Picks for Trim and Finish Work',
    description: 'Top 5 cordless brad nailers tested for precision, power, and ease of use in trim work.',
    category: 'reviews',
    categoryLabel: 'Reviews',
    type: 'review',
    rating: 4.4,
    date: '2026-01-25',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'dewalt-vs-milwaukee-2026',
    title: 'DeWalt vs Milwaukee: Which Brand Wins in 2026?',
    description: 'A head-to-head comparison of DeWalt and Milwaukee across drills, impact drivers, saws, and more.',
    category: 'comparisons',
    categoryLabel: 'Comparisons',
    type: 'comparison',
    date: '2026-02-11',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'ryobi-vs-dewalt-for-homeowners',
    title: 'Ryobi vs DeWalt: Best Value for Homeowners in 2026?',
    description: 'Comparing Ryobi and DeWalt for the average homeowner. Which brand offers more value?',
    category: 'comparisons',
    categoryLabel: 'Comparisons',
    type: 'comparison',
    date: '2026-02-06',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'impact-driver-vs-drill-difference',
    title: "Impact Driver vs Drill: What's the Difference and Which Do You Need?",
    description: 'Learn the key differences between impact drivers and drills, and find out which one you actually need.',
    category: 'comparisons',
    categoryLabel: 'Comparisons',
    type: 'comparison',
    date: '2026-01-30',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'cordless-tool-battery-guide',
    title: 'The Complete Guide to Cordless Tool Batteries: 18V vs 20V, Ah Ratings Explained',
    description: 'Everything you need to know about cordless tool batteries, voltage ratings, and amp-hours.',
    category: 'how-to',
    categoryLabel: 'How-To Guides',
    type: 'how-to',
    date: '2026-02-09',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'how-to-choose-first-power-tool-set',
    title: 'How to Choose Your First Power Tool Set (Without Wasting Money)',
    description: 'A beginner-friendly guide to picking your first power tool set without overspending.',
    category: 'how-to',
    categoryLabel: 'How-To Guides',
    type: 'how-to',
    date: '2026-02-01',
    author: 'Shelzy Perkins',
  },
  {
    slug: 'workshop-setup-guide-beginners',
    title: 'Home Workshop Setup Guide: Essential Tools and Layout Tips for Beginners',
    description: 'Set up your home workshop the right way with our guide to essential tools, layout, and organization.',
    category: 'how-to',
    categoryLabel: 'How-To Guides',
    type: 'how-to',
    date: '2026-01-20',
    author: 'Shelzy Perkins',
  },
]

export function getAllArticles(): Article[] {
  return articles
}

export function getArticleBySlug(slug: string): Article | undefined {
  return articles.find((a) => a.slug === slug)
}

export function getArticleCount(): number {
  return articles.length
}
