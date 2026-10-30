import * as React from "react";

import { CalendarPanel } from "@/components/CalendarPanel";
import { DashboardFooter } from "@/components/DashboardFooter";
import { DashboardHeader } from "@/components/DashboardHeader";
import { DetailPanel } from "@/components/DetailPanel";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { dayByNumber, days, padDay, TOTAL_DAYS } from "@/lib/data";
import { useMediaQuery } from "@/hooks/use-media-query";

function dayFromUrl(): number | null {
  const param = new URLSearchParams(window.location.search).get("day");
  if (!param) return null;
  const n = Number.parseInt(param, 10);
  return Number.isInteger(n) && n >= 1 && n <= TOTAL_DAYS ? n : null;
}

export default function App() {
  const isWide = useMediaQuery("(min-width: 1280px)");
  const [selectedDay, setSelectedDay] = React.useState<number | null>(
    dayFromUrl,
  );
  const [sheetOpen, setSheetOpen] = React.useState(false);

  const day = dayByNumber(selectedDay ?? 0);

  // Keep ?day= in the URL so a selected day can be shared/bookmarked.
  React.useEffect(() => {
    const url = new URL(window.location.href);
    if (selectedDay == null) {
      url.searchParams.delete("day");
    } else {
      url.searchParams.set("day", String(selectedDay));
    }
    window.history.replaceState({}, "", url);
  }, [selectedDay]);

  // Esc clears the selection, arrows walk through the days.
  React.useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setSheetOpen(false);
        setSelectedDay(null);
        return;
      }
      if (
        !["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(event.key)
      ) {
        return;
      }
      event.preventDefault();
      setSelectedDay((current) => {
        if (current == null) return days[0].day;
        const step =
          event.key === "ArrowUp" || event.key === "ArrowLeft" ? -1 : 1;
        return Math.min(TOTAL_DAYS, Math.max(1, current + step));
      });
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const handleSelect = (d: number) => {
    setSelectedDay(d);
    if (!isWide) {
      setSheetOpen(true);
    }
  };

  return (
    <div className="flex h-dvh flex-col overflow-hidden">
      <DashboardHeader />
      <main className="flex min-h-0 flex-1 gap-x-[3ch] px-[2ch]">
        {/* Footer lives inside the calendar column, so the details
         * panel runs past it to the viewport's bottom edge. */}
        <div className="flex min-h-0 min-w-0 flex-1 flex-col">
          <CalendarPanel
            days={days}
            selectedDay={selectedDay}
            onSelect={handleSelect}
            className="min-h-0 min-w-0 flex-1"
          />
          <DashboardFooter />
        </div>
        {/* Pulled up one row so the panel's top border sits on the
         * header rule's line (empty space above the rule is where the
         * calendar breathes — see CalendarPanel's top padding). */}
        <aside className="hidden min-h-0 shrink-0 xl:block xl:mt-[-1lh] xl:w-[64ch]">
          <DetailPanel day={day} onClear={() => setSelectedDay(null)} />
        </aside>
      </main>

      {/* Narrow screens: the details panel opens as a slide-over. */}
      <Sheet open={sheetOpen} onOpenChange={setSheetOpen}>
        <SheetContent side="right" className="w-[92vw] p-0 sm:max-w-[66ch]">
          <SheetHeader>
            <SheetTitle className="sr-only">
              {day ? `day ${padDay(day.day)}` : "day details"}
            </SheetTitle>
          </SheetHeader>
          <div className="flex min-h-0 flex-1 flex-col py-[1lh]">
            <DetailPanel
              day={day}
              onClear={() => {
                setSheetOpen(false);
                setSelectedDay(null);
              }}
            />
          </div>
        </SheetContent>
      </Sheet>
    </div>
  );
}
