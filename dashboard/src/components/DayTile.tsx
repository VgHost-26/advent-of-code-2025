import { AsciiBox } from "@/components/ascii/ascii-box";
import { Stars } from "@/components/Stars";
import { Badge } from "@/components/ui/badge";
import { isStarted, padDay, shortLang, type AocDay } from "@/lib/data";
import { cn } from "@/lib/utils";

/** One calendar tile: a fixed-width framed box with day number as
 * title, the puzzle title, the star indicator and language badges. */
export function DayTile({
  day,
  selected,
  onSelect,
}: {
  day: AocDay;
  selected: boolean;
  onSelect: (day: number) => void;
}) {
  const started = isStarted(day);

  return (
    <button
      type="button"
      onClick={() => onSelect(day.day)}
      aria-current={selected}
      className={cn(
        "group/tile cursor-pointer px-0 py-0 text-left outline-none",
        !started && "opacity-55 transition-opacity hover:opacity-90",
      )}
    >
      <AsciiBox
        width={22}
        bg="bg-background"
        title={selected ? `> day ${padDay(day.day)}` : `day ${padDay(day.day)}`}
        contentClassName="flex min-h-[3lh] flex-col"
        data-selected={selected}
        /* CSS (.aoc-tile) halos the border glyphs: soft glow on hover,
         * strong glow on the selected tile — no box shadow. */
        className="aoc-tile"
      >
        <span
          title={day.title ?? undefined}
          className={cn(
            "truncate",
            started
              ? "text-card-foreground group-hover/tile:text-ascii-text"
              : "text-ascii-comment",
          )}
        >
          {day.title ?? "not started"}
        </span>
        <Stars count={day.stars} />
        <span className="flex flex-wrap gap-x-[1ch] whitespace-nowrap">
          {day.languages.map((lang) => (
            <Badge
              key={lang}
              variant={day.solutionsByLang[lang]?.completed ? "default" : "ghost"}
            >
              {shortLang(lang)}
            </Badge>
          ))}
        </span>
      </AsciiBox>
    </button>
  );
}
