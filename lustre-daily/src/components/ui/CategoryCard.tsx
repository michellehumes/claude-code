import Link from "next/link";
import type { Category } from "@/site.config";
import { ReactElement } from "react";

interface CategoryCardProps {
  category: Category;
  postCount?: number;
}

const categoryIcons: Record<string, ReactElement> = {
  makeup: (
    <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={1.5}
        d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"
      />
    </svg>
  ),
  hair: (
    <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={1.5}
        d="M14.121 14.121L19 19m-7-7l7-7m-7 7l-2.879 2.879M12 12L9.121 9.121m0 5.758a3 3 0 10-4.243 4.243 3 3 0 004.243-4.243zm0-5.758a3 3 0 10-4.243-4.243 3 3 0 004.243 4.243z"
      />
    </svg>
  ),
  skincare: (
    <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={1.5}
        d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
      />
    </svg>
  ),
  trends: (
    <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={1.5}
        d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
      />
    </svg>
  ),
};

const categoryGradients: Record<string, string> = {
  makeup: "from-rose-400 to-pink-600",
  hair: "from-amber-400 to-orange-500",
  skincare: "from-emerald-400 to-teal-500",
  trends: "from-violet-400 to-purple-600",
};

export function CategoryCard({ category, postCount }: CategoryCardProps) {
  const icon = categoryIcons[category.slug] || categoryIcons.trends;
  const gradient = categoryGradients[category.slug] || categoryGradients.trends;

  return (
    <Link
      href={`/category/${category.slug}`}
      className="group relative overflow-hidden rounded-2xl p-6 transition-transform hover:-translate-y-1"
    >
      {/* Background gradient */}
      <div
        className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-90 transition-opacity group-hover:opacity-100`}
      />

      {/* Content */}
      <div className="relative z-10 text-white">
        {/* Icon */}
        <div className="mb-4 inline-flex h-14 w-14 items-center justify-center rounded-full bg-white/20">
          {icon}
        </div>

        {/* Title */}
        <h3 className="text-xl font-bold">{category.name}</h3>

        {/* Description */}
        <p className="mt-2 text-sm text-white/80">{category.description}</p>

        {/* Post count */}
        {postCount !== undefined && (
          <p className="mt-4 text-xs font-medium text-white/70">
            {postCount} article{postCount !== 1 ? "s" : ""}
          </p>
        )}

        {/* Arrow */}
        <div className="absolute bottom-6 right-6 opacity-0 transition-opacity group-hover:opacity-100">
          <svg
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M17 8l4 4m0 0l-4 4m4-4H3"
            />
          </svg>
        </div>
      </div>
    </Link>
  );
}

export default CategoryCard;
