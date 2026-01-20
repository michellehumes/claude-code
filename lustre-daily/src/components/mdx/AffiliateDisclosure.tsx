import { shortDisclosure } from "@/lib/affiliate";
import Link from "next/link";

interface AffiliateDisclosureProps {
  short?: boolean;
}

export function AffiliateDisclosure({ short = true }: AffiliateDisclosureProps) {
  if (short) {
    return (
      <div className="mb-6 rounded-lg border border-pink-100 bg-pink-50 px-4 py-3 text-sm text-gray-600 dark:border-pink-900/30 dark:bg-pink-950/20 dark:text-gray-400">
        <p>
          {shortDisclosure}{" "}
          <Link
            href="/affiliate-disclosure"
            className="font-medium text-pink-600 hover:underline dark:text-pink-400"
          >
            Learn more
          </Link>
        </p>
      </div>
    );
  }

  return (
    <div className="my-8 rounded-lg border border-gray-200 bg-gray-50 p-6 dark:border-gray-700 dark:bg-gray-800">
      <h3 className="mb-3 flex items-center gap-2 text-lg font-semibold text-gray-900 dark:text-white">
        <svg
          className="h-5 w-5 text-pink-500"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        Affiliate Disclosure
      </h3>
      <p className="text-sm text-gray-600 dark:text-gray-300">
        {shortDisclosure} We only recommend products we genuinely believe in.
        Prices may vary and we encourage you to verify current pricing on
        Amazon before purchasing.{" "}
        <Link
          href="/affiliate-disclosure"
          className="font-medium text-pink-600 hover:underline dark:text-pink-400"
        >
          Read our full disclosure policy
        </Link>
      </p>
    </div>
  );
}

export default AffiliateDisclosure;
