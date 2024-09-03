import yaml
from core.config.config_yaml import (ApiStandardConfig,
                                     WebStandardConfig,
                                     DesktopStandardConfig,
                                     APIConfig,
                                     WEBConfig,
                                     UserConfig,
                                     DatabaseConfig,
                                     DESKTOPConfig)


def load_api_config(file_path):
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)

    # Map Classes Structure
    config = ApiStandardConfig(
        name=config_data["name"],
        api=APIConfig(**config_data["api"]),
        user=UserConfig(**config_data["user"]),
        database=DatabaseConfig(**config_data["database"])
    )

    return config


def load_web_config(file_path):
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)

    # Map Classes Structure
    config = WebStandardConfig(
        name=config_data["name"],
        web=WEBConfig(**config_data["web"]),
        user=UserConfig(**config_data["user"]),
        database=DatabaseConfig(**config_data["database"])
    )

    return config


def load_desktop_config(file_path):
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)

        # Map Classes Structure
    config = DesktopStandardConfig(
        name=config_data["name"],
        desktop=DESKTOPConfig(**config_data["desktop"]),
        user=UserConfig(**config_data["user"])
    )

    return config
