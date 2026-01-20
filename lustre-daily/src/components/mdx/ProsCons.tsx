interface ProsConsProps {
  pros: string[];
  cons: string[];
  title?: string;
}

export function ProsCons({ pros, cons, title }: ProsConsProps) {
  return (
    <div className="my-6 rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      {title && (
        <h4 className="mb-4 text-lg font-semibold text-gray-900 dark:text-white">
          {title}
        </h4>
      )}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Pros */}
        <div>
          <h5 className="mb-3 flex items-center gap-2 font-medium text-green-600 dark:text-green-400">
            <svg
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
            Pros
          </h5>
          <ul className="space-y-2">
            {pros.map((pro, index) => (
              <li key={index} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
                <span className="mt-1 text-green-500">+</span>
                {pro}
              </li>
            ))}
          </ul>
        </div>

        {/* Cons */}
        <div>
          <h5 className="mb-3 flex items-center gap-2 font-medium text-red-600 dark:text-red-400">
            <svg
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
            Cons
          </h5>
          <ul className="space-y-2">
            {cons.map((con, index) => (
              <li key={index} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
                <span className="mt-1 text-red-500">-</span>
                {con}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ProsCons;
