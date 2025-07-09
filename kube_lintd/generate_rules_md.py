import os
import yaml

with open("rules_catalog.yaml", "r") as f:
    catalog = yaml.safe_load(f)

rules = catalog.get("rules", [])

with open("RULES.md", "w") as md:
    md.write("# 📚 kube-lintd Rule Reference\n\n")
    md.write("| Rule ID | Severity | Title |\n")
    md.write("|---------|----------|-------|\n")
    for r in rules:
        md.write(f"| {r['id']} | {r['severity']} | {r['title']} |\n")

    md.write("\n---\n")

    for r in rules:
        md.write(f"## {r['id']} — {r['title']}\n")
        md.write(f"**Severity:** `{r['severity']}`\n\n")
        md.write(f"**Description:**\n\n{r['description']}\n\n")

