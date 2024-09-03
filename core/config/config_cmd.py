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


def get_browser():
    for arg in sys.argv:
        if arg.startswith("--browser="):
            return arg.split("=")[1]
    return None
