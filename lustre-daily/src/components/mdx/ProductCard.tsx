"use client";

import Image from "next/image";
import { affiliateLink } from "@/lib/affiliate";
import { getProductByAsin } from "@/lib/products";

interface ProductCardProps {
  asin: string;
  // Optional overrides if product not in catalog
  name?: string;
  brand?: string;
  description?: string;
  whyWeLikeIt?: string;
  image?: string;
}

export function ProductCard({
  asin,
  name: nameProp,
  brand: brandProp,
  description: descriptionProp,
  whyWeLikeIt: whyProp,
  image: imageProp,
}: ProductCardProps) {
  // Try to get product from catalog
  const catalogProduct = getProductByAsin(asin);

  // Use props or fall back to catalog data
  const name = nameProp || catalogProduct?.name || "Product";
  const brand = brandProp || catalogProduct?.brand || "";
  const description = descriptionProp || catalogProduct?.shortDescription || "";
  const whyWeLikeIt = whyProp || catalogProduct?.whyWeLikeIt || "";
  const image = imageProp || catalogProduct?.image || "";
  const url = affiliateLink(asin);

  return (
    <div className="my-6 rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md dark:border-gray-700 dark:bg-gray-800">
      <div className="flex flex-col sm:flex-row sm:items-start sm:gap-4">
        {/* Product image */}
        <a
          href={url}
          target="_blank"
          rel="sponsored nofollow"
          className="mb-4 flex-shrink-0 sm:mb-0"
        >
          {image ? (
            <div className="relative h-28 w-28 overflow-hidden rounded-lg bg-white">
              <Image
                src={image}
                alt={name}
                fill
                className="object-contain p-2"
                sizes="112px"
              />
            </div>
          ) : (
            <div className="flex h-28 w-28 items-center justify-center rounded-lg bg-gradient-to-br from-pink-100 to-purple-100">
              <svg
                className="h-12 w-12 text-pink-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                />
              </svg>
            </div>
          )}
        </a>

        {/* Product info */}
        <div className="flex-grow">
          {brand && (
            <span className="text-xs font-medium uppercase tracking-wide text-pink-600 dark:text-pink-400">
              {brand}
            </span>
          )}
          <h4 className="mt-1 text-lg font-semibold text-gray-900 dark:text-white">
            <a
              href={url}
              target="_blank"
              rel="sponsored nofollow"
              className="hover:text-pink-600 dark:hover:text-pink-400 transition-colors"
            >
              {name}
            </a>
          </h4>
          {description && (
            <p className="mt-1 text-sm text-gray-600 dark:text-gray-300">
              {description}
            </p>
          )}
          {whyWeLikeIt && (
            <p className="mt-2 text-sm italic text-gray-500 dark:text-gray-400">
              <strong className="text-gray-700 dark:text-gray-200">Why we like it:</strong>{" "}
              {whyWeLikeIt}
            </p>
          )}
        </div>
      </div>

      {/* CTA Button */}
      <div className="mt-4 flex justify-end">
        <a
          href={url}
          target="_blank"
          rel="sponsored nofollow"
          className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-pink-500 to-purple-600 px-6 py-2 text-sm font-medium text-white transition-all hover:from-pink-600 hover:to-purple-700 hover:shadow-lg"
        >
          Check Price on Amazon
          <svg
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
            />
          </svg>
        </a>
      </div>
    </div>
  );
}

export default ProductCard;
