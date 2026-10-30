import * as React from "react";

import { CodeViewer } from "@/components/CodeViewer";
import { Button } from "@/components/ui/button";
import { Toggle } from "@/components/ui/toggle";
import { ToggleGroup } from "@/components/ui/toggle-group";
import {
  LANGUAGES,
  shortLang,
  type AocDay,
  type Language,
} from "@/lib/data";

const FILE_EXTENSIONS: Record<string, string> = {
  python: "py",
  go: "go",
  cpp: "cpp",
};

/** Language switcher + code viewer for one day's solutions. */
export function SolutionView({ day }: { day: AocDay }) {
  const available = React.useMemo<Language[]>(
    () => LANGUAGES.filter((lang) => day.solutionsByLang[lang]),
    [day],
  );
  const [selected, setSelected] = React.useState<Language | null>(
    available[0] ?? null,
  );
  const [copied, setCopied] = React.useState(false);

  const active: Language | null =
    selected && available.includes(selected)
      ? selected
      : (available[0] ?? null);
  const solution = active ? day.solutionsByLang[active] : null;

  const copy = async () => {
    if (!solution) return;
    try {
      await navigator.clipboard.writeText(solution.content);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1500);
    } catch {
      // clipboard unavailable (e.g. no permissions) -- silently ignore
    }
  };

  if (!solution) {
    return (
      <p className="py-[1lh] text-ascii-comment">
        no solutions yet -- add go/python/cpp/day
        {String(day.day).padStart(2, "0")}/ files
      </p>
    );
  }

  return (
    <div className="flex min-w-0 flex-col gap-y-[1lh]">
      <div className="flex items-center justify-between gap-x-[2ch] gap-y-[1lh]">
        <ToggleGroup
          value={active ? [active] : []}
          onValueChange={(values: string[]) => {
            const next = values[0];
            if (next === "python" || next === "go" || next === "cpp") {
              setSelected(next);
            }
          }}
        >
          {available.map((lang) => (
            <Toggle key={lang} value={lang} size="sm">
              {shortLang(lang)}
            </Toggle>
          ))}
        </ToggleGroup>
        <Button variant="ghost" onClick={() => void copy()}>
          <span className="text-primary">
            {copied ? "[ok]" : "[copy]"}
          </span>
          {copied ? "copied" : "copy"}
        </Button>
      </div>
      <span className="text-ascii-comment">
        solution.{active ? FILE_EXTENSIONS[active] ?? "txt" : "txt"}
      </span>
      <CodeViewer
        code={solution.content}
        lang={active ?? ""}
        highlightRanges={solution.highlight_ranges}
      />
    </div>
  );
}
