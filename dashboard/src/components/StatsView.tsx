"use client";

import { useEffect, useState } from "react";
import { benchStatus, fmtMs, type AocDay } from "@/lib/data";
import { cn } from "@/lib/utils";
import { DecoderText } from "@/components/DecoderText";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

const PARTS: string[] = ["1", "2"];
const PART_LABEL: Record<string, string> = { "1": "part 1", "2": "part 2" };

/** Spoiler-shrouded answer: hover previews the interaction, click toggles. */
function SpoilerAnswer({
  answer,
  mismatch,
  revealed,
  onToggle,
}: {
  answer: string;
  mismatch: boolean;
  revealed: boolean;
  onToggle: () => void;
}) {
  return (
    <Tooltip>
      <TooltipTrigger render={<span />}>
        <button
          type="button"
          onClick={onToggle}
          aria-pressed={revealed}
          aria-label={
            mismatch
              ? `spoiler, answers disagree -- click to ${revealed ? "hide" : "reveal"}`
              : `spoiler -- click to ${revealed ? "hide" : "reveal"} answer`
          }
          className="cursor-pointer select-none"
        >
          <DecoderText
            text={answer}
            revealed={revealed}
            className={cn(revealed && "text-ascii-primary")}
          />
        </button>
      </TooltipTrigger>
      <TooltipContent side="right" chWidth={10}>
        {revealed ? "Hide" : "Reveal"} answer
      </TooltipContent>
    </Tooltip>
  );
}

/** Benchmark results from benchmarks.json: one row per language/part. */
export function StatsView({ day }: { day: AocDay }) {
  const rows = day.languages.flatMap((lang) =>
    PARTS.map((part) => ({
      lang,
      part,
      bench: day.benchmarksByLang?.[lang]?.[part] ?? null,
    })),
  );

  const empty = rows.every(({ bench }) => bench === null);
  const [revealed, setRevealed] = useState<Set<string>>(new Set());

  // Day switches re-cover answers; re-revealing replays the decoder effect.
  useEffect(() => setRevealed(new Set()), [day.day]);

  const togglePart = (part: string) =>
    setRevealed((prev) => {
      const next = new Set(prev);
      if (next.has(part)) {
        next.delete(part);
      } else {
        next.add(part);
      }
      return next;
    });

  return (
    <div className="flex flex-col gap-y-[1lh] py-[1lh]">
      <div className="flex text-ascii-comment uppercase">
        <span className="w-[10ch]">lang</span>
        <span className="w-[9ch]">part</span>
        <span className="w-[12ch]">time</span>
        <span className="hidden flex-1 md:block">answer</span>
      </div>
      {rows.length === 0 ? (
        <p className="text-ascii-comment">no solutions to benchmark yet</p>
      ) : empty ? (
        <p className="text-ascii-comment">
          not benchmarked yet -- run scripts/benchmark.py
        </p>
      ) : (
        rows.map(({ lang, part, bench }) => {
          const status = benchStatus(day, part);
          return (
            <div key={`${lang}-${part}`} className="flex items-center">
              <span className="w-[10ch] text-ascii-soft">{lang}</span>
              <span className="w-[9ch]">{PART_LABEL[part]}</span>
              <span className="w-[12ch] text-ascii-primary">
                {bench ? (
                  <Tooltip>
                    <TooltipTrigger render={<span />}>
                      {fmtMs(bench.median_ms)}
                    </TooltipTrigger>
                    <TooltipContent>
                      min {fmtMs(bench.min_ms)} ({bench.runs} runs)
                    </TooltipContent>
                  </Tooltip>
                ) : (
                  <span className="text-ascii-comment">--</span>
                )}
              </span>
              <span
                className={cn(
                  "hidden flex-1 md:block text-ascii-comment",
                  status === "mismatch" ? "text-destructive" : "",
                )}
              >
                {bench ? (
                  <>
                    {status === "mismatch" ? "mismatch: " : "= "}
                    <SpoilerAnswer
                      answer={bench.answer}
                      mismatch={status === "mismatch"}
                      revealed={revealed.has(part)}
                      onToggle={() => togglePart(part)}
                    />
                  </>
                ) : (
                  "not benchmarked"
                )}
              </span>
            </div>
          );
        })
      )}
      <p className="text-ascii-comment">
        medians over {day.languages.length} solution
        {day.languages.length === 1 ? "" : "s"}; parse excluded from timing,
        per-run minimum in tooltip
      </p>
    </div>
  );
}
