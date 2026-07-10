#!/usr/bin/env python3
"""
graph_triage.py — Graph-based triage for the M1→M5 pipeline.

Called by the LLM agent between M2 (scan) and M3 (playbook).
Reads the most recent SARIF, runs the graph pipeline, and outputs
centrality-ranked patch priorities with coupling context.

Usage:
    python3 graph_triage.py --sarif /tmp/raptor_s7g_full/combined.sarif
    python3 graph_triage.py --latest-scan   # auto-detect most recent scan output

Output: JSON with ranked findings, coupling clusters, and centrality scores.
The LLM agent reads this output before calling generate_playbook.py.
"""

import json
import os
import sys
import glob
import re
import subprocess
from pathlib import Path
from collections import defaultdict

# Paths
AIKG_PATH = os.path.expanduser("~/projects/ai-knowledge-graph")
MERGED_GRAPH = "/tmp/s7g_merged.json"
SCAN_OUTPUT_DIR = "/tmp"


def find_latest_sarif():
    """Find the most recent RAPTOR scan output directory."""
    dirs = [d for d in os.listdir(SCAN_OUTPUT_DIR)
            if os.path.isdir(os.path.join(SCAN_OUTPUT_DIR, d)) and d.startswith("raptor_")]
    if not dirs:
        # Also check common names
        for path in [
            "/tmp/raptor_s7g_full/combined.sarif",
            "/tmp/raptor_test/combined.sarif",
        ]:
            if os.path.exists(path):
                return path
        return None
    # Sort by modification time, newest first
    dirs.sort(key=lambda d: os.path.getmtime(os.path.join(SCAN_OUTPUT_DIR, d)), reverse=True)
    for d in dirs:
        sarif = os.path.join(SCAN_OUTPUT_DIR, d, "combined.sarif")
        if os.path.exists(sarif):
            return sarif
    return None


