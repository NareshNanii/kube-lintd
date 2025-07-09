import argparse
import os
from kube_lintd.linter import lint_file
from rich.console import Console
from rich.table import Table
import yaml

def list_rules():
    catalog_path = os.path.join(os.path.dirname(__file__), "rules_catalog.yaml")
    if not os.path.exists(catalog_path):
        print("❌ Rule catalog not found.")

        return

    with open(catalog_path, "r") as f:
        catalog = yaml.safe_load(f)

    rules = catalog.get("rules", [])
    table = Table(title="🧾 kube-lintd Rule Catalog")
    table.add_column("ID", style="bold")
    table.add_column("Severity", style="cyan")
    table.add_column("Title", style="white")

    for rule in rules:
        table.add_row(rule.get("id"), rule.get("severity"), rule.get("title"))

    console = Console()
    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Static Pod YAML Linter")
    parser.add_argument('--file', type=str, help="Path to a single YAML file to lint")
    parser.add_argument('--watch', type=str, help="Directory to watch for YAML changes")
    parser.add_argument('--list-rules', action="store_true", help="Show all available lint rules")
    parser.add_argument('--rule-info', type=str, help="Show full info for a specific rule ID (e.g. K8S-CT-004)")
    args = parser.parse_args()

    if args.list_rules:
        list_rules()
    elif args.rule_info:
        show_rule_info(args.rule_info)
    elif args.file:
        if os.path.isfile(args.file):
            print(f"🔍 Linting {args.file}...")
            lint_file(args.file)
        else:
            print(f"❌ File not found: {args.file}")
    elif args.watch:
        from kube_lintd.watcher import watch_directory
        watch_directory(args.watch)
    else:
        print("  Please specify --file <filename.yaml>, --watch <directory>, or --list-rules")

def show_rule_info(rule_id):
    catalog_path = os.path.join(os.path.dirname(__file__), "rules_catalog.yaml")
    if not os.path.exists(catalog_path):
        print("❌ Rule catalog not found.")
        return

    with open(catalog_path, "r") as f:
        catalog = yaml.safe_load(f)

    match = next((r for r in catalog.get("rules", []) if r["id"] == rule_id), None)
    if match:
        console = Console()
        console.rule(f"[bold blue]{rule_id}[/bold blue]")
        console.print(f"[bold]Title:[/bold] {match.get('title')}")
        console.print(f"[bold]Severity:[/bold] {match.get('severity')}")
        console.print(f"[bold]Description:[/bold] {match.get('description')}")
    else:
        print(f"🔍 No rule found with ID '{rule_id}'. Try '--list-rules' to explore all.")
if __name__ == "__main__":
    main()

