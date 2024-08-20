from core.ui.common.BasePage import BasePage


class MasterDataPage(BasePage):

    def __init__(self, driver=None):
        super().__init__()
        if driver:
            self.driver = driver
