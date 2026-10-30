"""Cross-language benchmark runner (see BENCH-PLAN.md).

Finds days 1-12 x languages, runs each solution in bench mode (parse untimed,
1 warmup + N in-process timed runs per part), aggregates median+min,
cross-checks answers between languages and writes
dashboard/src/data/benchmarks.json.

Usage:
    python3 scripts/benchmark.py [--runs N] [--days 1,2,3] [--langs go,python]
"""

import argparse
import importlib.util
import json
import os
import statistics
import subprocess  # noqa: S404
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_DIR = os.path.join(ROOT_DIR, ".bench-build")
OUTPUT_FILE = os.path.join(
    ROOT_DIR, "dashboard", "src", "data", "benchmarks.json"
)

RUNS = 10
LANGUAGES = ["python", "go", "cpp"]
TOTAL_DAYS = 12
UNSOLVED_MARKER = "% unsolved"

EXTENSIONS = {"python": "py", "go": "go", "cpp": "cpp"}


def is_solved(day: int, lang: str) -> bool:
    solution = os.path.join(ROOT_DIR, lang, f"day{day:02d}", f"solution.{EXTENSIONS[lang]}")
    if not os.path.exists(solution):
        return False
    with open(solution) as f:
        return UNSOLVED_MARKER not in f.read()


def bench_python(day: int, runs: int) -> dict | None:
    """In-process: import the module and time the part functions directly."""
    solution = os.path.join(ROOT_DIR, "python", f"day{day:02d}", "solution.py")
    sys.path.insert(0, os.path.join(ROOT_DIR, "python"))
    try:
        spec = importlib.util.spec_from_file_location(f"aoc_day{day:02d}", solution)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        import common

        with open(os.path.join(ROOT_DIR, "inputs", f"day{day:02d}.txt")) as f:
            data = f.read()
        parts = getattr(module, "PARTS", None) or {
            "1": module.part1,
            "2": getattr(module, "part2", None),
        }
        return common.bench(module.parse, parts, data, runs)
    finally:
        try:
            sys.path.remove(os.path.join(ROOT_DIR, "python"))
        except ValueError:
            pass


def build_go(day: int) -> str | None:
    binary = os.path.join(BUILD_DIR, f"go_day{day:02d}")
    result = subprocess.run(
        ["go", "build", "-o", binary, f"./go/day{day:02d}"],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  go build failed for day {day}: {result.stderr.strip()}")
        return None
    return binary


def build_cpp(day: int) -> str | None:
    binary = os.path.join(BUILD_DIR, f"cpp_day{day:02d}")
    result = subprocess.run(
        [
            "g++", "-O2", "-std=c++17", "-I", "cpp",
            f'-DDAY_SOLUTION="day{day:02d}/solution.cpp"',
            f'-DDAY_INPUT="inputs/day{day:02d}.txt"',
            os.path.join("cpp", "harness.cpp"),
            "-o", binary,
        ],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  g++ build failed for day {day}: {result.stderr.strip()}")
        return None
    return binary


def run_bench_binary(binary: str, day: int, runs: int) -> dict | None:
    input_path = os.path.join(ROOT_DIR, "inputs", f"day{day:02d}.txt")
    result = subprocess.run(
        [binary, "--bench", "--input", input_path, "--runs", str(runs)],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  bench failed for {binary}: {result.stderr.strip()}")
        return None
    for line in reversed(result.stdout.strip().splitlines()):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    print(f"  no JSON line in output of {binary}")
    return None


def aggregate(stats: dict, runs: int) -> dict:
    """Bench stats -> {part: {median_ms, min_ms, runs, answer}}."""
    out = {}
    for label, answer in stats["answers"].items():
        ms = stats["timings"][label]
        out[label] = {
            "median_ms": round(statistics.median(ms), 6),
            "min_ms": round(min(ms), 6),
            "runs": runs,
            "answer": answer,
        }
    return out


def verify_answers(day_out: dict, day: int) -> list[str]:
    """Cross-language answer check; returns warnings."""
    warnings = []
    for label in sorted({p for lang in day_out.values() for p in lang}):
        answers = {}
        for lang, parts in day_out.items():
            if label in parts:
                answers.setdefault(parts[label]["answer"], []).append(lang)
        if len(answers) > 1:
            warnings.append(
                f"day {day} part {label}: answers disagree {answers}"
            )
    return warnings


def load_existing() -> dict:
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE) as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description="AoC benchmark runner")
    parser.add_argument("--runs", type=int, default=RUNS)
    parser.add_argument("--days", type=str, default=None, help="comma list, e.g. 1,2")
    parser.add_argument("--langs", type=str, default=",".join(LANGUAGES))
    args = parser.parse_args()

    langs = [l.strip() for l in args.langs.split(",")]
    days = (
        [int(d) for d in args.days.split(",")]
        if args.days
        else list(range(1, TOTAL_DAYS + 1))
    )

    os.makedirs(BUILD_DIR, exist_ok=True)
    benchmarks = load_existing()
    all_warnings = []

    for day in days:
        day_out = benchmarks.get(str(day), {})

        for lang in langs:
            if not is_solved(day, lang):
                if str(day) in benchmarks and lang in benchmarks[str(day)]:
                    del benchmarks[str(day)][lang]  # solution was removed
                continue

            print(f"day {day} [{lang}] ...", end=" ", flush=True)
            stats = None
            if lang == "python":
                stats = bench_python(day, args.runs)
            elif lang == "go":
                if (binary := build_go(day)) is not None:
                    stats = run_bench_binary(binary, day, args.runs)
            elif lang == "cpp":
                if (binary := build_cpp(day)) is not None:
                    stats = run_bench_binary(binary, day, args.runs)

            if stats is None:
                print("failed")
                continue

            if stats is None:
                print("failed")
                continue

            day_out[lang] = aggregate(stats, args.runs)
            part_summary = " | ".join(
                f"p{k}: {v['median_ms']:.4f}ms (min {v['min_ms']:.4f})"
                for k, v in day_out[lang].items()
            )
            print(part_summary)

        all_warnings += verify_answers(day_out, day)
        benchmarks[str(day)] = day_out

    with open(OUTPUT_FILE, "w") as f:
        json.dump(benchmarks, f, indent=2)
        f.write("\n")
    print(f"\nWrote {OUTPUT_FILE}")

    if all_warnings:
        print("\nANSWER MISMATCHES (dashboard will show these as errors):")
        for w in all_warnings:
            print(f"  {w}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
