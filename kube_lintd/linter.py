import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from ruamel.yaml import YAML
from colorama import Fore, Style, init
from difflib import get_close_matches
from kube_lintd.rules.container import validate_container
init(autoreset=True)

# Setup logging
LOG_DIR = os.path.expanduser("~/.kube-lintd/logs")
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, f"lint-{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)

def init_logger():
    logger = logging.getLogger("kube-lintd")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # 🧼 Clear existing handlers to prevent duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', "%H:%M:%S")

    # Log to daily file lint-YYYY-MM-DD.log
    dated_log_path = os.path.join(LOG_DIR, f"lint-{datetime.now().strftime('%Y-%m-%d')}.log")
    date_handler = logging.FileHandler(dated_log_path)
    date_handler.setFormatter(formatter)
    logger.addHandler(date_handler)

    # Log to rotating file: kube-lintd.log
    rolling_log_path = os.path.join(LOG_DIR, "kube-lintd.log")
    handler = RotatingFileHandler(rolling_log_path, maxBytes=1_000_000, backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = init_logger()


# Define valid top-level fields for a Pod manifest
VALID_FIELDS = {"apiVersion", "kind", "metadata", "spec", "status"}

def suggest_field_name(field):
    matches = get_close_matches(field, VALID_FIELDS, n=1, cutoff=0.7)
    if matches:
        return matches[0]
    return None

def load_config():
    import yaml as pyyaml  # use PyYAML just for config
    config_paths = [
        os.path.join(os.getcwd(), ".kube-lintd.yaml"),
        os.path.expanduser("~/.kube-lintd.yaml")
    ]
    for path in config_paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                return pyyaml.safe_load(f).get("rules", {})
    return {}

rules = load_config()


def lint_file(file_path):
    yaml = YAML()
    containers = []
    logger.info(f"🔁 Lint triggered for: {file_path}")

    try:
        print(f"{Fore.YELLOW}🔍 Linting {file_path}...")
        with open(file_path, "r") as f:
            data = yaml.load(f)

        errors = []

        # Validate basic structure
        if not isinstance(data, dict):
            errors.append("Top-level YAML is not a dictionary")
        else:
            for key in data:
                if key not in VALID_FIELDS:
                    suggestion = suggest_field_name(key)
                    if suggestion:
                        errors.append(f"Unknown top-level field '{key}'. Did you mean '{suggestion}'?")
                    else:
                        errors.append(f"Unknown top-level field '{key}'")

        # Required fields
        if "apiVersion" not in data:
            errors.append("Missing 'apiVersion' field")
        if "kind" not in data:
            errors.append("Missing 'kind' field")
        if "metadata" not in data:
            errors.append("Missing 'metadata' section")
        elif "name" not in data["metadata"]:
            errors.append("Missing 'metadata.name' field")

        # Extract spec and containers
        spec = data.get("spec", {})
        template_spec = spec.get("template", {}).get("spec", {})
        containers = template_spec.get("containers") or spec.get("containers", [])
        logger.debug(f"Resolved {len(containers)} containers from manifest.")

        # De-duplicate containers by name
        seen = set()
        unique = []
        for c in containers:
            cname = c.get("name")
            if cname and cname not in seen:
                seen.add(cname)
                unique.append(c)
        containers = unique

        # ✅ Unified container-level validation
        for container in containers:
            validate_container(container, rules, errors)

        # --- Pod-level Rule: hostNetwork ---
        if isinstance(spec, dict) and spec.get("hostNetwork") is True:
            errors.append("Use of 'hostNetwork: true' detected. Avoid unless explicitly required.")
        if isinstance(template_spec, dict) and template_spec.get("hostNetwork") is True:
            errors.append("Use of 'hostNetwork: true' inside Pod template detected. Avoid unless explicitly required.")

        # --- Pod-level Rule: runAsUser = 0 ---
        pod_ctx = template_spec.get("securityContext", spec.get("securityContext", {}))
        if isinstance(pod_ctx, dict) and pod_ctx.get("runAsUser") == 0:
            errors.append("Pod is running as user ID 0 (root). Use a non-root UID for better security.")

        # --- Pod-level Rule: duplicate image detection ---
        image_count = {}
        for c in containers:
            image = c.get("image", "<none>")
            image_count[image] = image_count.get(image, 0) + 1
        for image, count in image_count.items():
            if count > 1:
                errors.append(f"Image '{image}' used in {count} containers. Consider separating responsibilities.")

        # Logging results
        if errors:
            print(f"{Fore.RED}❌ {file_path} has {len(errors)} error(s):")
            for e in errors:
                print(f"{Fore.RED}   - {e}")
            logger.warning(f"{file_path} ❌ ({len(errors)} error[s])")
            for e in errors:
                logger.warning(f"   - {e}")
        else:
            print(f"{Fore.GREEN}✅ {file_path} looks valid")
            logger.info(f"{file_path} ✅")

    except Exception as e:
        err = f"❌ Error parsing {file_path}: {str(e)}"
        print(f"{Fore.RED}{err}")
        logger.error(err)


