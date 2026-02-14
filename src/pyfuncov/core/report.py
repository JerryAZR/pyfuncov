"""Report generation for coverage analysis."""

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class CovergroupReport:
    """Report for a single covergroup."""

    name: str
    coverage: float
    total_bins: int
    hit_bins: int
    coverpoints: List[Dict]
    missed_bins: List[str]


@dataclass
class CoverageReport:
    """Complete coverage report."""

    overall_coverage: float
    covergroups: List[CovergroupReport]
    missed_bins: List[str]
    generated_at: datetime
    version: str = "1.0"


def calculate_coverage(cg_data: Dict) -> tuple[float, int, int, List[str]]:
    """Calculate coverage for a covergroup.

    Args:
        cg_data: Covergroup data dictionary

    Returns:
        Tuple of (coverage_percent, total_bins, hit_bins, missed_bin_names)
    """
    total_bins = 0
    hit_bins = 0
    missed_bins = []

    coverpoints_data = cg_data.get("coverpoints", {})

    for cp_name, cp_data in coverpoints_data.items():
        bins_data = cp_data.get("bins", {}).get("bins", {})

        for bin_name, bin_info in bins_data.items():
            total_bins += 1
            hits = bin_info.get("hits", 0)
            if hits > 0:
                hit_bins += 1
            else:
                missed_bins.append(bin_name)

    if total_bins == 0:
        coverage = 0.0
    else:
        coverage = (hit_bins / total_bins) * 100

    return coverage, total_bins, hit_bins, missed_bins


def generate_text_report(coverage_data: Dict, version: str = "1.0") -> str:
    """Generate a human-readable text report.

    Args:
        coverage_data: Coverage data dictionary
        version: Coverage data format version

    Returns:
        Formatted text report string
    """
    lines = []
    lines.append("=" * 80)
    lines.append("Coverage Report")
    lines.append("=" * 80)

    total_bins = 0
    hit_bins = 0
    all_missed = []

    covergroups = coverage_data.get("covergroups", {})

    for cg_name, cg_data in covergroups.items():
        coverage, cg_total, cg_hit, missed = calculate_coverage(cg_data)

        lines.append(f"\nCovergroup: {cg_name}")
        lines.append(f"  Coverage: {coverage:.2f}% ({cg_hit}/{cg_total} bins)")

        total_bins += cg_total
        hit_bins += cg_hit
        all_missed.extend(missed)

    overall = (hit_bins / total_bins * 100) if total_bins > 0 else 0.0

    lines.append("\n" + "=" * 80)
    lines.append(f"Overall Coverage: {overall:.2f}% ({hit_bins}/{total_bins} bins)")
    lines.append("=" * 80)

    if all_missed:
        lines.append(f"\nMissed Bins ({len(all_missed)}):")
        for bin_name in all_missed:
            lines.append(f"  - {bin_name}")

    return "\n".join(lines)


def generate_json_report(coverage_data: Dict, version: str = "1.0") -> str:
    """Generate a JSON report for CI/CD integration.

    Args:
        coverage_data: Coverage data dictionary
        version: Coverage data format version

    Returns:
        JSON string report
    """
    covergroups_report = []
    all_missed = []

    total_bins = 0
    hit_bins = 0

    covergroups = coverage_data.get("covergroups", {})

    for cg_name, cg_data in covergroups.items():
        coverage, cg_total, cg_hit, missed = calculate_coverage(cg_data)

        coverpoints = []
        cp_data = cg_data.get("coverpoints", {})
        for cp_name, cp in cp_data.items():
            bins_list = []
            bins_dict = cp.get("bins", {}).get("bins", {})
            for bin_name, bin_info in bins_dict.items():
                bins_list.append({
                    "name": bin_name,
                    "hits": bin_info.get("hits", 0),
                })
            coverpoints.append({
                "name": cp_name,
                "bins": bins_list,
            })

        covergroups_report.append({
            "name": cg_name,
            "coverage": round(coverage, 2),
            "total_bins": cg_total,
            "hit_bins": cg_hit,
            "coverpoints": coverpoints,
        })

        total_bins += cg_total
        hit_bins += cg_hit
        all_missed.extend(missed)

    overall = (hit_bins / total_bins * 100) if total_bins > 0 else 0.0

    report = {
        "version": version,
        "overall_coverage": round(overall, 2),
        "total_bins": total_bins,
        "hit_bins": hit_bins,
        "covergroups": covergroups_report,
        "missed_bins": all_missed,
        "generated_at": datetime.now().isoformat(),
    }

    return json.dumps(report, indent=2)


def compare_reports(baseline_data: Dict, current_data: Dict) -> Dict:
    """Compare two coverage reports to identify regressions.

    Args:
        baseline_data: Baseline coverage data
        current_data: Current coverage data

    Returns:
        Comparison result dictionary
    """
    baseline_covergroups = baseline_data.get("covergroups", {})
    current_covergroups = current_data.get("covergroups", {})

    results = {
        "baseline_overall": 0.0,
        "current_overall": 0.0,
        "difference": 0.0,
        "regressions": [],
        "improvements": [],
    }

    # Calculate overall coverage for baseline
    baseline_total = 0
    baseline_hit = 0
    for cg_name, cg_data in baseline_covergroups.items():
        _, total, hit, _ = calculate_coverage(cg_data)
        baseline_total += total
        baseline_hit += hit
    results["baseline_overall"] = (baseline_hit / baseline_total * 100) if baseline_total > 0 else 0.0

    # Calculate overall coverage for current
    current_total = 0
    current_hit = 0
    for cg_name, cg_data in current_covergroups.items():
        _, total, hit, _ = calculate_coverage(cg_data)
        current_total += total
        current_hit += hit
    results["current_overall"] = (current_hit / current_total * 100) if current_total > 0 else 0.0

    results["difference"] = results["current_overall"] - results["baseline_overall"]

    # Find regressions and improvements per covergroup
    all_cgs = set(baseline_covergroups.keys()) | set(current_covergroups.keys())
    for cg_name in all_cgs:
        baseline_cg = baseline_covergroups.get(cg_name, {})
        current_cg = current_covergroups.get(cg_name, {})

        baseline_cov, _, _, _ = calculate_coverage(baseline_cg)
        current_cov, _, _, _ = calculate_coverage(current_cg)

        diff = current_cov - baseline_cov

        if diff < 0:
            results["regressions"].append({
                "covergroup": cg_name,
                "baseline": round(baseline_cov, 2),
                "current": round(current_cov, 2),
                "difference": round(diff, 2),
            })
        elif diff > 0:
            results["improvements"].append({
                "covergroup": cg_name,
                "baseline": round(baseline_cov, 2),
                "current": round(current_cov, 2),
                "difference": round(diff, 2),
            })

    return results


def generate_report(format: str = "text", data: Optional[Dict] = None) -> str:
    """Generate a coverage report.

    Args:
        format: Output format ("text" or "json")
        data: Coverage data dictionary (if None, returns empty report)

    Returns:
        Formatted report string
    """
    if data is None:
        data = {}

    version = data.get("version", "1.0")

    if format == "json":
        return generate_json_report(data, version)
    else:
        return generate_text_report(data, version)
