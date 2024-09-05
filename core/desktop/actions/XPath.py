from appium.webdriver.common.appiumby import AppiumBy as By

# Example Code
# (By.XPATH, "//*[contains(@Name, 'Save As...')]")
# (By.XPATH, "//*[@AutomationId='4']")
# (By.NAME, "Save As...	Ctrl+Shift+S")


class XPath:

    @staticmethod
    def contains(value: str):
        locator = (By.XPATH, f"//*[contains(@Name, '{value}')]")
        return locator

    @staticmethod
    def automation_id(value: str):
        locator = (By.XPATH, f"//*[@AutomationId='{value}']")
        return locator

    @staticmethod
    def start_with(value: str):
        locator = (By.XPATH, f"//*[starts-with(text(), '{value}')]")
        return locator
