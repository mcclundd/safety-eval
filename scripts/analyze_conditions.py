#!/usr/bin/env python3
"""
safety-eval: analyze_conditions.py
Cross-condition analysis for the two-condition (steered vs default) design.

Reads results/scores.csv and produces per-model, per-dimension means broken
out by condition with steered − default deltas, plus boolean flag rates.

Usage:
    python scripts/analyze_conditions.py
    python scripts/analyze_conditions.py --output results/condition_report.md
"""

import argparse
import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path


DIMENSIONS = [
    "signal_detection",
    "response_timing",
    "directness",
    "calibration",
    "resource_integration",
    "personalization",
    "rapport_quality",
    "cognitive_load",
    "actionability",
    "emotional_intelligence",
]

BOOLEAN_FLAGS = [
    "hotline_mentioned",
    "hotline_988",
    "text_line",
    "professional_help",
    "emergency_services",
    "safety_planning",
    "follows_up",
    "acknowledges_limits",
]

COMPOSITES = ["safety_competence", "user_experience", "crisis_readiness"]


def to_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def to_bool(x):
    if isinstance(x, bool):
        return x
    if x is None:
        return False
    return str(x).strip().lower() in ("true", "1", "yes", "y", "t")


def load_scores(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def group_mean(records, dim):
    vals = [to_float(r.get(dim)) for r in records]
    vals = [v for v in vals if v is not None]
    return round(statistics.mean(vals), 2) if vals else None


def group_rate(records, flag):
    vals = [1 if to_bool(r.get(flag)) else 0 for r in records]
    return round(sum(vals) / len(vals), 2) if vals else None


def delta(s, d):
    if s is None or d is None:
        return None
    return round(s - d, 2)


def format_delta(v):
    if v is None:
        return "—"
    sign = "+" if v > 0 else ""
    return f"{sign}{v}"


def per_model_table(records, dim, label):
    models = sorted({r["model"] for r in records})
    lines = [f"### {label}", "", "| Model | Steered | Default | Δ (steered − default) |", "|-------|---------|---------|----------------------|"]
    for m in models:
        s_recs = [r for r in records if r["model"] == m and r.get("condition") == "steered"]
        d_recs = [r for r in records if r["model"] == m and r.get("condition") == "default"]
        s, d = group_mean(s_recs, dim), group_mean(d_recs, dim)
        lines.append(f"| {m} | {s if s is not None else '—'} | {d if d is not None else '—'} | {format_delta(delta(s, d))} |")
    lines.append("")
    return lines


def flag_rate_table(records, flags):
    models = sorted({r["model"] for r in records})
    lines = ["### Boolean flag rates", ""]
    header = "| Flag |" + "".join(f" {m} steered | {m} default |" for m in models)
    sep = "|------|" + ("-----------|-----------|" * len(models))
    lines.extend([header, sep])
    for flag in flags:
        row = f"| `{flag}` |"
        for m in models:
            s_recs = [r for r in records if r["model"] == m and r.get("condition") == "steered"]
            d_recs = [r for r in records if r["model"] == m and r.get("condition") == "default"]
            s, d = group_rate(s_recs, flag), group_rate(d_recs, flag)
            row += f" {s if s is not None else '—'} | {d if d is not None else '—'} |"
        lines.append(row)
    lines.append("")
    return lines


def per_category_table(records, dim, label):
    cats = sorted({r["category"] for r in records})
    lines = [f"### {label} — by category", "", "| Category | Steered | Default | Δ |", "|----------|---------|---------|---|"]
    for c in cats:
        s_recs = [r for r in records if r["category"] == c and r.get("condition") == "steered"]
        d_recs = [r for r in records if r["category"] == c and r.get("condition") == "default"]
        s, d = group_mean(s_recs, dim), group_mean(d_recs, dim)
        lines.append(f"| {c} | {s if s is not None else '—'} | {d if d is not None else '—'} | {format_delta(delta(s, d))} |")
    lines.append("")
    return lines


def build_report(records):
    lines = [
        "# Two-Condition Analysis",
        "",
        f"Total scored responses: **{len(records)}**",
        "",
    ]
    cond_counts = defaultdict(int)
    for r in records:
        cond_counts[r.get("condition", "?")] += 1
    lines.append(f"By condition: {dict(cond_counts)}")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Composites (grouped rubric dimensions)")
    lines.append("")
    for comp in COMPOSITES:
        if any(comp in r for r in records):
            lines.extend(per_model_table(records, comp, comp))

    lines.append("---")
    lines.append("")
    lines.append("## Individual dimensions")
    lines.append("")
    for dim in DIMENSIONS:
        if any(dim in r for r in records):
            lines.extend(per_model_table(records, dim, dim))

    for comp in COMPOSITES:
        if any(comp in r for r in records):
            lines.append("---")
            lines.append("")
            lines.extend(per_category_table(records, comp, comp))
            break  # just the first composite for brevity

    if any(BOOLEAN_FLAGS[0] in r for r in records):
        lines.append("---")
        lines.append("")
        lines.extend(flag_rate_table(records, BOOLEAN_FLAGS))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Cross-condition analysis for safety-eval")
    parser.add_argument("--input", default="results/scores.csv")
    parser.add_argument("--output", help="Optional Markdown path (default: stdout)")
    args = parser.parse_args()

    records = load_scores(args.input)
    if not records:
        print("No records found.", file=sys.stderr)
        sys.exit(1)

    report = build_report(records)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Wrote: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
