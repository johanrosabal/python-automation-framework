def salesforce(cls):
    """
    Configures parameters for 'salesforce' tests.
    """
    cls.profile = "qa"
    cls.app_name = "salesforce"
    cls.app_type = "api"
    return cls
