# 📚 kube-lintd Rule Reference

| Rule ID | Severity | Title |
|---------|----------|-------|
| K8S-CT-001 | warning | Missing resource limits |
| K8S-CT-002 | high | Privileged mode enabled |
| K8S-CT-003 | info | imagePullPolicy set to Always |
| K8S-CT-004 | info | readOnlyRootFilesystem not enabled |
| K8S-CT-005 | warning | Image has no tag |
| K8S-CT-006 | warning | Using latest tag |
| K8S-PD-001 | high | Pod running as UID 0 (root) |
| K8S-PD-002a | warning | hostNetwork enabled in Pod spec |
| K8S-PD-002b | warning | hostNetwork enabled in Pod template |
| K8S-PD-003 | info | Duplicate image usage across containers |
| K8S-YAML-001 | high | YAML parsing failed |

---
## K8S-CT-001 — Missing resource limits
**Severity:** `warning`

**Description:**

Containers should explicitly define CPU and memory limits to prevent resource contention and overcommitment.

## K8S-CT-002 — Privileged mode enabled
**Severity:** `high`

**Description:**

Privileged containers have full access to the host. Avoid unless absolutely necessary.

## K8S-CT-003 — imagePullPolicy set to Always
**Severity:** `info`

**Description:**

'imagePullPolicy: Always' is best avoided for static pods or when image tags are versioned explicitly.

## K8S-CT-004 — readOnlyRootFilesystem not enabled
**Severity:** `info`

**Description:**

Enables immutability within the container and reduces risk of tampering.

## K8S-CT-005 — Image has no tag
**Severity:** `warning`

**Description:**

Always pin images with a tag to avoid pulling unintended versions.

## K8S-CT-006 — Using latest tag
**Severity:** `warning`

**Description:**

Avoid using the 'latest' tag in production as it can lead to non-deterministic deployments.

## K8S-PD-001 — Pod running as UID 0 (root)
**Severity:** `high`

**Description:**

Run pods as non-root wherever possible to reduce security risks.

## K8S-PD-002a — hostNetwork enabled in Pod spec
**Severity:** `warning`

**Description:**

Avoid using hostNetwork unless specifically required, as it exposes the Pod to host-level networking.

## K8S-PD-002b — hostNetwork enabled in Pod template
**Severity:** `warning`

**Description:**

Avoid using hostNetwork in controllers like Deployment or DaemonSet templates.

## K8S-PD-003 — Duplicate image usage across containers
**Severity:** `info`

**Description:**

Consider using separate images for distinct responsibilities within a Pod.

## K8S-YAML-001 — YAML parsing failed
**Severity:** `high`

**Description:**

The provided YAML file is syntactically invalid. Check indentation and formatting on the indicated line.

