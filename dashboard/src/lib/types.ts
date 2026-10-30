/** Shapes of the generated data files under src/data/. */

export type SolutionData = {
  /** Full solution file content. */
  content: string;
  /** Highlighted code regions, 0-indexed half-open [start, end] line pairs. */
  highlight_ranges?: number[][];
  /** Whether that language got both puzzles. */
  completed?: boolean;
};

export type ProgressEntry = {
  day: number;
  status: string;
  languages: string[];
  title?: string;
  html?: string;
  /** Keyed by language: python | go | cpp. */
  solutions: Record<string, SolutionData>;
};

/** progress.json — object keyed by day number as string. */
export type ProgressFile = Record<string, ProgressEntry>;

/** stars.json — manual config, one entry per day. */
export type StarsFile = Record<string, { stars: number }>;

/** benchmarks.json — one entry per day/part/language (see BENCH-PLAN.md). */
export type BenchEntry = {
  median_ms: number;
  min_ms: number;
  runs: number;
  answer: string;
};

/** benchmarks.json — object keyed by day number as string, then language, then part. */
export type BenchmarksFile = Record<
  string,
  Record<string, Record<string, BenchEntry>>
>;

/** A day merged from progress + stars, as consumed by the UI. */
export type AocDay = {
  day: number;
  status: string;
  title: string | null;
  html: string | null;
  languages: string[];
  stars: 0 | 1 | 2;
  /** Keyed by language: python | go | cpp (present solutions only). */
  solutionsByLang: Record<string, SolutionData>;
  /** Keyed by language, then part ("1" | "2"). Present when benchmarked. */
  benchmarksByLang?: Record<string, Record<string, BenchEntry>>;
};

export type Language = "python" | "go" | "cpp";
