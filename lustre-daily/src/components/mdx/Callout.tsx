import { cn } from "@/lib/utils";
import { ReactNode } from "react";

type CalloutType = "info" | "tip" | "warning" | "expert" | "note";

interface CalloutProps {
  type?: CalloutType;
  title?: string;
  children: ReactNode;
}

const calloutStyles: Record<CalloutType, { bg: string; border: string; icon: string; title: string }> = {
  info: {
    bg: "bg-blue-50 dark:bg-blue-950/30",
    border: "border-blue-200 dark:border-blue-800",
    icon: "💡",
    title: "Info",
  },
  tip: {
    bg: "bg-green-50 dark:bg-green-950/30",
    border: "border-green-200 dark:border-green-800",
    icon: "✨",
    title: "Pro Tip",
  },
  warning: {
    bg: "bg-amber-50 dark:bg-amber-950/30",
    border: "border-amber-200 dark:border-amber-800",
    icon: "⚠️",
    title: "Heads Up",
  },
  expert: {
    bg: "bg-purple-50 dark:bg-purple-950/30",
    border: "border-purple-200 dark:border-purple-800",
    icon: "👩‍🔬",
    title: "Expert Insight",
  },
  note: {
    bg: "bg-gray-50 dark:bg-gray-800/50",
    border: "border-gray-200 dark:border-gray-700",
    icon: "📝",
    title: "Note",
  },
};

export function Callout({ type = "info", title, children }: CalloutProps) {
  const styles = calloutStyles[type];
  const displayTitle = title || styles.title;

  return (
    <div
      className={cn(
        "my-6 rounded-lg border-l-4 p-4",
        styles.bg,
        styles.border
      )}
    >
      <div className="flex items-start gap-3">
        <span className="text-xl" role="img" aria-hidden="true">
          {styles.icon}
        </span>
        <div className="flex-grow">
          {displayTitle && (
            <p className="mb-2 font-semibold text-gray-900 dark:text-white">
              {displayTitle}
            </p>
          )}
          <div className="text-sm text-gray-700 dark:text-gray-300 [&>p]:m-0">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Callout;
