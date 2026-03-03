import yaml
from core.config.config_yaml import (ApiStandardConfig,
                                     WebStandardConfig,
                                     WebSoftshipConfig,
                                     DesktopStandardConfig,
                                     APIConfig,
                                     ApiLoadIQConfig,
                                     ApiLoadIQEndpointsConfig,
                                     WEBConfig,
                                     WebSoftshipModules,
                                     UserConfig,
                                     DatabaseConfig,
                                     DESKTOPConfig)


''' 
This is exclusive use for standard LoadIQProject application, using Endpoints Functionality
'''


def load_iq_api_config(file_path):
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)

    # Map Classes Structure
    config = ApiLoadIQConfig(
        name=config_data["name"],
        api=APIConfig(**config_data["api"]),
        user=UserConfig(**config_data["user"]),
        database=DatabaseConfig(**config_data["database"]),
        endpoints=ApiLoadIQEndpointsConfig(**config_data["endpoints"]),
    )

    return config


''' 
This is exclusive use for standard Softship Web Project application, using Modules
'''


def load_web_softship_config(file_path):
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)

    # Map Classes Structure
    config = WebSoftshipConfig(
        name=config_data["name"],
        web=WEBConfig(**config_data["web"]),
        modules=WebSoftshipModules(**config_data["modules"]),
        user=UserConfig(**config_data["user"]),
        database=DatabaseConfig(**config_data["database"])
    )

    return config


''' 
This is used for Standard API application
'''


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


''' 
This is used for Standard WEB application
'''


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


''' 
This is used for Standard DESKTOP application
'''


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
