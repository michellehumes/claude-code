"use client";

import Link from "next/link";
import { useState } from "react";
import { siteConfig } from "@/site.config";
import { cn } from "@/lib/utils";

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/80 dark:border-gray-800 dark:bg-gray-900/95 dark:supports-[backdrop-filter]:bg-gray-900/80">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-pink-500 to-purple-600">
            <svg
              className="h-6 w-6 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
              />
            </svg>
          </div>
          <span className="bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-xl font-bold text-transparent">
            {siteConfig.name}
          </span>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex md:items-center md:gap-6">
          {siteConfig.categories.map((category) => (
            <Link
              key={category.slug}
              href={`/category/${category.slug}`}
              className="text-sm font-medium text-gray-700 transition-colors hover:text-pink-600 dark:text-gray-300 dark:hover:text-pink-400"
            >
              {category.name}
            </Link>
          ))}
          <Link
            href="/posts"
            className="text-sm font-medium text-gray-700 transition-colors hover:text-pink-600 dark:text-gray-300 dark:hover:text-pink-400"
          >
            All Posts
          </Link>
          <Link
            href="/about"
            className="text-sm font-medium text-gray-700 transition-colors hover:text-pink-600 dark:text-gray-300 dark:hover:text-pink-400"
          >
            About
          </Link>
        </div>

        {/* Mobile menu button */}
        <button
          type="button"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="inline-flex items-center justify-center rounded-lg p-2 text-gray-700 hover:bg-gray-100 md:hidden dark:text-gray-300 dark:hover:bg-gray-800"
        >
          <span className="sr-only">Open main menu</span>
          {mobileMenuOpen ? (
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          )}
        </button>
      </nav>

      {/* Mobile Navigation */}
      <div
        className={cn(
          "border-t border-gray-200 md:hidden dark:border-gray-800",
          mobileMenuOpen ? "block" : "hidden"
        )}
      >
        <div className="space-y-1 px-4 py-3">
          {siteConfig.categories.map((category) => (
            <Link
              key={category.slug}
              href={`/category/${category.slug}`}
              onClick={() => setMobileMenuOpen(false)}
              className="block rounded-lg px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"
            >
              {category.name}
            </Link>
          ))}
          <Link
            href="/posts"
            onClick={() => setMobileMenuOpen(false)}
            className="block rounded-lg px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"
          >
            All Posts
          </Link>
          <Link
            href="/about"
            onClick={() => setMobileMenuOpen(false)}
            className="block rounded-lg px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"
          >
            About
          </Link>
        </div>
      </div>
    </header>
  );
}

export default Header;
