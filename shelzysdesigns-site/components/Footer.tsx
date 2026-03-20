import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-charcoal text-white">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div>
            <Link href="/" className="font-heading text-xl font-bold">
              Shelzy&apos;s Designs
            </Link>
            <p className="mt-2 text-gray-400 text-sm">
              Digital templates, planners & trackers designed to simplify your life.
            </p>
            <div className="flex gap-4 mt-4">
              <a
                href="https://instagram.com/shelzysdesigns"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Instagram"
                className="text-gray-400 hover:text-white transition-colors"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
              </a>
              <a
                href="https://pinterest.com/shelzysdesigns"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Pinterest"
                className="text-gray-400 hover:text-white transition-colors"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.373 0 0 5.372 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738a.36.36 0 01.083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.631-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12 0-6.628-5.373-12-12-12z"/></svg>
              </a>
              <a
                href="https://www.etsy.com/shop/ShelzysDesignsStore"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Etsy Shop"
                className="text-gray-400 hover:text-white transition-colors"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M8.559 3.074c0-.292.044-.41.365-.41h5.477c1.404 0 2.464.68 3.14 2.152l.478 1.07h.586L18.25 1.81l-.586-.06c-.292.34-.536.39-.975.39H7.097c-1.264 0-1.752.488-1.752 1.752v16.192c0 1.264.488 1.752 1.752 1.752h9.71c.44 0 .683.049.975.39l.586-.06.355-4.076h-.586l-.478 1.07c-.676 1.472-1.736 2.152-3.14 2.152H8.924c-.321 0-.365-.117-.365-.41V12.69h4.316c.973 0 1.575.527 1.942 1.697l.29.878h.586V9.335h-.586l-.29.878c-.367 1.17-.969 1.697-1.942 1.697H8.559V3.074z"/></svg>
              </a>
            </div>
          </div>

          {/* Shop */}
          <div>
            <h4 className="font-heading font-semibold mb-3">Shop</h4>
            <div className="flex flex-col gap-2 text-sm text-gray-400">
              <Link href="/collections/templates" className="hover:text-white transition-colors">Templates</Link>
              <Link href="/collections/planners" className="hover:text-white transition-colors">Planners</Link>
              <Link href="/collections/wedding" className="hover:text-white transition-colors">Wedding</Link>
              <Link href="/collections/bundles" className="hover:text-white transition-colors">Bundles</Link>
              <Link href="/collections/budget-finance" className="hover:text-white transition-colors">Budget & Finance</Link>
              <Link href="/collections/business" className="hover:text-white transition-colors">Business</Link>
            </div>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-heading font-semibold mb-3">Resources</h4>
            <div className="flex flex-col gap-2 text-sm text-gray-400">
              <Link href="/blog" className="hover:text-white transition-colors">Blog</Link>
              <Link href="/faq" className="hover:text-white transition-colors">FAQ</Link>
            </div>
          </div>

          {/* Policies */}
          <div>
            <h4 className="font-heading font-semibold mb-3">Policies</h4>
            <div className="flex flex-col gap-2 text-sm text-gray-400">
              <Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link>
              <Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link>
              <Link href="/refunds" className="hover:text-white transition-colors">Refund Policy</Link>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-6 text-center text-sm text-gray-500">
          &copy; {new Date().getFullYear()} Shelzy&apos;s Designs. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
