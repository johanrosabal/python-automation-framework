def oracle(cls):
    """
    Configures parameters for 'oracle' tests.
    """
    cls.profile = "qa"
    cls.app_name = "oracle"
    cls.app_type = "web"
    cls.browser = "edge"
    return cls
