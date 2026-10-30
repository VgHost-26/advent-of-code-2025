import { AOC_HOME, AUTHOR_URL } from "@/lib/data";

/** Bottom line: dimmed byline, no ruler above it. */
export function DashboardFooter() {
  return (
    <footer className="px-[0ch] pb-[.5lh] pt-[1lh] text-ascii-comment flex justify-center gap-1">
      <div className="">
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
      </div>

      <div className="grow w-ful flex flex-col items-center justify-center">
        <span>
          Made with passion by{" "}
          <a
            href={AUTHOR_URL}
            target="_blank"
            rel="noreferrer"
            className="hover:text-primary-hover text-primary"
          >
            VgHost-26
          </a>
        </span>
      </div>
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
        for those ASCII components
      </span>
    </footer>
  );
}
