def validate_pod(spec, template_spec, containers, rules, errors):
    # --- Rule: hostNetwork: true (spec level) → K8S-PD-002a ---
    if isinstance(spec, dict) and spec.get("hostNetwork") is True:
        errors.append({
            "id": "K8S-PD-002a",
            "message": "Use of 'hostNetwork: true' detected in Pod spec. Avoid unless explicitly required.",
            "severity": "warning"
        })

    # --- Rule: hostNetwork: true (template spec level) → K8S-PD-002b ---
    if isinstance(template_spec, dict) and template_spec.get("hostNetwork") is True:
        errors.append({
            "id": "K8S-PD-002b",
            "message": "Use of 'hostNetwork: true' inside Pod template. Avoid unless explicitly required.",
            "severity": "warning"
        })

    # --- Rule: runAsUser = 0 → K8S-PD-001 ---
    pod_ctx = template_spec.get("securityContext", spec.get("securityContext", {}))
    if isinstance(pod_ctx, dict) and pod_ctx.get("runAsUser") == 0:
        errors.append({
            "id": "K8S-PD-001",
            "message": "Pod is running as user ID 0 (root). Use a non-root UID for better security.",
            "severity": "high"
        })

    # --- Rule: duplicate images in containers → K8S-PD-003 ---
    image_count = {}
    for container in containers:
        image = container.get("image", "<none>")
        image_count[image] = image_count.get(image, 0) + 1
    for image, count in image_count.items():
        if count > 1:
            errors.append({
                "id": "K8S-PD-003",
                "message": f"Image '{image}' used in {count} containers. Consider separating responsibilities.",
                "severity": "info"
            })

