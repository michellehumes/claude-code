import EmailSignup from "./components/EmailSignup";

const navLinks = [
  { label: "Shop All", href: "#" },
  { label: "Templates", href: "#" },
  { label: "Planners", href: "#" },
  { label: "Wedding", href: "#" },
  { label: "Bundles", href: "#" },
  { label: "Blog", href: "#" },
  { label: "About", href: "#" },
];

const bestSellers = [
  {
    name: "Monthly Budget Tracker",
    price: "$5.99",
    slug: "monthly-budget-tracker",
    img: "/shelzy_images/shelzy_01_img01.svg",
  },
  {
    name: "Small Business Planner 2026",
    price: "$7.99",
    slug: "small-business-planner-2026",
    img: "/shelzy_images/shelzy_08_img01.svg",
  },
  {
    name: "ADHD Life Dashboard",
    price: "$7.99",
    slug: "adhd-life-dashboard",
    img: "/shelzy_images/shelzy_14_img01.svg",
  },
  {
    name: "Meal Planner + Auto Grocery List",
    price: "$5.99",
    slug: "meal-planner-auto-grocery-list",
    img: "/shelzy_images/shelzy_19_img01.svg",
  },
  {
    name: "Job Search Command Center",
    price: "$7.99",
    slug: "job-search-command-center",
    img: "/shelzy_images/shelzy_32_img01.svg",
  },
  {
    name: "Interactive Wedding Planner Dashboard",
    price: "$9.99",
    slug: "interactive-wedding-planner-dashboard",
    img: "/shelzy_images/shelzy_37_img01.svg",
  },
];

const testimonials = [
  {
    name: "Jordan M.",
    text: "This budget tracker literally changed my financial life. I went from guessing where my money went to actually having savings. The auto-calculations do all the hard work!",
    rating: 5,
  },
  {
    name: "Priya S.",
    text: "I bought the wedding planner dashboard and it kept me so organized throughout the entire planning process. Worth every single penny — I recommend it to all my engaged friends!",
    rating: 5,
  },
  {
    name: "Taylor R.",
    text: "As someone with ADHD, the Life Dashboard has been a game-changer. It\u2019s simple enough that I actually use it every day, and the visual layout keeps me on track. Best purchase I\u2019ve made!",
    rating: 5,
  },
];

function MobileMenuButton() {
  return (
    <button
      className="md:hidden text-charcoal"
      aria-label="Toggle menu"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M4 6h16M4 12h16M4 18h16"
        />
      </svg>
    </button>
  );
}

