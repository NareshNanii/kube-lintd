import argparse
import os
from kube_lintd.linter import lint_file

def main():
    parser = argparse.ArgumentParser(description="Static Pod YAML Linter")
    parser.add_argument('--file', type=str, help="Path to a single YAML file to lint")
    parser.add_argument('--watch', type=str, help="Directory to watch for YAML changes (coming soon)")

    args = parser.parse_args()

    if args.file:
        if os.path.isfile(args.file):
            print(f"🔍 Linting {args.file}...")
            lint_file(args.file)
        else:
            print(f"❌ File not found: {args.file}")
    elif args.watch:
        from kube_lintd.watcher import watch_directory
        watch_directory(args.watch)
    else:
        print("⚠️ Please specify --file <filename.yaml> or --watch <directory>")

if __name__ == "__main__":
    main()

