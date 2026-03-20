import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-white border-b border-mid-gray">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="font-heading text-2xl font-bold text-charcoal">
          Shelzy&apos;s Designs
        </Link>
        <nav className="hidden md:flex items-center gap-6">
          <Link href="/collections/templates" className="text-text-light hover:text-charcoal transition-colors">Templates</Link>
          <Link href="/collections/planners" className="text-text-light hover:text-charcoal transition-colors">Planners</Link>
          <Link href="/collections/wedding" className="text-text-light hover:text-charcoal transition-colors">Wedding</Link>
          <Link href="/blog" className="text-text-light hover:text-charcoal transition-colors">Blog</Link>
          <Link href="/faq" className="text-text-light hover:text-charcoal transition-colors">FAQ</Link>
          <Link
            href="https://www.etsy.com/shop/ShelzysDesignsStore"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-pink text-white px-4 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity"
          >
            Shop on Etsy
          </Link>
        </nav>
      </div>
    </header>
  );
}