function StarIcon() {
  return (
    <svg
      className="w-5 h-5 text-yellow-400"
      fill="currentColor"
      viewBox="0 0 20 20"
    >
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
  );
}

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <a href="/" className="font-heading text-2xl font-bold text-pink">
              Shelzy&apos;s Designs
            </a>
            <nav className="hidden md:flex items-center space-x-8">
              {navLinks.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  className="text-charcoal hover:text-pink transition-colors text-sm font-medium"
                >
                  {link.label}
                </a>
              ))}
            </nav>
            <MobileMenuButton />
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-light-gray py-16 md:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="font-heading text-4xl md:text-5xl lg:text-6xl font-bold text-charcoal mb-6">
            Templates That Actually Work
          </h1>
          <p className="text-text-light text-lg md:text-xl max-w-2xl mx-auto mb-8">
            Beautiful, functional spreadsheet templates for Google Sheets and
            Excel. Budget trackers, planners, dashboards &amp; more — designed to
            simplify your life.
          </p>
          <a
            href="#"
            className="inline-block bg-pink text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-pink-hover transition-colors"
          >
            Shop All Templates
          </a>
        </div>
      </section>

      {/* Featured Collections */}
      <section className="py-16 md:py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="font-heading text-3xl md:text-4xl font-bold text-charcoal text-center mb-12">
            Featured Collections
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <a
              href="#"
              className="group block bg-teal/10 rounded-2xl p-8 text-center hover:bg-teal/20 transition-colors"
            >
              <div className="w-16 h-16 bg-teal/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-8 h-8 text-teal"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h3 className="font-heading text-xl font-bold text-charcoal mb-2">
                Budget + Finance
              </h3>
              <p className="text-text-light">
                Take control of your money with auto-calculating trackers and
                dashboards.
              </p>
            </a>
            <a
              href="#"
              className="group block bg-teal/10 rounded-2xl p-8 text-center hover:bg-teal/20 transition-colors"
            >
              <div className="w-16 h-16 bg-teal/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-8 h-8 text-teal"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                  />
                </svg>
              </div>
              <h3 className="font-heading text-xl font-bold text-charcoal mb-2">
                Wedding Planning
              </h3>
              <p className="text-text-light">
                Plan your perfect day with checklists, budgets, and timelines all
                in one place.
              </p>
            </a>
            <a
              href="#"
              className="group block bg-orange/10 rounded-2xl p-8 text-center hover:bg-orange/20 transition-colors"
            >
              <div className="w-16 h-16 bg-orange/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-8 h-8 text-orange"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <h3 className="font-heading text-xl font-bold text-charcoal mb-2">
                Business Tools
              </h3>
              <p className="text-text-light">
                Streamline your small business with professional planning and
                tracking templates.
              </p>
            </a>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-light-gray py-16 md:py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="font-heading text-3xl md:text-4xl font-bold text-charcoal text-center mb-12">
            How It Works
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-14 h-14 bg-pink text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                1
              </div>
              <h3 className="font-heading text-lg font-bold text-charcoal mb-2">
                Choose Your Template
              </h3>
              <p className="text-text-light">
                Browse our collection and find the perfect template for your
                needs.
              </p>
            </div>
            <div className="text-center">
              <div className="w-14 h-14 bg-pink text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                2
              </div>
              <h3 className="font-heading text-lg font-bold text-charcoal mb-2">
                Instant Download
              </h3>
              <p className="text-text-light">
                Get your file immediately after purchase — no waiting, no
                shipping.
              </p>
            </div>
            <div className="text-center">
              <div className="w-14 h-14 bg-pink text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                3
              </div>
              <h3 className="font-heading text-lg font-bold text-charcoal mb-2">
                Start Organizing
              </h3>
              <p className="text-text-light">
                Open in Google Sheets or Excel, customize to your style, and
                enjoy!
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Best Sellers */}
      <section className="py-16 md:py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="font-heading text-3xl md:text-4xl font-bold text-charcoal text-center mb-12">
            Best Sellers
          </h2>
          <div className="flex overflow-x-auto gap-6 pb-4 -mx-4 px-4 snap-x snap-mandatory scrollbar-hide">
            {bestSellers.map((product) => (
              <a
                key={product.slug}
                href={`#${product.slug}`}
                className="flex-shrink-0 w-64 snap-start group"
              >
                <div className="bg-light-gray rounded-xl overflow-hidden mb-3">
                  <img
                    src={product.img}
                    alt={product.name}
                    className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
                <h3 className="font-heading font-semibold text-charcoal group-hover:text-pink transition-colors">
                  {product.name}
                </h3>
                <p className="text-pink font-bold mt-1">{product.price}</p>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="bg-light-gray py-16 md:py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="font-heading text-3xl md:text-4xl font-bold text-charcoal text-center mb-12">
            What Our Customers Say
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((t) => (
              <div
                key={t.name}
                className="bg-white rounded-2xl p-8 shadow-sm"
              >
                <div className="flex mb-4">
                  {Array.from({ length: t.rating }).map((_, i) => (
                    <StarIcon key={i} />
                  ))}
                </div>
                <p className="text-text-light mb-6 leading-relaxed">
                  &ldquo;{t.text}&rdquo;
                </p>
                <p className="font-heading font-bold text-charcoal">
                  {t.name}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Email Signup */}
      <EmailSignup />

      {/* Designed for Real Life */}
      <section className="py-16 md:py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="font-heading text-3xl md:text-4xl font-bold text-charcoal mb-6">
            Designed for Real Life
          </h2>
          <p className="text-text-light text-lg leading-relaxed mb-6">
            Hi, I&apos;m Shelzy! I create digital templates because I believe
            getting organized shouldn&apos;t be complicated (or ugly). Every
            template is designed to be beautiful AND functional — with
            auto-calculating formulas, clean layouts, and intuitive designs that
            you&apos;ll actually enjoy using.
          </p>
          <p className="text-text-light text-lg leading-relaxed">
            Whether you&apos;re tracking your budget, planning a wedding, or
            running a small business, my templates are built to save you time and
            make your life easier.
          </p>
        </div>
      </section>

      {/* Trust Strip */}
      <section className="bg-charcoal py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <svg
                className="w-8 h-8 text-pink mx-auto mb-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>
              <h3 className="text-white font-semibold mb-1">
                Instant Download
              </h3>
              <p className="text-white/60 text-sm">
                Get your files immediately
              </p>
            </div>
            <div>
              <svg
                className="w-8 h-8 text-pink mx-auto mb-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"
                />
              </svg>
              <h3 className="text-white font-semibold mb-1">
                Excel + Google Sheets
              </h3>
              <p className="text-white/60 text-sm">
                Works with both platforms
              </p>
            </div>
            <div>
              <svg
                className="w-8 h-8 text-pink mx-auto mb-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                />
              </svg>
              <h3 className="text-white font-semibold mb-1">
                Auto-Calculating Formulas
              </h3>
              <p className="text-white/60 text-sm">
                Built-in smart formulas
              </p>
            </div>
            <div>
              <svg
                className="w-8 h-8 text-pink mx-auto mb-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <h3 className="text-white font-semibold mb-1">
                100% Satisfaction
              </h3>
              <p className="text-white/60 text-sm">
                Love it or get a full refund
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-charcoal border-t border-white/10 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-heading text-xl font-bold text-pink mb-4">
                Shelzy&apos;s Designs
              </h3>
              <p className="text-white/60 text-sm leading-relaxed">
                Beautiful, functional digital templates designed to simplify your
                life.
              </p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Shop</h4>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-white/60 hover:text-pink text-sm transition-colors">
                    All Templates
                  </a>
                </li>
                <li>
                  <a href="#" className="text-white/60 hover:text-pink text-sm transition-colors">
                    Budget &amp; Finance
                  </a>
                </li>
                <li>
                  <a href="#" className="text-white/60 hover:text-pink text-sm transition-colors">
                    Planners
                  </a>
                </li>
                <li>
                  <a href="#" className="text-white/60 hover:text-pink text-sm transition-colors">
                    Wedding
                  </a>
                </li>
                <li>
                  <a href="#" className="text-white/60 hover:text-pink text-sm transition-colors">
                    Bundles
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Help</h4>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-white/60 hover:text-pink text-sm transition-colors">
                    FAQ
                  </a>
                </li>
                <li>
                  <a href="#" className="text-white/60 hover:text-pink text-sm transition-colors">
                    Contact
                  </a>
                </li>
                <li>
                  <a href="#" className="text-white/60 hover:text-pink text-sm transition-colors">
                    Refund Policy
                  </a>
                </li>
                <li>
                  <a href="#" className="text-white/60 hover:text-pink text-sm transition-colors">
                    Terms of Service
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Connect</h4>
              <ul className="space-y-2">
                <li>
                  <a
                    href="https://instagram.com/shelzysdesigns"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-white/60 hover:text-pink text-sm transition-colors"
                  >
                    Instagram @shelzysdesigns
                  </a>
                </li>
                <li>
                  <a
                    href="https://pinterest.com/shelzysdesigns"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-white/60 hover:text-pink text-sm transition-colors"
                  >
                    Pinterest @shelzysdesigns
                  </a>
                </li>
                <li>
                  <a href="#" className="text-white/60 hover:text-pink text-sm transition-colors">
                    Etsy Shop
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-white/10 mt-8 pt-8 text-center">
            <p className="text-white/40 text-sm">
              &copy; 2026 Shelzy&apos;s Designs
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
