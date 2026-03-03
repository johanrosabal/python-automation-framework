def softship(cls):
    """
    Configures parameters for 'softship' tests.
    """
    cls.profile = "qa"
    cls.app_name = "softship"
    cls.app_type = "web"
    cls.browser = "edge"
    return cls
