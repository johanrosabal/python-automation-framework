from dataclasses import dataclass
from typing import Optional


@dataclass
class APIConfig:
    base_token_url: str
    base_url: str
    grant_type: str
    client_id: str
    client_secret: str


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
