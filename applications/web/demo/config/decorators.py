def demo(cls):
    """
    Configures parameters for 'demo' tests.
    """
    cls.profile = "qa"
    cls.app_name = "demo"
    cls.app_type = "web"
    cls.browser = "chrome"
    return cls
