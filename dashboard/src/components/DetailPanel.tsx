import * as React from "react";

import { AsciiBox, AsciiBoxDivider } from "@/components/ascii/ascii-box";
import { Badge } from "@/components/ui/badge";
import { Empty, EmptyDescription, EmptyMedia, EmptyTitle } from "@/components/ui/empty";
import { Stars } from "@/components/Stars";
import { SolutionView } from "@/components/SolutionView";
import { StatsView } from "@/components/StatsView";
import { TaskView } from "@/components/TaskView";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { Button } from "@/components/ui/button";
import { aocUrl, padDay, type AocDay } from "@/lib/data";

type DetailTab = "task" | "solutions" | "stats";

/** Right-hand panel for the selected day. Everything except the tab
 * panels is fixed: the box header (stars, badges, close button) and
 * the tab strip stay put while each tab's content scrolls inside the
 * box. Renders a centered Empty state when nothing is selected. */
export function DetailPanel({
  day,
  onClear,
}: {
  day: AocDay | null;
  onClear?: () => void;
}) {
  const [tab, setTab] = React.useState<DetailTab>("task");

  if (!day) {
    return (
      <div className="flex h-full items-center justify-center">
        <AsciiBox fluid width={46} title="details" padY={1} className="w-[46ch]">
          <Empty className="min-h-[8lh] justify-center">
            <EmptyMedia>
              <span>[ ? ]</span>
            </EmptyMedia>
            <EmptyTitle>no day selected</EmptyTitle>
            <EmptyDescription>
              pick a day from the calendar -- gold "*" markers show earned
              stars, bracketed badges list solved languages
            </EmptyDescription>
          </Empty>
        </AsciiBox>
      </div>
    );
  }

  const hasSolutions = day.languages.length > 0;

  return (
    <div className="flex h-full min-w-0 flex-col">
      <AsciiBox
        fluid
        fill
        width={46}
        title={`day ${padDay(day.day)} ${day.title ? `-- ${day.title.toLowerCase()}` : ""}`}
        className="flex min-h-0 flex-1 flex-col"
        contentClassName="flex min-w-0 flex-1 flex-col"
      >
        {/* Fixed header row: stars, language badges, close. */}
        <div className="flex flex-wrap items-center justify-between gap-x-[4ch] gap-y-[1lh]">
          <Tooltip>
            <TooltipTrigger
              render={<span className="text-sm" aria-label={`${day.stars} of 2 stars`} />}
            >
              <Stars count={day.stars} className="text-[1.25em]" />
            </TooltipTrigger>
            <TooltipContent chWidth={16} side="bottom">
              {day.stars} / 2 solved
            </TooltipContent>
          </Tooltip>
          <span className="flex flex-wrap gap-x-[1ch]">
            {day.languages.map((lang) => (
              <Badge
                key={lang}
                variant={day.solutionsByLang[lang]?.completed ? "default" : "ghost"}
              >
                {lang}
              </Badge>
            ))}
          </span>
          {onClear ? (
            <Button variant="ghost" onClick={onClear} className="shrink-0">
              <span className="text-primary">[x]</span> close
            </Button>
          ) : null}
        </div>

        <AsciiBoxDivider pad={false} />

        {/* Tab strip is fixed; only the panel below scrolls. */}
        <Tabs
          key={day.day}
          value={tab}
          onValueChange={setTab}
          className="flex min-h-0 min-w-0 flex-1 flex-col"
        >
          <TabsList className="shrink-0">
            <TabsTrigger value="task">task</TabsTrigger>
            <TabsTrigger value="solutions" disabled={!hasSolutions}>
              solutions
            </TabsTrigger>
            <TabsTrigger value="stats" disabled={!hasSolutions}>
              stats
            </TabsTrigger>
          </TabsList>
          <TabsContent value="task" className="min-h-0">
            <ScrollArea className="h-full">
              <div className="pb-[1lh]">
                <TaskView day={day} />
                <a
                  href={aocUrl(day.day)}
                  target="_blank"
                  rel="noreferrer"
                  className="text-primary hover:text-ascii-text"
                >
                  &gt;&gt; read on adventofcode.com
                </a>
              </div>
            </ScrollArea>
          </TabsContent>
          <TabsContent value="solutions" className="min-h-0">
            <ScrollArea className="h-full">
              <div className="pb-[1lh]">
                <SolutionView day={day} />
              </div>
            </ScrollArea>
          </TabsContent>
          <TabsContent value="stats" className="min-h-0">
            <ScrollArea className="h-full">
              <div className="pb-[1lh]">
                <StatsView day={day} />
              </div>
            </ScrollArea>
          </TabsContent>
        </Tabs>
      </AsciiBox>
    </div>
  );
}
