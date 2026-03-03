def mock(cls):
    """
    Configures parameters for 'demo' tests.
    """
    cls.profile = "qa"
    cls.app_name = "mock"
    cls.app_type = "api"
    return cls
