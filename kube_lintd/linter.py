from ruamel.yaml import YAML

def lint_file(file_path):
    yaml = YAML()
    try:
        with open(file_path, 'r') as f:
            data = yaml.load(f)

        errors = []

        if not isinstance(data, dict):
            errors.append("Top-level YAML is not a dictionary")

        if 'apiVersion' not in data:
            errors.append("Missing 'apiVersion' field")

        if 'kind' not in data:
            errors.append("Missing 'kind' field")

        if 'metadata' not in data:
            errors.append("Missing 'metadata' section")
        elif 'name' not in data.get('metadata', {}):
            errors.append("Missing 'metadata.name' field")

        if errors:
            print(f"❌ {file_path} has {len(errors)} error(s):")
            for e in errors:
                print(f"   - {e}")
        else:
            print(f"✅ {file_path} looks valid")

    except Exception as e:
        print(f"❌ Error parsing {file_path}: {str(e)}")