def load_sarif(path):
    """Load SARIF and extract per-file findings."""
    with open(path) as f:
        data = json.load(f)

    files = {}
    for run in data.get("runs", []):
        for result in run.get("results", []):
            rule_id = result.get("ruleId", "unknown")
            level = result.get("level", "warning")
            rule_short = rule_id.rsplit(".", 1)[-1] if "." in rule_id else rule_id

            sev_map = {"none": "info", "note": "low", "warning": "medium", "error": "high"}
            severity = sev_map.get(level, "medium")

            for loc in result.get("locations", []):
                phys = loc.get("physicalLocation", {})
                artifact = phys.get("artifactLocation", {})
                uri = artifact.get("uri", "unknown").replace("file://", "")
                region = phys.get("region", {})
                line = region.get("startLine", 0)

                # Normalize path
                rel = uri
                for prefix in ["/home/cherry/projects/s7g/", "/home/cherry/projects/", "/github/workspace/s7g/", "/github/workspace/", "/home/runner/work/network/network/"]:
                    if rel.startswith(prefix):
                        rel = rel[len(prefix):]
                        break

                if rel not in files:
                    files[rel] = {"findings": [], "vulns": set(), "max_severity": "info"}
                files[rel]["findings"].append({
                    "rule": rule_short,
                    "line": line,
                    "severity": severity,
                    "message": result.get("message", {}).get("text", "")[:150],
                })
                files[rel]["vulns"].add(rule_short)

                sev_order = ["info", "low", "medium", "high"]
                if sev_order.index(severity) > sev_order.index(files[rel]["max_severity"]):
                    files[rel]["max_severity"] = severity

    # Fetch ownership for all files found
    # Import parser blame helpers or define them
    for rel in files.keys():
        try:
            resolved_repo = os.getcwd()
            target_path = rel
            
            # Map path to real directory locations
            candidate_repos = [
                "/media/cherry/Lexar/New folder/AGE REPUBLIC",
                "/home/cherry/projects/s7g",
                "/home/cherry/projects/ai-knowledge-graph",
                os.getcwd()
            ]
            
            found = False
            for repo in candidate_repos:
                if os.path.exists(os.path.join(repo, rel)):
                    resolved_repo = repo
                    found = True
                    break
                    
            if not found:
                # Try finding inside the target resolved directories by matching basename
                basename = rel.split("/")[-1]
                for repo in candidate_repos:
                    if not os.path.exists(repo):
                        continue
                    for root, dirs, files_in_dir in os.walk(repo):
                        if basename in files_in_dir:
                            resolved_repo = repo
                            # Make path relative to that repo
                            target_path = os.path.relpath(os.path.join(root, basename), repo)
                            found = True
                            break
                    if found:
                        break

            result = subprocess.run(
                ["git", "log", "-1", "--format=%an|%ae|%ad", "--date=short", "--", target_path],
                cwd=resolved_repo,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout:
                parts = result.stdout.strip().split("|")
                if len(parts) == 3:
                    files[rel]["owner"] = {"name": parts[0], "email": parts[1], "date": parts[2]}
                else:
                    files[rel]["owner"] = {"name": "unknown", "email": "unknown", "date": "unknown"}
            else:
                files[rel]["owner"] = {"name": "unknown", "email": "unknown", "date": "unknown"}
        except Exception:
            files[rel]["owner"] = {"name": "unknown", "email": "unknown", "date": "unknown"}

    return files



def load_or_build_merged_graph():
    """Load the merged graph if it exists, otherwise build from SARIF."""
    if os.path.exists(MERGED_GRAPH):
        with open(MERGED_GRAPH) as f:
            return json.load(f)
    return None


def compute_centrality(files_data):
    """
    Compute centrality scores for each file.
    Centrality = how many other files share a vulnerability type with this file.
    A file that shares vulns with many others is a high-centrality hub.
    """
    # vuln → [files that have it]
    vuln_files = defaultdict(set)
    for fp, data in files_data.items():
        for v in data["vulns"]:
            vuln_files[v].add(fp)

    # file → centrality score (number of unique files it shares vulns with)
    centrality = defaultdict(set)
    for v, files in vuln_files.items():
        if len(files) > 1:
            for fp in files:
                centrality[fp].update(files - {fp})

    centrality_scores = {fp: len(connected) for fp, connected in centrality.items()}
    return centrality_scores, dict(centrality)


def rank_findings(files_data):
    """Rank findings by composite score: centrality (60%) + severity (40%)."""
    centrality_scores, centrality_map = compute_centrality(files_data)

    # Normalize centrality to 0-10 scale
    max_centrality = max(centrality_scores.values()) if centrality_scores else 1

    ranked = []
    for fp, data in files_data.items():
        c_score = centrality_scores.get(fp, 0) / max_centrality * 10
        sev_score = {"high": 10, "medium": 6, "low": 3, "info": 0}[data["max_severity"]]
        composite = round(0.6 * c_score + 0.4 * sev_score, 1)

        ranked.append({
            "file": fp,
            "max_severity": data["max_severity"],
            "finding_count": len(data["findings"]),
            "vulnerability_types": sorted(data["vulns"]),
            "centrality_score": round(c_score, 1),
            "composite_priority": composite,
            "coupled_files": sorted(centrality_map.get(fp, set())),
        })

    ranked.sort(key=lambda x: x["composite_priority"], reverse=True)
    return ranked


def generate_triage_output(sarif_path=None):
    """Main entry point: produce triage-ranked output for the LLM agent."""
    if not sarif_path:
        sarif_path = find_latest_sarif()

    if not sarif_path or not os.path.exists(sarif_path):
        print(json.dumps({
            "status": "error",
            "message": "No SARIF scan output found. Run RAPTOR scan first.",
            "searched": f"{SCAN_OUTPUT_DIR}/raptor_*/combined.sarif",
        }, indent=2))
        sys.exit(1)

    print(json.dumps({
        "phase": "M2→M3 Bridge: Graph Triage",
        "sarif_source": sarif_path,
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }, indent=2))
    print()

    # Load
    files_data = load_sarif(sarif_path)
    ranked = rank_findings(files_data)

    # Summary
    high_count = sum(1 for r in ranked if r["max_severity"] == "high")
    med_count = sum(1 for r in ranked if r["max_severity"] == "medium")

    print(json.dumps({
        "status": "triage_complete",
        "total_files_with_findings": len(files_data),
        "total_findings": sum(len(d["findings"]) for d in files_data.values()),
        "severity_summary": {
            "high": high_count,
            "medium": med_count,
            "low": sum(1 for r in ranked if r["max_severity"] == "low"),
        },
    }, indent=2))
    print()

    # Patch priority list (top 5)
    print("### PATCH PRIORITY (Graph-Weighted)")
    print("| Rank | File | Severity | Findings | Centrality | Priority | Coupled Files |")
    print("|------|------|----------|----------|------------|----------|---------------|")
    for i, r in enumerate(ranked[:10], 1):
        coupled = ", ".join(r["coupled_files"][:3])
        if len(r["coupled_files"]) > 3:
            coupled += f" ... (+{len(r['coupled_files']) - 3})"
        sev_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(r["max_severity"], "⚪")
        print(f"| {i} | {r['file']} | {sev_icon}{r['max_severity'].upper()} | {r['finding_count']} | {r['centrality_score']}/10 | {r['composite_priority']} | {coupled} |")

    print()
    print("### TRIAGE RECOMMENDATION")
    if ranked:
        top = ranked[0]
        print(f"**Patch first:** `{top['file']}` — {top['vulnerability_types']}")
        
        # Look up owner if present
        top_owner_info = ""
        owners_map = files_data.get(top['file'], {}).get("owner", {})
        if owners_map and owners_map.get("email") != "unknown":
            top_owner_info = f" (Owner: {owners_map.get('name')} <{owners_map.get('email')}>)"
            
        print(f"**Why:** Centrality score {top['centrality_score']}/10 — this file shares vulnerabilities with {len(top['coupled_files'])} other file(s).{top_owner_info}")
        print(f"**Fixing it resolves risk across:** {', '.join(top['coupled_files'][:5])}")
        if len(top['coupled_files']) > 5:
            print(f"  ... and {len(top['coupled_files']) - 5} more file(s).")
        print()

        # Print Owner Assignment table
        print("### OWNER ASSIGNMENT")
        print("| File | Owner | Last Modified |")
        print("|------|-------|---------------|")
        for r in ranked[:10]:
            f_data = files_data.get(r['file'], {})
            owner = f_data.get("owner", {})
            owner_str = "unknown"
            if owner.get("email") != "unknown":
                owner_str = f"{owner.get('name')} <{owner.get('email')}>"
            print(f"| {r['file']} | {owner_str} | {owner.get('date', 'unknown')} |")
        print()

        # If there are coupling clusters, highlight them
        clusters = find_coupling_clusters(ranked)
        if clusters:
            print("### COUPLING CLUSTERS")
            print("Files that share vulnerability patterns — patch as a group:")
            for cluster in clusters[:3]:
                print(f"- {', '.join(cluster[:4])}")
                if len(cluster) > 4:
                    print(f"  + {len(cluster) - 4} more")
            print()


    # Full data for downstream consumption
    print("### FULL_RANKING")
    print(json.dumps(ranked, indent=2))


def find_coupling_clusters(ranked):
    """Find clusters of mutually coupled files."""
    clusters = []
    seen = set()

    for r in ranked:
        if r["file"] in seen:
            continue
        coupled = [r["file"]] + [c for c in r["coupled_files"] if c not in seen]
        if len(coupled) > 1:
            clusters.append(coupled)
            for f in coupled:
                seen.add(f)

    return clusters


def check_centrality_threshold(sarif_path, threshold):
    """Verify if any file centrality exceeds threshold, exiting with status 1 if so."""
    files_data = load_sarif(sarif_path)
    ranked = rank_findings(files_data)
    failed = False
    for r in ranked:
        if r["centrality_score"] > threshold:
            print(f"❌ SECURITY POLICY VIOLATION: File '{r['file']}' has centrality {r['centrality_score']:.1f}/10, exceeding maximum threshold of {threshold:.1f}")
            failed = True
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Graph-based triage for M1→M5 pipeline")
    parser.add_argument("--sarif", help="Path to SARIF file (auto-detects latest if omitted)")
    parser.add_argument("--latest-scan", action="store_true", help="Auto-detect most recent scan")
    parser.add_argument("--fail-on-central", type=float, help="Fail build if any file centrality exceeds this threshold (0.0 to 10.0)")
    args = parser.parse_args()

    sarif_path = args.sarif
    if args.latest_scan or not sarif_path:
        sarif_path = find_latest_sarif()

    # If only verifying threshold for CI pipeline
    if args.fail_on_central is not None:
        if not sarif_path or not os.path.exists(sarif_path):
            print("ERROR: SARIF not found.")
            sys.exit(1)
        check_centrality_threshold(sarif_path, args.fail_on_central)
        print(f"✅ Security Policy check passed: all files below centrality threshold {args.fail_on_central:.1f}")
        sys.exit(0)

    generate_triage_output(sarif_path)

