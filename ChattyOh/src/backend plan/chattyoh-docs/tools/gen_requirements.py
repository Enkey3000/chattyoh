#!/usr/bin/env python3
"""Generates docs/requirements.md from the SRS (single source of truth) so the two never drift.
Usage: python tools/gen_requirements.py"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]; D = ROOT / "docs"

def rows(name, prefix, n):
    out = []
    for line in (D / name).read_text(encoding="utf-8").splitlines():
        if line.startswith("| " + prefix):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) >= n: out.append(c)
    return out

feat = {r[0]: r for r in rows("01-prd.md", "PRD-F-", 5)}
srs = rows("02-srs.md", "SRS-", 7)
stories = {}
for u in rows("user-stories.md", "US-", 6):
    for q in re.split(r"[,\s]+", u[4]):
        if q: stories.setdefault(q, []).append(u[0])

def group(src):
    return (src, feat[src][1], feat[src][2]) if src in feat else ("QUALITY", "Quality attributes and cross-cutting rules", "Must")

groups = {}
for r in srs: groups.setdefault(group(r[2]), []).append(r)
order = sorted(groups, key=lambda g: (g[0] == "QUALITY", g[0]))
slices = {}
for r in srs: slices[r[6]] = slices.get(r[6], 0) + 1

out = ["# Requirements", "",
       "**Project:** ChattyOh Inc · **Generated from:** `docs/02-srs.md` by `tools/gen_requirements.py` — **do not edit by hand**; change the SRS and regenerate.",
       "**Purpose:** a readable register of every requirement grouped by product feature, with priority, release slice, verification method and linked user stories. Detail, rationale, architecture decisions and security controls for each requirement are in the SRS; traceability to tests and APIs is in `11-rtm.md`.", "",
       "## Summary", "", f"{len(srs)} requirements: " + ", ".join(f"{k} = {v}" for k, v in sorted(slices.items())) + ".", "",
       "Priority comes from the PRD feature (Must / Should); quality-attribute requirements are Must. Slice: MVP-0 walking skeleton, MVP-1 complete core, MVP-2 hardening (see `15-mvp-pattern.md`).", ""]
for g in order:
    out += [f"## {g[1]}" + (f" ({g[0]})" if g[0] != "QUALITY" else ""), "", f"Priority: **{g[2]}**", "",
            "| ID | Requirement | Slice | Verification | User stories |", "|---|---|---|---|---|"]
    for r in groups[g]:
        out.append(f"| {r[0]} | {r[1]} | {r[6]} | {r[5]} | {', '.join(stories.get(r[0], [])) or '—'} |")
    out.append("")
(D / "requirements.md").write_text("\n".join(out), encoding="utf-8")
print("requirements.md written:", len(srs), "requirements")
