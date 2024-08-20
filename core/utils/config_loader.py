import yaml
from pathlib import Path


def load_config(request):
    profile = request.config.getoption("--profile")
    app_name = request.config.getoption("--app-name")
    app_type = request.config.getoption("--app-type")

    # Root Project
    project_root = Path(__file__).resolve().parent
    print(f"{project_root}")

    # Define the path based on the application and profile
    config_path = project_root / f'applications/{app_type}/{app_name}/config/{profile}_config.yaml'
    print(f"Config path: {config_path}")

    if not config_path.exists():
        raise FileNotFoundError(f"The config file {config_path} does not exist.")

    # Read the YAML file
    with open(config_path, 'r') as file:
        config_data = yaml.safe_load(file)

    # Return the configuration for use in tests
    return config_data
