import { AOC_HOME, AUTHOR_URL } from "@/lib/data";

/** Bottom line: dimmed byline, no ruler above it. */
export function DashboardFooter() {
  return (
    <footer className="pb-[.5lh] pt-[1lh] text-ascii-comment flex justify-between gap-1">
      <span>
        Puzzles by{" "}
        <a
          href={AOC_HOME}
          target="_blank"
          rel="noreferrer"
          className="hover:text-primary-hover text-primary"
        >
          adventofcode.com
        </a>{" "}
      </span>

      <span>
        Made by{" "}
        <a
          href={AUTHOR_URL}
          target="_blank"
          rel="noreferrer"
          className="hover:text-primary-hover text-primary"
        >
          VgHost-26
        </a>
      </span>
      <span className="text-[.9em]">
        Big shoutout to{" "}
        <a
          href="https://github.com/ekmas/cnlibs"
          target="_blank"
          rel="noreferrer"
          className="hover:text-primary-hover text-primary"
        >
          ekmas
        </a>{" "}
        for ASCII components
      </span>
    </footer>
  );
}
