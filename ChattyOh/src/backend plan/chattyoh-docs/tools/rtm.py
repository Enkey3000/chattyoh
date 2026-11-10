#!/usr/bin/env python3
"""Requirements Traceability Matrix generator and CI gate.

Usage:  python tools/rtm.py            # regenerate docs/rtm/rtm.csv and docs/11-rtm.md, print report
        python tools/rtm.py --check    # same, but exit 1 if any ERROR is found (use in CI)
Needs:  pip install pyyaml
Reads:  docs/01-prd.md, 02-srs.md, 03-architecture.md, 04-security-measures.md, 07-threat-model.md,
        08-test-cases.md, 09-uat-plan.md and packages/contracts/openapi.yaml (x-srs / x-sec).
"""
import csv, pathlib, re, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def table_rows(name, prefix, min_cols):
    out = []
    for line in (DOCS / name).read_text(encoding="utf-8").splitlines():
        if line.startswith("| " + prefix):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= min_cols:
                out.append(cells)
    return out


def split(s):
    return [x.strip() for x in re.split(r"[,\s]+", s) if x.strip() and x.strip() not in ("—", "-")]


prd = {r[0] for r in table_rows("01-prd.md", "PRD-", 2)}
srs = {r[0]: r for r in table_rows("02-srs.md", "SRS-", 7)}
adr = {r[0] for r in table_rows("03-architecture.md", "ARCH-ADR-", 4)}
sec = {r[0] for r in table_rows("04-security-measures.md", "SEC-C-", 5)}
thr = {r[0]: r for r in table_rows("07-threat-model.md", "THR-", 6)}
tcs = {r[0]: r for r in table_rows("08-test-cases.md", "TC-", 7)}
uat = {r[0]: r for r in table_rows("09-uat-plan.md", "UAT-", 5)}
us = {r[0]: r for r in table_rows("user-stories.md", "US-", 6)}

spec = yaml.safe_load((ROOT / "packages/contracts/openapi.yaml").read_text(encoding="utf-8"))
ops = {}
for path, methods in spec["paths"].items():
    for method, o in methods.items():
        ops[o["operationId"]] = {"srs": o.get("x-srs", []), "sec": o.get("x-sec", []), "where": f"{method.upper()} {path}"}

errors, warnings = [], []

# --- link integrity
for rid, r in srs.items():
    if r[2] not in prd: errors.append(f"{rid}: unknown PRD source {r[2]}")
    for a in split(r[3]):
        if a not in adr: errors.append(f"{rid}: unknown ADR {a}")
    for s in split(r[4]):
        if s not in sec: errors.append(f"{rid}: unknown control {s}")
tc_by_req, tc_by_thr = {}, {}
for tid, t in tcs.items():
    for q in split(t[2]):
        if q not in srs: errors.append(f"{tid}: unknown requirement {q}")
        tc_by_req.setdefault(q, []).append(tid)
    for h in split(t[3]):
        if h not in thr: errors.append(f"{tid}: unknown threat {h}")
        tc_by_thr.setdefault(h, []).append(tid)
for hid, h in thr.items():
    for s in split(h[4]):
        if s not in sec: errors.append(f"{hid}: unknown control {s}")
    for q in split(h[5]):
        if q not in srs: errors.append(f"{hid}: unknown requirement {q}")
    if h[3] == "High":
        if hid not in tc_by_thr: errors.append(f"{hid}: High threat has no test case")
        if not split(h[4]): errors.append(f"{hid}: High threat has no control")
for oid, o in ops.items():
    if not o["srs"] or not o["sec"]: errors.append(f"API-{oid}: missing x-srs or x-sec")
    for q in o["srs"]:
        if q not in srs: errors.append(f"API-{oid}: unknown requirement {q}")
    for s in o["sec"]:
        if s not in sec: errors.append(f"API-{oid}: unknown control {s}")
for uid, u in uat.items():
    for p in split(u[2]):
        if p not in prd: errors.append(f"{uid}: unknown PRD item {p}")
    for q in split(u[3]):
        if q not in srs: errors.append(f"{uid}: unknown requirement {q}")

us_by_req = {}
for sid, u in us.items():
    if u[3] not in prd: errors.append(f"{sid}: unknown PRD item {u[3]}")
    for q in split(u[4]):
        if q not in srs: errors.append(f"{sid}: unknown requirement {q}")
        us_by_req.setdefault(q, []).append(sid)

