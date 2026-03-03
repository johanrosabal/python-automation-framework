import sys


def get_profile():
    for arg in sys.argv:
        if arg.startswith("--profile="):
            return arg.split("=")[1]
    return None


def get_app_name():
    for arg in sys.argv:
        if arg.startswith("--app-name="):
            return arg.split("=")[1]
    return None


def get_app_type():
    for arg in sys.argv:
        if arg.startswith("--app-type="):
            return arg.split("=")[1]
    return None


def get_app_endpoint():
    for arg in sys.argv:
        if arg.startswith("--app-endpoint="):
            return arg.split("=")[1]
    return None


def get_app_module():
    for arg in sys.argv:
        if arg.startswith("--app-module="):
            return arg.split("=")[1]
    return None


def get_browser():
    for arg in sys.argv:
        if arg.startswith("--browser="):
            return arg.split("=")[1]
    return None


def get_headless():
    for arg in sys.argv:
        if arg.startswith("--headless="):
            return arg.split("=")[1]
    return None
