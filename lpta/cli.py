import sys

from lpta.analysis.history_builder import build_history, save_history
from lpta.report import open_report, render_report, save_report

def main():
    """
    runs: python -m lpta.cli <source_file.c>.
    builds history and save it to the output/history.json.
    """

    if len(sys.argv)  < 2: 
        print("Usage: python -m lpta.cli <source_file.c>")
        sys.exit(1)

    source_path = sys.argv[1]
    history = build_history(source_path)

    save_history(history)

    html = render_report(history)
    report_path = save_report(html)
    print(f"Report saved to {report_path}")

    open_report(report_path)

if __name__ == "__main__":
    main()