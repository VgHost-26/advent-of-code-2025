import progress from "@/data/progress.json";
import stars from "@/data/stars.json";
import benchmarksFile from "@/data/benchmarks.json";
import type {
  AocDay,
  BenchEntry,
  BenchmarksFile,
  ProgressEntry,
  SolutionData,
} from "@/lib/types";

export type {
  AocDay,
  BenchEntry,
  Language,
  ProgressEntry,
  SolutionData,
} from "@/lib/types";

/** 2025 had a 12-day "Advent" calendar. */
export const TOTAL_DAYS = 12;
export const TOTAL_STARS = TOTAL_DAYS * 2;

export const LANGUAGES = ["python", "go", "cpp"] as const;

const LANG_LABELS: Record<string, string> = {
  python: "py",
  go: "go",
  cpp: "c++",
};

function shortLang(lang: string): string {
  return LANG_LABELS[lang] ?? lang;
}

export { shortLang };

function clampStars(day: number): 0 | 1 | 2 {
  const configured = (stars as unknown as Record<string, { stars?: number }>)[
    String(day)
  ]?.stars;
  const n = Math.trunc(Number(configured ?? 0));
  if (Number.isFinite(n) && n >= 0 && n <= 2) return n as 0 | 1 | 2;
  return 0;
}

function benchmarksFor(
  day: number
): Record<string, Record<string, BenchEntry>> | null {
  const entry = (benchmarksFile as BenchmarksFile)[String(day)];
  if (!entry || Object.keys(entry).length === 0) return null;
  return entry;
}

const _benchmarks = Array.from({ length: TOTAL_DAYS }, (_, i) =>
  benchmarksFor(i + 1)
);

function progressFor(day: number): ProgressEntry | null {
  const entry = (progress as unknown as Record<string, ProgressEntry>)[
    String(day)
  ];
  return entry ?? null;
}

/** Day list sorted 1..TOTAL_DAYS, merged with manual star counts. */
export const days: AocDay[] = Array.from(
  { length: TOTAL_DAYS },
  (_, i): AocDay => {
    const day = i + 1;
    const entry = progressFor(day);
    const solutions: Record<string, SolutionData> = {};    for (const lang of LANGUAGES) {
      const sol = entry?.solutions?.[lang];
      if (sol && sol.content) solutions[lang] = sol;
    }
    return {
      day,
      status: entry?.status ?? "not_started",
      title: entry?.title ?? null,
      html: entry?.html ?? null,
      languages: entry?.languages ?? [],
      stars: clampStars(day),
      solutionsByLang: solutions,
      benchmarksByLang: _benchmarks[i] ?? undefined,
    };
  }
);

/** All benchmarked languages of a part agree on the answer? */
export function benchStatus(
  day: AocDay,
  part: string
): "none" | "ok" | "mismatch" {
  const answers = new Set(
    Object.values(day.benchmarksByLang ?? {})
      .map((parts) => parts[part]?.answer)
      .filter((a): a is string => Boolean(a))
  );
  if (answers.size === 0) return "none";
  return answers.size === 1 ? "ok" : "mismatch";
}

/** "12.3456" ms, compact precision. */
export function fmtMs(ms: number): string {
  if (ms < 0.01) return `${ms.toPrecision(2)}ms`;
  if (ms < 1000) return `${ms.toFixed(Math.abs(ms) < 10 ? 3 : 1)}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

export function dayByNumber(day: number): AocDay | null {
  return days[day - 1] ?? null;
}

export const totalStars = days.reduce((sum, d) => sum + d.stars, 0);

export const languageCounts = LANGUAGES.map((lang) => ({
  lang,
  label: shortLang(lang),
  count: days.filter((d) => d.solutionsByLang[lang]).length,
}));

export function aocUrl(day: number): string {
  return `https://adventofcode.com/2025/day/${day}`;
}

/** Link back to the puzzles' home; the footer's "made by" points here. */
export const AOC_HOME = "https://adventofcode.com/2025";
export const AUTHOR_URL = "https://github.com/VgHost-26";

/** "07" style zero-padded day number. */
export const padDay = (day: number): string => String(day).padStart(2, "0");

export const isStarted = (day: AocDay): boolean =>
  day.languages.length > 0 || day.stars > 0;
