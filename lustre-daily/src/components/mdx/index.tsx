import { ProductCard } from "./ProductCard";
import { Callout } from "./Callout";
import { ProsCons } from "./ProsCons";
import { RoutineSteps, Step } from "./RoutineSteps";
import { AffiliateDisclosure } from "./AffiliateDisclosure";
import { TableOfContents } from "./TableOfContents";
import Link from "next/link";
import Image from "next/image";

// Custom link component with affiliate handling
function CustomLink({
  href,
  children,
  ...props
}: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href?: string }) {
  const isAmazonLink = href?.includes("amazon.com");
  const isInternalLink = href?.startsWith("/") || href?.startsWith("#");

  if (isInternalLink && href) {
    return (
      <Link href={href} {...props}>
        {children}
      </Link>
    );
  }

  return (
    <a
      href={href}
      target="_blank"
      rel={isAmazonLink ? "sponsored nofollow" : "noopener noreferrer"}
      className="text-pink-600 hover:underline dark:text-pink-400"
      {...props}
    >
      {children}
    </a>
  );
}

// Custom image component
function CustomImage({
  src,
  alt,
  ...props
}: React.ImgHTMLAttributes<HTMLImageElement>) {
  if (!src || typeof src !== "string") return null;

  // Handle external images
  if (src.startsWith("http")) {
    return (
      <figure className="my-6">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={src}
          alt={alt || ""}
          className="mx-auto rounded-lg shadow-md"
          loading="lazy"
          {...props}
        />
        {alt && (
          <figcaption className="mt-2 text-center text-sm text-gray-500 dark:text-gray-400">
            {alt}
          </figcaption>
        )}
      </figure>
    );
  }

  // Handle local images with Next.js Image
  return (
    <figure className="my-6">
      <Image
        src={src}
        alt={alt || ""}
        width={800}
        height={450}
        className="mx-auto rounded-lg shadow-md"
        {...(props as object)}
      />
      {alt && (
        <figcaption className="mt-2 text-center text-sm text-gray-500 dark:text-gray-400">
          {alt}
        </figcaption>
      )}
    </figure>
  );
}

// MDX component mapping
export const mdxComponents = {
  // Custom components
  ProductCard,
  Callout,
  ProsCons,
  RoutineSteps,
  Step,
  AffiliateDisclosure,
  TableOfContents,

  // Override default HTML elements
  a: CustomLink,
  img: CustomImage,

  // Enhanced headings with anchor links
  h1: ({ children, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => {
    const id = children?.toString().toLowerCase().replace(/\s+/g, "-");
    return (
      <h1 id={id} className="scroll-mt-24" {...props}>
        {children}
      </h1>
    );
  },
  h2: ({ children, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => {
    const id = children?.toString().toLowerCase().replace(/\s+/g, "-");
    return (
      <h2 id={id} className="scroll-mt-24" {...props}>
        <a href={`#${id}`} className="no-underline hover:underline">
          {children}
        </a>
      </h2>
    );
  },
  h3: ({ children, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => {
    const id = children?.toString().toLowerCase().replace(/\s+/g, "-");
    return (
      <h3 id={id} className="scroll-mt-24" {...props}>
        <a href={`#${id}`} className="no-underline hover:underline">
          {children}
        </a>
      </h3>
    );
  },

  // Enhanced blockquote
  blockquote: ({ children, ...props }: React.BlockquoteHTMLAttributes<HTMLQuoteElement>) => (
    <blockquote
      className="my-6 border-l-4 border-pink-300 bg-pink-50 py-4 pl-4 pr-4 italic text-gray-700 dark:border-pink-700 dark:bg-pink-950/20 dark:text-gray-300"
      {...props}
    >
      {children}
    </blockquote>
  ),

  // Enhanced code blocks
  pre: ({ children, ...props }: React.HTMLAttributes<HTMLPreElement>) => (
    <pre
      className="my-6 overflow-x-auto rounded-lg bg-gray-900 p-4 text-sm text-gray-100"
      {...props}
    >
      {children}
    </pre>
  ),
  code: ({ children, ...props }: React.HTMLAttributes<HTMLElement>) => (
    <code
      className="rounded bg-gray-100 px-1.5 py-0.5 text-sm text-pink-600 dark:bg-gray-800 dark:text-pink-400"
      {...props}
    >
      {children}
    </code>
  ),

  // Enhanced table
  table: ({ children, ...props }: React.TableHTMLAttributes<HTMLTableElement>) => (
    <div className="my-6 overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700" {...props}>
        {children}
      </table>
    </div>
  ),
  th: ({ children, ...props }: React.ThHTMLAttributes<HTMLTableCellElement>) => (
    <th
      className="bg-gray-50 px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:bg-gray-800 dark:text-white"
      {...props}
    >
      {children}
    </th>
  ),
  td: ({ children, ...props }: React.TdHTMLAttributes<HTMLTableCellElement>) => (
    <td
      className="border-t border-gray-200 px-4 py-3 text-sm text-gray-600 dark:border-gray-700 dark:text-gray-300"
      {...props}
    >
      {children}
    </td>
  ),
};

// Export individual components for direct use
export {
  ProductCard,
  Callout,
  ProsCons,
  RoutineSteps,
  Step,
  AffiliateDisclosure,
  TableOfContents,
};