# --- coverage
api_by_req, uat_by_req, thr_by_req = {}, {}, {}
for oid, o in ops.items():
    for q in o["srs"]: api_by_req.setdefault(q, []).append("API-" + oid)
for uid, u in uat.items():
    for q in split(u[3]): uat_by_req.setdefault(q, []).append(uid)
for hid, h in thr.items():
    for q in split(h[5]): thr_by_req.setdefault(q, []).append(hid)
for rid in srs:
    if rid not in tc_by_req: errors.append(f"{rid}: no test case")
    if rid not in us_by_req: warnings.append(f"{rid}: no user story")
    if rid.startswith("SRS-FR-") and not rid.startswith("SRS-FR-UI") and rid not in api_by_req:
        warnings.append(f"{rid}: no API operation references it")
for f in [p for p in prd if p.startswith("PRD-F-")]:
    if not any(r[2] == f for r in srs.values()): errors.append(f"{f}: no SRS requirement")
    if not any(f in split(u[2]) for u in uat.values()): warnings.append(f"{f}: no UAT scenario")
used_sec = set()
for r in srs.values(): used_sec |= set(split(r[4]))
for h in thr.values(): used_sec |= set(split(h[4]))
for o in ops.values(): used_sec |= set(o["sec"])
for s in sorted(sec - used_sec): errors.append(f"{s}: control not referenced by any requirement, threat or operation")

# --- outputs
(DOCS / "rtm").mkdir(exist_ok=True)
header = ["PRD item", "Requirement", "ADR", "Controls", "API operations", "Threats", "Test cases", "User stories", "UAT", "Slice", "Test status"]
rows = []
for rid, r in srs.items():
    rows.append([r[2], rid, "; ".join(split(r[3])), "; ".join(split(r[4])), "; ".join(api_by_req.get(rid, [])),
                 "; ".join(thr_by_req.get(rid, [])), "; ".join(tc_by_req.get(rid, [])), "; ".join(us_by_req.get(rid, [])), "; ".join(uat_by_req.get(rid, [])), r[6],
                 "Designed (not yet automated)"])
with open(DOCS / "rtm" / "rtm.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(header); w.writerows(rows)

n_req = len(srs)
cov = sum(1 for rid in srs if rid in tc_by_req)
high = [h for h in thr.values() if h[3] == "High"]
md = ["# 11 — Requirements Traceability Matrix (RTM)", "",
      "**Project:** ChattyOh Inc · **Owner:** QA Lead · **Generated by:** `tools/rtm.py` (do not edit by hand) · **CSV:** `docs/rtm/rtm.csv`", "",
      "Chain: PRD item → SRS requirement → ADR → controls → API operations → threats → test cases → UAT → release slice.", "",
      "## Summary", "",
      "| Measure | Value |", "|---|---|",
      f"| PRD items | {len(prd)} |", f"| Requirements | {n_req} |", f"| Requirements with ≥ 1 test case | {cov} of {n_req} |",
      f"| Test cases (designed) | {len(tcs)} |", f"| Threats | {len(thr)} (High: {len(high)}, all with a test and control) |",
      f"| Controls | {len(sec)} |", f"| API operations | {len(ops)} |", f"| User stories | {len(us)} |", f"| UAT scenarios | {len(uat)} |",
      f"| Errors | {len(errors)} |", f"| Warnings | {len(warnings)} |", "",
      "**Status note:** test cases are designed but not yet automated; none has been executed against a product build. Coverage here means *traceability*, not passing tests.", "",
      "## Matrix", "", "| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
for r in rows: md.append("| " + " | ".join(c if c else "—" for c in r) + " |")
md += ["", "## Errors", ""] + ([f"- {e}" for e in errors] or ["None."]) + ["", "## Warnings", ""] + ([f"- {w}" for w in warnings] or ["None."]) + [""]
(DOCS / "11-rtm.md").write_text("\n".join(md), encoding="utf-8")

print(f"requirements {n_req} | with tests {cov} | tests {len(tcs)} | threats {len(thr)} (High {len(high)}) | controls {len(sec)} | ops {len(ops)} | UAT {len(uat)}")
for e in errors: print("ERROR:", e)
for w in warnings: print("WARN:", w)
if "--check" in sys.argv and errors:
    sys.exit(1)
