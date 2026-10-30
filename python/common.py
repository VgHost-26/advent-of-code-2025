"""Shared helpers for AoC solution scripts: input reading + bench protocol.

Bench protocol (see BENCH-PLAN.md):
    solution.py --bench [--input inputs/dayNN.txt] [--runs N]
prints exactly one JSON line:
    {"answers": {"1": "...", "2": "..."},
     "timings": {"1": [<ms>, ...], "2": [<ms>, ...]}}
timings are milliseconds (float), one per timed run, warmup excluded.

Solutions declare a module-level `PARTS` dict ({"1": part1, "2": part2|None})
so the benchmark orchestrator can import and run them in-process.
"""

import json
import sys
import time


def read_input(default_path: str, args: list[str] | None = None) -> str:
    """Read the puzzle input, honouring `--input PATH` / `--input=PATH`
    or a positional path. `--bench`/`--runs N` are ignored."""
    args = args if args is not None else sys.argv[1:]
    path = default_path
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--input" and i + 1 < len(args):
            path = args[i + 1]
            i += 2
            continue
        if arg.startswith("--input="):
            path = arg.split("=", 1)[1]
        elif arg == "--runs" and i + 1 < len(args):
            i += 2
            continue
        elif arg.startswith("--runs="):
            pass
        elif not arg.startswith("-"):
            path = arg
        i += 1
    with open(path, "r") as f:
        return f.read()


def bench(parse, parts: dict, data: str, runs: int = 10) -> dict:
    """Run the bench protocol in-process.

    parts: {"1": part1, "2": part2, ...} (None-valued parts are skipped).
    parse() runs once, untimed; only the part functions go inside the clock.
    One untimed warmup runs before the measured iterations.
    """
    parsed = parse(data)
    answers: dict[str, str] = {}
    timings: dict[str, list[float]] = {}
    for label, fn in parts.items():
        if fn is None:
            continue
        reference = fn(parsed)  # untimed warmup
        runs_ms = []
        result = reference
        for _ in range(runs):
            t0 = time.perf_counter_ns()
            result = fn(parsed)
            runs_ms.append((time.perf_counter_ns() - t0) / 1_000_000)
        answers[label] = str(result)
        timings[label] = [round(ms, 6) for ms in runs_ms]
    return {"answers": answers, "timings": timings}


def is_bench(args: list[str] | None = None) -> bool:
    args = args if args is not None else sys.argv[1:]
    return "--bench" in args


def bench_runs(args: list[str] | None = None, default: int = 10) -> int:
    args = args if args is not None else sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--runs" and i + 1 < len(args):
            return int(args[i + 1])
        if arg.startswith("--runs="):
            return int(arg.split("=", 1)[1])
    return default


def run_cli(parse, parts: dict, default_input: str) -> None:
    """Main entry point for a `python dayNN/solution.py` invocation."""
    if is_bench():
        data = read_input(default_input)
        runs = bench_runs()
        stats = bench(parse, parts, data, runs)
        print(json.dumps(stats))
        return

    data = read_input(default_input)
    parsed = parse(data)
    print(f"Solving with input from {default_input}")
    for label, fn in parts.items():
        if fn is None:
            continue
        print(f"Part {label}: {fn(parsed)}")
