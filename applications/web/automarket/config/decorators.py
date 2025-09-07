def automarket(cls):
    """
    Configures parameters for 'demo' tests.
    """
    cls.profile = "qa"
    cls.app_name = "automarket"
    cls.app_type = "web"
    cls.browser = "chrome"
    return cls
