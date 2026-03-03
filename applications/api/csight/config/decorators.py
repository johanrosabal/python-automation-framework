def csight(cls):
    """
    Configures parameters for 'C-Sight' tests.
    """
    cls.profile = "uat"
    cls.app_name = "csight"
    cls.app_type = "api"
    cls.browser = "edge"
    return cls
