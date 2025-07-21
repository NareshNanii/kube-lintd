import argparse
import sys
from kube_lintd.linter import lint_file

def parse_args():
    parser = argparse.ArgumentParser(
        description="kube-lintd: A Kubernetes YAML linter for security and governance"
    )
    parser.add_argument(
        "file",
        type=str,
        help="Path to the Kubernetes manifest YAML file"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in structured JSON format"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        lint_file(args.file, output_json=args.json)
    except Exception as e:
        print(f"❌ Failed to lint file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()



