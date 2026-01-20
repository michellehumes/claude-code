import fs from "fs";
import path from "path";
import { affiliateLink } from "./affiliate";

const productsPath = path.join(process.cwd(), "content/products/products.json");

export interface Product {
  asin: string;
  name: string;
  brand: string;
  category: "makeup" | "hair" | "skincare";
  image?: string;
  shortDescription: string;
  whyWeLikeIt: string;
  tags: string[];
}

export interface ProductWithLink extends Product {
  affiliateUrl: string;
}

let productsCache: Product[] | null = null;

/**
 * Load products from JSON file
 */
export function loadProducts(): Product[] {
  if (productsCache !== null) {
    return productsCache;
  }

  if (!fs.existsSync(productsPath)) {
    console.warn("Products file not found at:", productsPath);
    return [];
  }

  const fileContents = fs.readFileSync(productsPath, "utf8");
  const data = JSON.parse(fileContents);
  const products: Product[] = data.products || [];
  productsCache = products;
  return products;
}

/**
 * Get a product by ASIN
 */
export function getProductByAsin(asin: string): ProductWithLink | null {
  const products = loadProducts();
  const product = products.find((p) => p.asin === asin);

  if (!product) {
    return null;
  }

  return {
    ...product,
    affiliateUrl: affiliateLink(asin),
  };
}

/**
 * Get products by category
 */
export function getProductsByCategory(category: string): ProductWithLink[] {
  const products = loadProducts();
  return products
    .filter((p) => p.category === category)
    .map((p) => ({
      ...p,
      affiliateUrl: affiliateLink(p.asin),
    }));
}

/**
 * Get products by tag
 */
export function getProductsByTag(tag: string): ProductWithLink[] {
  const products = loadProducts();
  return products
    .filter((p) => p.tags.map((t) => t.toLowerCase()).includes(tag.toLowerCase()))
    .map((p) => ({
      ...p,
      affiliateUrl: affiliateLink(p.asin),
    }));
}

/**
 * Get products by brand
 */
export function getProductsByBrand(brand: string): ProductWithLink[] {
  const products = loadProducts();
  return products
    .filter((p) => p.brand.toLowerCase() === brand.toLowerCase())
    .map((p) => ({
      ...p,
      affiliateUrl: affiliateLink(p.asin),
    }));
}

/**
 * Get random products from a category (for generating content)
 */
export function getRandomProducts(
  category: string,
  count: number,
  excludeAsins: string[] = []
): ProductWithLink[] {
  const products = loadProducts();
  const filtered = products.filter(
    (p) => p.category === category && !excludeAsins.includes(p.asin)
  );

  // Fisher-Yates shuffle
  const shuffled = [...filtered];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }

  return shuffled.slice(0, count).map((p) => ({
    ...p,
    affiliateUrl: affiliateLink(p.asin),
  }));
}

/**
 * Search products by name or description
 */
export function searchProducts(query: string): ProductWithLink[] {
  const products = loadProducts();
  const lowerQuery = query.toLowerCase();

  return products
    .filter(
      (p) =>
        p.name.toLowerCase().includes(lowerQuery) ||
        p.shortDescription.toLowerCase().includes(lowerQuery) ||
        p.brand.toLowerCase().includes(lowerQuery)
    )
    .map((p) => ({
      ...p,
      affiliateUrl: affiliateLink(p.asin),
    }));
}

/**
 * Get all unique brands
 */
export function getAllBrands(): string[] {
  const products = loadProducts();
  const brandSet = new Set<string>();
  products.forEach((p) => brandSet.add(p.brand));
  return Array.from(brandSet).sort();
}

/**
 * Get all unique product tags
 */
export function getAllProductTags(): string[] {
  const products = loadProducts();
  const tagSet = new Set<string>();
  products.forEach((p) => p.tags.forEach((t) => tagSet.add(t)));
  return Array.from(tagSet).sort();
}

/**
 * Validate that an ASIN exists in the catalog
 */
export function validateAsin(asin: string): boolean {
  const products = loadProducts();
  return products.some((p) => p.asin === asin);
}

/**
 * Clear the products cache (for testing)
 */
export function clearProductsCache(): void {
  productsCache = null;
}
