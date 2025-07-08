def validate_container(container, rules, errors):
    cname = container.get("name", "<unnamed>")

    if rules.get("requireResourceLimits", True):
        resources = container.get("resources", {})
        limits = resources.get("limits", {})
        if not limits:
            errors.append(f"Container '{cname}' has no resource limits. Set cpu/memory limits explicitly.")

    if rules.get("enforcePrivileged", True):
        sc = container.get("securityContext", {})
        if isinstance(sc, dict) and sc.get("privileged") is True:
            errors.append(f"Container '{cname}' is running in privileged mode. This is discouraged.")

    if rules.get("warnOnImagePullPolicyAlways", True):
        if container.get("imagePullPolicy") == "Always":
            errors.append(f"Container '{cname}' uses 'imagePullPolicy: Always'. Avoid for static pods or production.")

    sc = container.get("securityContext", {})
    if isinstance(sc, dict):
        ro_root = sc.get("readOnlyRootFilesystem")
        if ro_root is not True:
            errors.append(f"Container '{cname}' does not enable readOnlyRootFilesystem. Recommended for immutability.")

    image = container.get("image", "")
    if ":" not in image:
        errors.append(f"Container '{cname}' image '{image}' has no tag specified.")
    elif image.endswith(":latest"):
        errors.append(f"Container '{cname}' is using 'latest' tag. Pin to a version.")

