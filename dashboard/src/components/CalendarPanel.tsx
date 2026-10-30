import { DayTile } from "@/components/DayTile";
import { type AocDay } from "@/lib/data";
import { ScrollArea } from "@/components/ui/scroll-area";

/** Scrollable calendar of DayTiles. */
export function CalendarPanel({
  days,
  selectedDay,
  onSelect,
  className,
}: {
  days: AocDay[];
  selectedDay: number | null;
  onSelect: (day: number) => void;
  className?: string;
}) {
  return (
    <ScrollArea className={className}>
      <div
        aria-label="Advent of Code 2025 calendar"
        className="grid auto-rows-min grid-cols-1 gap-x-[2ch] gap-y-[2lh] pt-[1lh] pb-[2lh] sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
      >
        {days.map((day) => (
          <DayTile
            key={day.day}
            day={day}
            selected={selectedDay === day.day}
            onSelect={onSelect}
          />
        ))}
      </div>
    </ScrollArea>
  );
}
