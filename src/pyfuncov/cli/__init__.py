"""CLI interface for pyfuncov."""

import argparse
import sys

from pyfuncov import compare_reports, generate_report, load_coverage


def cmd_report(args):
    """Generate a coverage report."""
    try:
        load_coverage(args.file)
        report = generate_report(format=args.format)
        print(report)
    except FileNotFoundError:
        print(f"Error: Coverage file not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_diff(args):
    """Compare two coverage runs."""
    try:
        # Load baseline
        load_coverage(args.baseline)
        from pyfuncov import get_coverage_data
        baseline_data = get_coverage_data()
        baseline = baseline_data.covergroups

        # Reset and load current
        from pyfuncov import reset_coverage_data
        reset_coverage_data()
        load_coverage(args.current)
        current_data = get_coverage_data()
        current = current_data.covergroups

        # Compare
        result = compare_reports({"covergroups": baseline}, {"covergroups": current})

        # Output results
        print("Coverage Comparison")
        print("=" * 40)
        print(f"Baseline: {result['baseline_overall']:.2f}%")
        print(f"Current:  {result['current_overall']:.2f}%")
        print(f"Diff:     {result['difference']:+.2f}%")

        if result["regressions"]:
            print("\nRegressions:")
            for r in result["regressions"]:
                print(f"  - {r['covergroup']}: {r['baseline']}% -> {r['current']}% ({r['difference']:+.2f}%)")

        if result["improvements"]:
            print("\nImprovements:")
            for i in result["improvements"]:
                print(f"  + {i['covergroup']}: {i['baseline']}% -> {i['current']}% ({i['difference']:+.2f}%)")

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="pyfuncov - Python Functional Coverage Tool"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # report command
    report_parser = subparsers.add_parser("report", help="Generate coverage report")
    report_parser.add_argument("file", help="Coverage data file (JSON)")
    report_parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    report_parser.set_defaults(func=cmd_report)

    # diff command
    diff_parser = subparsers.add_parser("diff", help="Compare coverage runs")
    diff_parser.add_argument("baseline", help="Baseline coverage file")
    diff_parser.add_argument("current", help="Current coverage file")
    diff_parser.set_defaults(func=cmd_diff)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
