def loadiq_loadboard(cls):
    """
    Configures parameters for 'LoadIQ Loadboard' tests.
    """
    cls.profile = "qa"
    cls.app_name = "loadiq"
    cls.app_type = "api"
    cls.app_endpoint = "loadboard"
    return cls


def loadiq_trackntrace(cls):
    """
    Configures parameters for 'LoadIQ Track N Trace' tests.
    """
    cls.profile = "qa"
    cls.app_name = "loadiq"
    cls.app_type = "api"
    cls.app_endpoint = "trackntrace"
    return cls


def loadiq_user_management(cls):
    """
    Configures parameters for 'LoadIQ User Management' tests.
    """
    cls.profile = "qa"
    cls.app_name = "loadiq"
    cls.app_type = "api"
    cls.app_endpoint = "user_management"
    return cls


def loadiq_location(cls):
    """
    Configures parameters for 'LoadIQ User Location' tests.
    """
    cls.profile = "qa"
    cls.app_name = "loadiq"
    cls.app_type = "api"
    cls.app_endpoint = "location"
    return cls


def loadiq_tmsexchange(cls):
    """
    Configures parameters for 'LoadIQ User Location' tests.
    """
    cls.profile = "qa"
    cls.app_name = "loadiq"
    cls.app_type = "api"
    cls.app_endpoint = "tmsexchange"
    return cls

def  loadiq_devtmsexchange(cls):
    """
    Configures parameters for 'LoadIQ User Location' tests.
    """
    cls.profile = "dev"
    cls.app_name = "loadiq"
    cls.app_type = "api"
    cls.app_endpoint = "tmsexchange"
    return cls
