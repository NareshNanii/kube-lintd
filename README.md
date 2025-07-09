# 🧹 kube-lintd — Secure Your Static Pods Before kubelet Breaks

`kube-lintd` is a fast, customizable linter and validator for static Kubernetes Pod manifests. It detects YAML issues, security misconfigurations, and deployment risks **before** kubelet fails silently or throws cryptic errors.

> 🔍 Perfect for CI/CD pipelines, clusters, and local dev workspaces.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## ✨ Features

- 🔎 Lint static Pod files instantly with rich output
- 👀 Watch directories like `/etc/kubernetes/manifests/` in real-time
- 🔐 Detect `privileged: true`, `hostNetwork`, root containers, and more
- 📚 Explore all rules with `--list-rules` and detailed `--rule-info`
- 📄 Auto-generate `RULES.md` from your YAML catalog
- 🧠 (Coming soon) Explain kubelet errors using natural language
- 🖥️ Optional web UI under development

---

## ⚡ Quickstart

```bash
git clone https://github.com/your-username/kube-lintd.git
cd kube-lintd
python3 -m venv venv
source venv/bin/activate
pip install -e .
'''

---

## 🚀 Usage

# Lint a specific YAML manifest
kube-lintd --file path/to/pod.yaml

# Watch a directory for changes (like kubelet)
kube-lintd --watch /etc/kubernetes/manifests

# Explore rules
kube-lintd --list-rules

# Detailed info about a rule
kube-lintd --rule-info K8S-CT-004

---

Example output:

[✓] kube-apiserver.yaml: Valid
[!] etcd.yaml: Line 12 — missing '-' before 'name'
[!] controller.yaml: Uses 'hostNetwork: true' and runs as UID 0

---

📚 Rule Catalog

Use built-in commands to explore:

kube-lintd --list-rules
kube-lintd --rule-info K8S-PD-001

Or check out the full 📘 RULES.md

---

⚙️ Example .kube-lintd.yaml Config

ignore:
  - K8S-CT-004
fail_on: warning
rules_catalog_path: kube_lintd/rules_catalog.yaml

(Note: CLI config support is planned for a future release)

---

🔍 YAML Before & After

Before: insecure static pod

apiVersion: v1
kind: Pod
metadata:
  name: insecure-pod
spec:
  containers:
    - name: nginx
      image: nginx

---

After: safer, production-ready

apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  containers:
    - name: nginx
      image: nginx:1.25
      resources:
        limits:
          cpu: "500m"
          memory: "256Mi"
      securityContext:
        runAsNonRoot: true
        readOnlyRootFilesystem: true

---

🛣️ Roadmap

[x] CLI: file + directory linting

[x] YAML-based rule catalog

[x] Markdown rule doc generator

[ ] Web UI for visual feedback

[ ] kubelet log explainer

[ ] GitHub Action / CI/CD integration

[ ] YAML fix suggestions (--fix)

[ ] JSON output & structured annotations

---

🤝 Contributing
Pull requests welcome! Whether it’s a new rule, better docs, or a feature suggestion — we’d love to hear from you.

---

📜 License
MIT License — Built with ❤️ to help engineers ship safer clusters.
