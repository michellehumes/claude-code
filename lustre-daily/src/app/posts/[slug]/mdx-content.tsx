"use client";

import { useMemo } from "react";
import { mdxComponents } from "@/components/mdx";
import { MDXRemote } from "next-mdx-remote";
import { serialize } from "next-mdx-remote/serialize";
import remarkGfm from "remark-gfm";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";

interface MDXContentProps {
  content: string;
}

// Simple client-side MDX rendering
export function MDXContent({ content }: MDXContentProps) {
  // Parse and render MDX content
  const processedContent = useMemo(() => {
    return processMarkdown(content);
  }, [content]);

  return <div dangerouslySetInnerHTML={{ __html: processedContent }} />;
}

// Simple markdown to HTML processor
function processMarkdown(content: string): string {
  let html = content;

  // Remove frontmatter
  html = html.replace(/^---[\s\S]*?---\n*/m, "");

  // Process ProductCard components - extract all attributes
  html = html.replace(
    /<ProductCard([^>]+)\/>/g,
    (_, attrs) => {
      // Extract attributes
      const asin = attrs.match(/asin="([^"]+)"/)?.[1] || "";
      const name = attrs.match(/name="([^"]+)"/)?.[1] || "Product";
      const brand = attrs.match(/brand="([^"]+)"/)?.[1] || "";
      const description = attrs.match(/description="([^"]+)"/)?.[1] || "";
      const whyWeLikeIt = attrs.match(/whyWeLikeIt="([^"]+)"/)?.[1] || "";
      const image = attrs.match(/image="([^"]+)"/)?.[1] || "";

      const tag = "shelzysbeauty-20";
      const url = `https://www.amazon.com/dp/${asin}/?tag=${tag}`;

      const imageHtml = image
        ? `<img src="${image}" alt="${name}" class="h-28 w-28 object-contain p-2 rounded-lg bg-white" loading="lazy" />`
        : `<div class="flex h-28 w-28 items-center justify-center rounded-lg bg-gradient-to-br from-pink-100 to-purple-100">
            <svg class="h-12 w-12 text-pink-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
            </svg>
          </div>`;

      return `
        <div class="my-6 rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md dark:border-gray-700 dark:bg-gray-800">
          <div class="flex flex-col sm:flex-row sm:items-start sm:gap-4">
            <a href="${url}" target="_blank" rel="sponsored nofollow" class="mb-4 flex-shrink-0 sm:mb-0">
              ${imageHtml}
            </a>
            <div class="flex-grow">
              ${brand ? `<span class="text-xs font-medium uppercase tracking-wide text-pink-600 dark:text-pink-400">${brand}</span>` : ""}
              <h4 class="mt-1 text-lg font-semibold text-gray-900 dark:text-white">
                <a href="${url}" target="_blank" rel="sponsored nofollow" class="hover:text-pink-600 dark:hover:text-pink-400 transition-colors">${name}</a>
              </h4>
              ${description ? `<p class="mt-1 text-sm text-gray-600 dark:text-gray-300">${description}</p>` : ""}
              ${whyWeLikeIt ? `<p class="mt-2 text-sm italic text-gray-500 dark:text-gray-400"><strong class="text-gray-700 dark:text-gray-200">Why we like it:</strong> ${whyWeLikeIt}</p>` : ""}
            </div>
          </div>
          <div class="mt-4 flex justify-end">
            <a href="${url}" target="_blank" rel="sponsored nofollow" class="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-pink-500 to-purple-600 px-6 py-2 text-sm font-medium text-white transition-all hover:from-pink-600 hover:to-purple-700 hover:shadow-lg">
              Check Price on Amazon
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
              </svg>
            </a>
          </div>
        </div>
      `;
    }
  );

  // Process Callout components
  html = html.replace(
    /<Callout(?:\s+type="([^"]*)")?(?:\s+title="([^"]*)")?\s*>([\s\S]*?)<\/Callout>/g,
    (_, type = "info", title, content) => {
      const icons: Record<string, string> = {
        info: "💡",
        tip: "✨",
        warning: "⚠️",
        expert: "👩‍🔬",
        note: "📝",
      };
      const bgColors: Record<string, string> = {
        info: "bg-blue-50 dark:bg-blue-950/30 border-blue-200 dark:border-blue-800",
        tip: "bg-green-50 dark:bg-green-950/30 border-green-200 dark:border-green-800",
        warning: "bg-amber-50 dark:bg-amber-950/30 border-amber-200 dark:border-amber-800",
        expert: "bg-purple-50 dark:bg-purple-950/30 border-purple-200 dark:border-purple-800",
        note: "bg-gray-50 dark:bg-gray-800/50 border-gray-200 dark:border-gray-700",
      };
      return `
        <div class="my-6 rounded-lg border-l-4 p-4 ${bgColors[type] || bgColors.info}">
          <div class="flex items-start gap-3">
            <span class="text-xl">${icons[type] || icons.info}</span>
            <div class="flex-grow">
              ${title ? `<p class="mb-2 font-semibold text-gray-900 dark:text-white">${title}</p>` : ""}
              <div class="text-sm text-gray-700 dark:text-gray-300">${content.trim()}</div>
            </div>
          </div>
        </div>
      `;
    }
  );

  // Process headings
  html = html.replace(/^### (.+)$/gm, (_, text) => {
    const id = text.toLowerCase().replace(/[^\w\s-]/g, "").replace(/\s+/g, "-");
    return `<h3 id="${id}" class="scroll-mt-24 mt-8 mb-4 text-xl font-bold text-gray-900 dark:text-white">${text}</h3>`;
  });
  html = html.replace(/^## (.+)$/gm, (_, text) => {
    const id = text.toLowerCase().replace(/[^\w\s-]/g, "").replace(/\s+/g, "-");
    return `<h2 id="${id}" class="scroll-mt-24 mt-10 mb-4 text-2xl font-bold text-gray-900 dark:text-white">${text}</h2>`;
  });

  // Process bold and italic
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");

  // Process links
  html = html.replace(
    /\[([^\]]+)\]\(([^)]+)\)/g,
    (_, text, url) => {
      const isAmazon = url.includes("amazon.com");
      const rel = isAmazon ? 'rel="sponsored nofollow"' : 'rel="noopener noreferrer"';
      return `<a href="${url}" target="_blank" ${rel} class="text-pink-600 hover:underline dark:text-pink-400">${text}</a>`;
    }
  );

  // Process lists
  html = html.replace(/^- (.+)$/gm, "<li class=\"ml-4 list-disc text-gray-700 dark:text-gray-300\">$1</li>");
  html = html.replace(/(<li[^>]*>.*<\/li>\n?)+/g, "<ul class=\"my-4 space-y-2\">$&</ul>");

  // Process paragraphs
  html = html.replace(/^(?!<[a-z]|#|\s*$)(.+)$/gm, "<p class=\"my-4 text-gray-700 dark:text-gray-300 leading-relaxed\">$1</p>");

  // Clean up extra whitespace
  html = html.replace(/\n{3,}/g, "\n\n");

  return html;
}
