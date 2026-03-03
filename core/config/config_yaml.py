from dataclasses import dataclass
from typing import Optional


@dataclass
class WEBConfig:
    base_url: str
    browser: str


@dataclass
class DESKTOPConfig:
    application: str


@dataclass
class APIConfig:
    base_token_url: str
    base_url: str
    grant_type: str
    client_id: str
    client_secret: str


@dataclass
class WebSoftshipModules:
    contracts: str
    finance: str
    commercial: str
    configuration: str
    booking: str
    sof: str
    master_data: str


@dataclass
class ApiLoadIQEndpointsConfig:
    loadboard: str
    trackntrace: str
    user_management: str
    location: str
    tmsexchange: str


@dataclass
class UserConfig:
    username: str
    password: str


@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    name: str
    ssl: bool


@dataclass
class ApiStandardConfig:
    name: str
    api: APIConfig
    user: UserConfig
    database: DatabaseConfig


@dataclass
class ApiLoadIQConfig:
    name: str
    api: APIConfig
    user: UserConfig
    database: DatabaseConfig
    endpoints: ApiLoadIQEndpointsConfig


@dataclass
class WebStandardConfig:
    name: str
    web: WEBConfig
    user: UserConfig
    database: DatabaseConfig


@dataclass
class DesktopStandardConfig:
    name: str
    desktop: DESKTOPConfig
    user: UserConfig


@dataclass
class WebSoftshipConfig:
    name: str
    modules: WebSoftshipModules
    web: WEBConfig
    user: UserConfig
    database: DatabaseConfig
