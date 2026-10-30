import { cn } from "@/lib/utils";

/** Gold "*" star indicator — filled for earned stars, dimmed for
 * missing ones. Plain asterisks, rendered with the aoc-star token. */
export function Stars({
  count,
  max = 2,
  className,
}: {
  count: number;
  max?: number;
  className?: string;
}) {
  const earned = Math.min(Math.max(count, 0), max);
  return (
    <span
      aria-label={`${earned} of ${max} stars`}
      className={cn("select-none leading-none", className)}
    >
      {Array.from({ length: max }, (_, i) => (
        <span
          key={i}
          aria-hidden
          className={cn(
            i < earned
              ? "font-heading text-aoc-star"
              : "text-ascii-comment/40"
          )}
        >
          *
        </span>
      ))}
    </span>
  );
}
