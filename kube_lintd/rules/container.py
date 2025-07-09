def validate_container(container, rules, errors):
    cname = container.get("name", "<unnamed>")

    # Rule: Resource limits (K8S-CT-001)
    if rules.get("requireResourceLimits", True):
        resources = container.get("resources", {})
        limits = resources.get("limits", {})
        if not limits:
            errors.append({
                "id": "K8S-CT-001",
                "message": f"Container '{cname}' has no resource limits. Set cpu/memory limits explicitly.",
                "severity": "warning"
            })

    # Rule: Privileged mode (K8S-CT-002)
    if rules.get("enforcePrivileged", True):
        sc = container.get("securityContext", {})
        if isinstance(sc, dict) and sc.get("privileged") is True:
            errors.append({
                "id": "K8S-CT-002",
                "message": f"Container '{cname}' is running in privileged mode. This is discouraged.",
                "severity": "high"
            })

    # Rule: imagePullPolicy: Always (K8S-CT-003)
    if rules.get("warnOnImagePullPolicyAlways", True):
        if container.get("imagePullPolicy") == "Always":
            errors.append({
                "id": "K8S-CT-003",
                "message": f"Container '{cname}' uses 'imagePullPolicy: Always'. Avoid for static pods or production.",
                "severity": "info"
            })

    # Rule: readOnlyRootFilesystem not enabled (K8S-CT-004)
    sc = container.get("securityContext", {})
    if isinstance(sc, dict):
        ro_root = sc.get("readOnlyRootFilesystem")
        if ro_root is not True:
            errors.append({
                "id": "K8S-CT-004",
                "message": f"Container '{cname}' does not enable readOnlyRootFilesystem. Recommended for immutability.",
                "severity": "info"
            })

    # Rule: Untagged images (K8S-CT-005)
    image = container.get("image", "")
    if ":" not in image:
        errors.append({
            "id": "K8S-CT-005",
            "message": f"Container '{cname}' image '{image}' has no tag specified.",
            "severity": "warning"
        })
    # Rule: 'latest' tag usage (K8S-CT-006)
    elif image.endswith(":latest"):
        errors.append({
            "id": "K8S-CT-006",
            "message": f"Container '{cname}' is using 'latest' tag. Pin to a version.",
            "severity": "warning"
        })

    # Rule: 'latest' tag usage (K8S-YAML-001)
    elif image.endswith(":latest"):
        errors.append({
            "id": "K8S-YAML-001",
            "message": f"Invalid YAML syntax at line 19, column 11: expected <block end>, but found '<scalar>'",
            "severity": "high"
        })

