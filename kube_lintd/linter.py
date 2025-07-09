import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from kube_lintd.rules.pod import validate_pod
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
                config = pyyaml.safe_load(f) or {}
                return {
                    "rules": config.get("rules", {}),
                    "ignore": config.get("ignore", [])
                }
    return {"rules": {}, "ignore": []}



def lint_file(file_path, output_json=False):
    yaml = YAML()
    config = load_config()
    rules = config["rules"]
    ignore_ids = set(config["ignore"])
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
        validate_pod(spec, template_spec, containers, rules, errors)

        if output_json:
            import json
            output = {
                "file": file_path,
                "errors": errors
            }
            print(json.dumps(output, indent=2))
        else:
            if errors:
                print(f"{Fore.RED}❌ {file_path} has {len(errors)} issue(s):")

                for e in errors:
                    icon = {
                        "high": "🔥",
                        "warning": "⚠️",
                        "info": "🛈"
                    }.get(e.get("severity", "info"), "🛈")

                    color = {
                        "high": Fore.RED,
                        "warning": Fore.YELLOW,
                        "info": Fore.BLUE
                    }.get(e.get("severity", "info"), Fore.WHITE)
                    eid = e.get("id", "N/A")
                    severity = e.get("severity", "info")
                    message = e.get("message", str(e))

                    print(f"   {color}{icon} [{e.get('id')}] ({e.get('severity')}) {e.get('message')}{Style.RESET_ALL}")

                logger.warning(f"{file_path} ❌ ({len(errors)} issue[s])")
                for e in errors:
                    logger.warning(f"   - [{e.get('id')}] {e.get('severity').upper()}: {e.get('message')}")
            else:
                print(f"{Fore.GREEN}✅ {file_path} looks valid")
                logger.info(f"{file_path} ✅")


    except Exception as e:
        err = f"❌ Error parsing {file_path}: {str(e)}"
        print(f"{Fore.RED}{err}")
        logger.error(err)


