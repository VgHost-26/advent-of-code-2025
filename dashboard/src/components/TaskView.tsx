import type { AocDay } from "@/lib/data";

/** The scraped AoC article HTML rendered with .aoc-article styles. */
export function TaskView({ day }: { day: AocDay }) {
  if (!day.html) {
    return (
      <p className="py-[1lh] text-ascii-comment">
        no task description -- run <span className="text-primary">
        scripts/update_progress.py</span> to fetch it from adventofcode.com
      </p>
    );
  }
  return (
    <div
      className="aoc-article pb-[1lh]"
      dangerouslySetInnerHTML={{ __html: day.html }}
    />
  );
}
