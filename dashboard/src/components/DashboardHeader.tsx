import { Badge } from "@/components/ui/badge";
import { AsciiRule } from "@/components/ascii/ascii-box";
import { languageCounts, totalStars, TOTAL_STARS, AUTHOR_URL } from "@/lib/data";
import { Progress } from "@/components/ui/progress";
export function DashboardHeader() {
  return (
    <header className="flex flex-col px-[2ch] pt-[1lh]">
      <div className="flex flex-col items-start justify-between gap-x-[4ch] gap-y-[1lh] sm:flex-row sm:items-center">
        <div>
          <h1
            className="font-heading text-primary"
            style={{ textShadow: "var(--ascii-glow)" }}
          >
            Advent of Code 2025
          </h1>
          <p className="text-ascii-comment">
            <a
              href={AUTHOR_URL}
              target="_blank"
              rel="noreferrer"
              className="hover:text-shadow-[0_0_8px] text-aoc-star"
            >
              VgHost-26
            </a>{" "}
            progress dashboard
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-x-[3ch] gap-y-[1lh]">
          <Progress
            min={0}
            max={TOTAL_STARS}
            value={totalStars}
            barWidth={14}
            label={
              <span>
                {totalStars} / {TOTAL_STARS}{" "}
                <span aria-hidden className="font-heading text-aoc-star">
                  *
                </span>
              </span>
            }
          />
          <div className="flex items-center gap-x-[1ch]">
            {languageCounts.map(({ lang, count }) => (
              <Badge key={lang} variant="ghost">
                <span>{lang}</span>
                <span className="text-primary">{count}</span>
              </Badge>
            ))}
          </div>
          <span className="hidden text-ascii-comment xl:inline">
            [↑↓] select day <span aria-hidden>--</span> [esc] close
          </span>
        </div>
      </div>
      {/* On wide screens the rule stops short of the details panel so
           the panel's top border continues the same line to the right
           edge (the aside is pulled up by one row to meet it). */}
      <AsciiRule className="mt-[1lh] w-full " />
    </header>
  );
}
