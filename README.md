# kube-lintd 🧹📦

A lightweight real-time linter and validator for static Kubernetes pod manifests.

Static pods can silently break clusters when misconfigured. `kube-lintd` watches your static manifest directory (like `/etc/kubernetes/manifests`) and provides instant feedback on schema issues, invalid YAML, and common pitfalls — before kubelet throws cryptic errors.

---

## ✨ Features

- ✅ Watches static pod YAMLs in real-time
- 🧪 Validates YAML syntax and Kubernetes schema
- 💡 Detects common mistakes: bad indentation, wrong fields, missing `kind`, etc.
- 🧠 (Soon) Explains kubelet errors using natural language
- 🖥️ Optional Web UI and log viewer coming soon
- 🔌 Works anywhere: bare metal, VMs, CI/CD

---

## 📦 Quickstart (Developer Mode)

```bash
git clone https://github.com/your-username/kube-lintd.git
cd kube-lintd
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python -m kube_lintd.cli --watch /etc/kubernetes/manifests
```
----
# Want to lint a single file?
python -m kube_lintd.cli --file /path/to/manifest.yaml

# 🔍 Sample Output

[✓] kube-apiserver.yaml: Valid
[!] etcd.yaml: Line 12 — missing '-' before 'name'
[!] scheduler.yaml: Unknown field 'namspace'. Did you mean 'namespace'?

-----

# 🛣 Roadmap
[x] CLI: Watch & lint in real-time

[ ] Web UI for validation and visual diffs

[ ] Live kubelet log parser + error explainer

[ ] GitHub Actions & CI/CD support

[ ] Offline-friendly schema bundle

----------
# 🤝 Contributing
PRs welcome! Whether it's a new linter rule, integration, or test — jump in.

----------
# 📜 License
MIT License. Built with ❤️ to help engineers everywhere ship safer clusters.


---

Next up, I’ll scaffold the `cli.py` and `linter.py` files so you can run your first `--file` check and start watching folders in real time.

Ready to see your tool come to life? Let’s ship it 🔧💻

-----------
