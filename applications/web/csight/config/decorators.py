def csight(cls):
    """
    Configures parameters for 'C-Sight' tests.
    """
    cls.profile = "uat"
    cls.app_name = "csight"
    cls.app_type = "web"
    cls.browser = "edge"
    cls.headless = False
    return cls
