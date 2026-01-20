import { siteConfig } from "@/site.config";

/**
 * Generates an Amazon affiliate link with the configured associate tag.
 * Link format: https://www.amazon.com/dp/{ASIN}/?tag={TAG}
 *
 * @param asin - Amazon Standard Identification Number
 * @returns Formatted affiliate link
 */
export function affiliateLink(asin: string): string {
  const tag = siteConfig.amazonAssociateTag;
  return `https://www.amazon.com/dp/${asin}/?tag=${tag}`;
}

/**
 * Checks if a URL is an Amazon affiliate link
 */
export function isAmazonLink(url: string): boolean {
  return url.includes("amazon.com");
}

/**
 * Extracts ASIN from an Amazon URL
 */
export function extractAsin(url: string): string | null {
  // Matches /dp/ASIN or /gp/product/ASIN patterns
  const match = url.match(/\/(?:dp|gp\/product)\/([A-Z0-9]{10})/i);
  return match ? match[1] : null;
}

/**
 * Standard affiliate disclosure text (short version for post headers)
 */
export const shortDisclosure =
  "This post contains affiliate links. As an Amazon Associate I earn from qualifying purchases.";

/**
 * Full affiliate disclosure text
 */
export const fullDisclosure = `
## Affiliate Disclosure

${siteConfig.name} is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com.

When you click on links to various merchants on this site and make a purchase, this can result in this site earning a commission. Affiliate programs and affiliations include, but are not limited to, the Amazon Associates Program.

We only recommend products we genuinely believe in and have thoroughly researched. Our editorial opinions are our own and are not influenced by any advertiser or commercial partnerships.

**Please note:** We do not guarantee specific prices as Amazon prices fluctuate. Always check the current price on Amazon before purchasing.
`.trim();

/**
 * Footer disclosure (required by Amazon Associates)
 */
export const footerDisclosure =
  "As an Amazon Associate I earn from qualifying purchases.";
