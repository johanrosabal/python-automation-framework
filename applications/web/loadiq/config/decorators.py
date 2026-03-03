def loadiq(cls):
    """
    Configures parameters for 'Load IQ' tests.
    """
    cls.profile = "qa"
    cls.app_name = "loadiq"
    cls.app_type = "web"
    cls.browser = "edge"
    cls.app_api= "apí"
    cls.app_endpoint = "devtmsexchange"
    return cls
