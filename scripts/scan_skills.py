#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosystem Sediment & Technical Debt CI Scanner
=============================================
Calculates sediment score based on stale files, vague instructions, and duplicates.
Exits with code 1 if sediment score exceeds threshold.
"""

import os
import sys
import time
import re
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime

VAGUE_KEYWORDS = [
    r"\bconsider\b",
    r"\bmaybe\b",
    r"\bensure\b",
    r"\bbest practices?\b",
    r"\bappropriate\b",
    r"\bsometimes\b",
    r"\bperiodically\b",
    r"\bregularly\b"
]

def scan_skills(target_path: Path):
    stale_skills = []
    vague_instructions = []
    paragraphs = {}
    duplicate_paragraphs = []
    total_files = 0
    total_rules = 0
    now = time.time()
    
    # Traverse directory
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if not file.endswith(".md"):
                continue
                
            total_files += 1
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, target_path)
            
            # 1. Age Analysis
            try:
                mtime = os.path.getmtime(full_path)
                age_days = int((now - mtime) / (24 * 3600))
                if age_days > 90:
                    stale_skills.append({"file": rel_path, "age_days": age_days})
            except Exception:
                pass
                
            # Read content
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                continue
                
            # Count instructions/rules
            lines = content.splitlines()
            for line_no, line in enumerate(lines, 1):
                clean_line = line.strip()
                if clean_line.startswith("-") or clean_line.startswith("*") or re.match(r"^\d+\.", clean_line):
                    total_rules += 1
                    
                    # 2. Vague Terms Detection
                    for kw in VAGUE_KEYWORDS:
                        if re.search(kw, clean_line, re.IGNORECASE):
                            vague_instructions.append({
                                "file": rel_path,
                                "line_no": line_no,
                                "text": clean_line,
                                "keyword": kw.replace(r"\b", "")
                            })
                            break
                            
            # 3. Duplicate Paragraphs (DRY Analysis)
            blocks = content.split("\n\n")
            for block in blocks:
                clean_block = block.strip()
                if len(clean_block) < 60 or clean_block.startswith("```"):
                    continue
                
                block_hash = hashlib.sha256(clean_block.encode("utf-8")).hexdigest()
                if block_hash in paragraphs:
                    duplicate_paragraphs.append({
                        "file_a": paragraphs[block_hash]["file"],
                        "file_b": rel_path,
                        "text": clean_block[:150] + "..."
                    })
                else:
                    paragraphs[block_hash] = {"file": rel_path, "text": clean_block}
                    
    return {
        "files_scanned": total_files,
        "instructions_analyzed": total_rules,
        "stale_skills": stale_skills,
        "vague_instructions": vague_instructions,
        "duplicate_paragraphs": duplicate_paragraphs
    }

def generate_report(results: dict, sediment_score: float, threshold: float, output_path: Path):
    stale_skills = results["stale_skills"]
    vague_instructions = results["vague_instructions"]
    duplicate_paragraphs = results["duplicate_paragraphs"]
    
    stale_skills.sort(key=lambda x: x["age_days"], reverse=True)
    
    with open(output_path, "w", encoding="utf-8") as rep:
        rep.write("# Ecosystem Sediment & Technical Debt Report\n\n")
        rep.write(f"**Scan Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        rep.write(f"**Total Skill Files Scanned:** {results['files_scanned']}\n")
        rep.write(f"**Total Instructions Scanned:** {results['instructions_analyzed']}\n")
        rep.write(f"**Sediment Score:** {sediment_score:.4f} (Threshold: {threshold:.3f})\n\n")
        
        # 1. Age Table
        rep.write("## 1. Stale Skills (>90 Days Unmodified)\n\n")
        if stale_skills:
            rep.write("| Skill Path | Last Modified Age (Days) | Status |\n")
            rep.write("| :--- | :--- | :--- |\n")
            for item in stale_skills[:20]:
                status = "🔴 Critical" if item["age_days"] > 120 else "⚠️ Warning"
                rep.write(f"| [{item['file']}](file://hermes_home/skills/{item['file']}) | {item['age_days']} | {status} |\n")
            if len(stale_skills) > 20:
                rep.write(f"\n*...and {len(stale_skills) - 20} more stale files.*\n")
        else:
            rep.write("✅ Zero stale files found!\n")
        rep.write("\n")
        
        # 2. Vague Instructions Table
        rep.write("## 2. Vague / Ambiguous Instructions\n\n")
        if vague_instructions:
            rep.write("| File | Line | Vague Instruction | Keyword Flag |\n")
            rep.write("| :--- | :--- | :--- | :--- |\n")
            for item in vague_instructions[:30]:
                rep.write(f"| [{item['file']}](file://hermes_home/skills/{item['file']}) | {item['line_no']} | `{item['text']}` | **{item['keyword']}** |\n")
            if len(vague_instructions) > 30:
                rep.write(f"\n*...and {len(vague_instructions) - 30} more ambiguous instructions.*\n")
        else:
            rep.write("✅ Zero ambiguous instructions found!\n")
        rep.write("\n")
        
        # 3. Duplicate Content (DRY violations)
        rep.write("## 3. Duplicate Paragraph Blocks (DRY Violations)\n\n")
        if duplicate_paragraphs:
            rep.write("| File A | File B | Duplicate Content Snippet |\n")
            rep.write("| :--- | :--- | :--- |\n")
            for item in duplicate_paragraphs[:20]:
                rep.write(f"| [{item['file_a']}](file://hermes_home/skills/{item['file_a']}) | [{item['file_b']}](file://hermes_home/skills/{item['file_b']}) | `{item['text']}` |\n")
            if len(duplicate_paragraphs) > 20:
                rep.write(f"\n*...and {len(duplicate_paragraphs) - 20} more duplicate blocks.*\n")
        else:
            rep.write("✅ Zero duplicate blocks found!\n")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Scan S7G skill ecosystem for sediment and duplication"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.10,
        help="Sediment score threshold (default: 0.10)"
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Root path to scan (default: current directory)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="ecosystem_sediment_report.md",
        help="Output report file (default: ecosystem_sediment_report.md)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format (for CI integration)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose output"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    root_path = Path(args.path).resolve()
    report_path = Path(args.output).resolve()
    
    if not root_path.exists():
        if not args.quiet:
            print(f"Error: Target path {root_path} does not exist.")
        sys.exit(1)
        
    scan_results = scan_skills(root_path)
    
    # Calculate sediment score
    issues_count = len(scan_results["vague_instructions"]) + len(scan_results["duplicate_paragraphs"])
    sediment_score = issues_count / max(1, scan_results["instructions_analyzed"])
    exceeds_threshold = sediment_score > args.threshold
    
    if args.json:
        output_data = {
            "sediment_score": sediment_score,
            "threshold": args.threshold,
            "exceeds_threshold": exceeds_threshold,
            "status": "FAIL" if exceeds_threshold else "PASS",
            "files_scanned": scan_results["files_scanned"],
            "instructions_analyzed": scan_results["instructions_analyzed"],
            "findings": {
                "vague_instructions_count": len(scan_results["vague_instructions"]),
                "duplicate_blocks_count": len(scan_results["duplicate_paragraphs"]),
                "stale_files_count": len(scan_results["stale_skills"]),
                "stale_files": scan_results["stale_skills"][:10],
                "vague_instructions": scan_results["vague_instructions"][:10],
                "duplicate_paragraphs": scan_results["duplicate_paragraphs"][:10]
            }
        }
        print(json.dumps(output_data, indent=2))
        sys.exit(1 if exceeds_threshold else 0)
        
    # Markdown Output
    generate_report(scan_results, sediment_score, args.threshold, report_path)
    
    if not args.quiet:
        print(f"📊 Report generated: {report_path}")
        print(f"📈 Sediment Score: {sediment_score:.4f} (threshold: {args.threshold:.3f})")
        if exceeds_threshold:
            print(f"❌ FAILED: Sediment score exceeds threshold of {args.threshold:.3f}")
            sys.exit(1)
        else:
            print(f"✅ PASSED: Sediment score is within threshold")
            sys.exit(0)

if __name__ == "__main__":
    main()
