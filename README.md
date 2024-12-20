# python-automation-framework

## Update Zcaler Certification
1. Go to "resources/cert/ZscalerRootCertificate-2048-SHA256.pem" copy this file and pasted in "C:\drive"
2. Run the following command on "PowerShell"
   ```commandline
   mv $env:C:\drive\ZscalerRootCertificate-2048-SHA256.pem $env:APPDATA
   pip config set global.cert $env:APPDATA\ZscalerRootCertificate-2048-SHA256.pem 
   ```
3. Open Zscaler > More > About > App Policy: Crowley Tunner 2.0 >> Update Policy
4. Try to download a Python Package Library: If fail try one more time to download the required library

## Python Configuration
1. Search Inbox on task bar type "Edit environment variables for your account"
2. On User variables for {Current User}, on PATH variable click on New
   Add: 
      - C:\Users\{Current User}\AppData\Local\Programs\Python\Python312\Scripts
      - C:\Users\{Current User}\AppData\Local\Programs\Python\Python312
3. Check Python Version on Terminal
   ```commandline
   python --version
   pip --version
    ```

## Desktop Local Server Configuration with 'Appium Python Client' and Allure Command Line
1. Requirements: Have Installed 'Node.js' and 'NPM' Package Management 
    ```commandline
    npm install -g appium
    npm install -g appium-doctor
    npm install -g allure-commandline
    ```
2. Also is required to install Appium Drivers

   ```commandline
   appium driver install windows
   appium driver install gecko
   appium driver install chromium
   ```
3. Check Appium Drivers Installed 
   ```commandline
   appium driver list
   ```
4. To execute Desktop Application Automation, user should be start up the Appium Server Before Execute any Test
   ```commandline
   appium --allow-cors
   ```
   
## Packages 
1. Run the 'install.bat' file on project Root
2. Check Packages Installed with following command on terminal
   ```commandline
    pip list
    ```

## Terminal Pycharm
1. In order to enable Terminal on Windows Pycharm user enable the following commands
   ```commandline
   Get-ExecutionPolicy -List
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
   ```
## Installing Individual Packages
1. In case that we need to install a individual package from the "requirements.txt" follow the next terminal command
```commandline
pip install <package> --trusted-host pypi.org --trusted-host files.pythonhosted.org
```
## Arguments to Provide on Execution
### WEB Applications
1. For Web Executions: Provide Profile, Application Name, Application Type, Browser and Allure Generate results
   ```commandline
       --profile=qa --app-name=softship --app-type=web --browser=chrome --alluredir=reports/allure-results
   ```
2. Initialize Allure Server Report Example:
   ```commandline
   allure serve C:\Automation\QA%20Automation\applications\web\softship\tests\reports\allure-results
   ```
### API Applications
1. For API Executions: Provide Profile, Application Name, Application Type and Allure Generate
   ```commandline
        --profile=qa --app-name=salesforce --app-type=api --alluredir=reports/allure-results
   ```
### Run Terminal Execution
1. Example:
```commandline
pytest --profile=qa --app-name=softship --app-type=web --browser=edge --alluredir=reports/allure-results C:\QA%20Automation\applications\web\softship\tests\test_master_data_customer_suppliers_address.py::TestMasterDataCustomerSuppliersAddress
```

# Automation Architecture
1. Set the commands arguments with the test case specification
2. The "BaseTest" class reads the arguments and set the "Driver" session on Top super class "BASE APP", this class share this variable under "BasePage" Child Class.
3. All the "Action" Classes use the "Driver" session to Locate every Web Element before apply any action.
4. All the "Child Objects" under "BasePage" will have enabled all these actions.

<img src="resources\images\AUTOMATION-CORE.PNG" alt="AUTOMATION-CORE" width="600"/>

# Child Page Object
<img src="resources\images\CHILD-OBJECT-PAGE.PNG" alt="AUTOMATION-CORE" width="900"/>

## Class Name Format
1. File class name should be in CamelCase (PascalCase) every word should start with uppercase letter.
   Not use underscores or spaces.
2. Examples:
   - LoginPage
   - SignUpPage
   - WelcomePage
   
## Methods Name Format
1. Methods name should use **snake_case** format (lowercase letters with the words separated by underscores).
2. Avoid method names that are just a verb; Try to be more descriptive if necessary.
3. Examples:
   - load_page
   - set_username
   - set_password
## Variables Name Format
1. Uses the snake_case format (lowercase letters with words separated by underscores).
2. Example:
   - user_list
   - count_item
   - file_name
## Private Variables and Methods
1. Uses a single underscore at the beginning of the name to indicate that a variable or method is "private."
2. Example:
 - _private_var
 - _private_method
 - _helper_method
 - _driver

## Locator
1. Locator are tuple objects, can have 2 values or 3 values in case the is necessary to specify the web element name reference. 
   Following the next example the **__input_username** and **__input_password** has only the 'By' and 'value' but **button_login** contains an additional value to specify the reference name **Login Button** this value will display in the console log.

2. Example Code:
   ```console
       _input_user_name = (By.NAME, "username")
       _input_password = (By.NAME, "password")
       _button_login = (By.XPATH, "//button[contains(@class,'login-button')]", "Login Button")
   ``` 
3. Console Log Example:
      ```console
      BasePage - INFO: Event: [LoginPage] | Web Element By: [name] | Locator value: [username]
      BasePage - INFO: Event: [LoginPage] | Web Element By: [name] | Locator value: [password]
      BasePage - INFO: Event: [LoginPage] | Web Element By: [xpath] | Locator value: [//button[contains(@class,'login-button')]] | Login Button
      ```
## Locator Prefix Conventions
# Locator Prefix Conventions

In test automation and UI development, using standard prefixes for locators helps keep the code organized and maintainable.

## Common Prefixes

| Prefix               | Description                                   | Examples                                                        |
|----------------------|-----------------------------------------------|-----------------------------------------------------------------|
| **`_btn_`**          | For buttons                                   | `_btn_login`, `_btn_submit`, `_btn_cancel`                      |
| **`_input_`**        | For input fields                              | `_input_username`, `_input_password`, `_input_search`           |
| **`_link_`**         | For links                                     | `_link_forgot_password`, `_link_home`, `_link_terms_of_service` |
| **`_chk_`**          | For checkboxes                                | `_chk_remember_me`, `_chk_terms`, `_chk_subscribe`              |
| **`_rad_`**          | For radio buttons                             | `_rad_male`, `_rad_female`, `_rad_yes`, `_rad_no`               |
| **`_select_`**       | For dropdowns                                 | `_select_country`, `_select_language`, `_select_category`       |
| **`_autocomplete_`** | For auto complete                             | `_autocomplete_country`, `_autocomplete_language`               |
| **`_txt_`**          | For text areas                                | `_txt_description`, `_txt_comment`, `_txt_address`              |
| **`_msg_`**          | For messages (error messages, warnings, etc.) | `_msg_error`, `_msg_success`, `_msg_warning`                    |
| **`_img_`**          | For images                                    | `_img_logo`, `_img_banner`, `_img_profile`                      |
| **`_ico_`**          | For icons                                     | `_ico_settings`, `_ico_notification`, `_ico_search`             |
| **`_div_`**          | For divisions (containers, sections)          | `_div_header`, `_div_footer`, `_div_main_content`               |
| **`_modal_`**        | For modals or pop-ups                         | `_modal_login`, `_modal_alert`, `_modal_confirmation`           |
| **`_tab_`**          | For tabs                                      | `_tab_profile`, `_tab_settings`, `_tab_notifications`           |
| **`_form_`**         | For forms                                     | `_form_login`, `_form_registration`, `_form_feedback`           |
| **`_frame_`**        | For Frames                                    | `_frame_login`, `_frame_registration`, `_frame_feedback`        |
| **`_nav_`**          | For navigation elements                       | `_nav_menu`, `_nav_sidebar`, `_nav_footer`                      |

## Code Example

Here is an example of how you might use these prefixes in a page class for a test:

```python
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/"
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self._input_username = (By.ID, "username")
        self._input_password = (By.ID, "password")
        self._btn_login = (By.ID, "login-button")
        self._link_forgot_password = (By.LINK_TEXT, "Forgot Password")
        self._msg_error = (By.CSS_SELECTOR, ".error-message")

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/"
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self._nav_menu = (By.ID, "main-menu")
        self._img_logo = (By.ID, "logo")
        self._tab_profile = (By.ID, "profile-tab")
        self._btn_logout = (By.ID, "logout-button")
 ```

### Child Page Object Template on Pycharm

To create a custom template in PyCharm that will be used when creating a new Python class, follow these steps:

1. **Open Template Settings:**
 - Go to File > Settings (or PyCharm > Preferences on macOS).
 - In the left panel, navigate to Editor > File and Code Templates.

2. **Create a New Python Template:**
 - Inside File and Code Templates, select Python Script.
 - Click the + button to add a new template.

3. **Configure the Template:**
 - Give your template a name, like Custom Python Class.
 - Ensure that ${NAME} is a variable that PyCharm will automatically replace with the file or class name when creating a new file.
 - In the template editor, paste your code:

   ```python
   from selenium.webdriver.common.by import By
   from core.asserts.AssertCollector import AssertCollector
   from core.config.logger_config import setup_logger
   from core.ui.common.BaseApp import BaseApp
   from core.ui.common.BasePage import BasePage
   
   logger = setup_logger('${NAME}')
   
   class ${NAME}(BasePage):
   
       def __init__(self, driver):
           """
           Initialize the ${NAME} instance.
           """
           super().__init__(driver)
           # Driver
           self.driver = driver
           # Name
           self._name = self.__class__.__name__
           # Relative URL
           self.relative = "/web/index.php/auth/login"
           # Locator definitions
           self._locator_1 = (By.NAME, "...", "Input Locator_1")
           self._locator_2 = (By.NAME, "...", "Input Locator_2")
   
       @classmethod
       def get_instance(cls):
           if not hasattr(cls, '_instance'):
               cls._instance = ${NAME}(BaseApp.get_driver())
               cls._name = __class__.__name__
           return cls._instance
   
       def load_page(self):
           base_url = BaseApp.get_base_url()
           logger.info("LOAD PAGE: " + base_url + self.relative)
           self.navigation().go(base_url, self.relative)
           return self
   
       def some_method(self):
           pass
   ```
4. **Save the Template:**
 - Click OK or Apply to save the new template.
5. **Use the Template:**
 - Now, when you create a new file, select New > Python File, and then choose Custom Python Class (or whatever name you gave your template).

# Test Case Example

1. Create an instance of the page object with the static method ".get_instance"
2. Withing the test load the page with ".load_page()" method.

```python
from core.config.logger_config import setup_logger
from applications.web.demo.pages.LoginPage import LoginPage
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test

logger = setup_logger('TestLogin')


class TestLogin(BaseTest):

    LoginPage = LoginPage.get_instance()

    @test(test_case_id="HRM-0001", test_description="Verify Login Page headline")
    def test_login_headline(self):
        # 01. Interact with page elements
        self.LoginPage.load_page()
        # 02. Validations
        self.LoginPage.verify_headline("Login")
```

# Actions
## Element
WebElement constructor
### Explanation of Each Method
1. **set_locator:** Waits for the specified element to appear and logs the event.
2. **is_visible:** Returns True if the element is displayed on the page.
3. **is_enabled:** Returns True if the element is enabled and interactive.
4. **is_selected:** Returns True if the element is selected.
5. **get_tag_name:** Retrieves the tag name of the element.
6. **get_position:** Returns the position and size of the element.
7. **get_css_property:** Gets the value of a specified CSS property.
8. **get_text:** Returns the text content of the element.
9. **get_attribute:** Returns the value of a specified attribute.
10. **wait_for_element:** Waits for a single element to be visible within a timeout.
11. **wait_for_elements:** Waits for all matching elements to be visible within a timeout.
12. **log_console:** Formats a log message for better traceability of actions and elements.

## Click
Click actions over elements.
![alt text](/resources/images/CLICK.png)
### Code
One Line
```python
    self.click().set_locator(locator="{locator}", page="{page_name}").single_click()
```
Multi-Line using "\" on each line.
```python
    self.click() \
        .set_locator(locator="{locator}", page="{page_name}") \
        .single_click()
```
### Explanation of Each Method
1. **set_locator:** Sets the locator for the target element, waits for it, and logs the process. Returns self to allow method chaining.
2. **pause:** Pauses the execution for a given number of seconds.
3. **single_click:** Clicks the element once, logging whether it was successful.
4. **double_click:** Double-clicks the element if present, logging the action.
5. **click_and_hold:** Clicks and holds on the element, logging if it’s successful.
6. **context_click:** Performs a right-click on the element, logging success or failure.
7. **drag_and_drop:** Drags one element onto another if both are provided.
8. **mouse_over:** Moves the mouse over the element to simulate a hover effect.
9. **pause:** Pauses the execution for a given number of seconds.
10. **screenshot:** Captures a screenshot of the element and attaches it to the Allure report.

## SendKeys
Typing text and key events.
![alt text](/resources/images/SEND_KEYS.png)
### Code
One Line
```python
    self.send_keys().set_locator(locator="{locator}", page="{page_name}").set_text("")
```
Multi-Line using "\" on each line.
```python
    self.send_keys() \
        .set_locator(locator="{locator}", page="{page_name}") \
        .set_text("")
```
### Explanation of Each Method
1. **set_locator:** Sets the locator for the target element, waits for it, and logs the process. Returns self to allow method chaining.
2. **set_text:** Sets and sends the provided text to the element.
3. **set_text_by_character:** Sends text to the element character by character.
4. **get_text:** Retrieves text from the element's value attribute.
5. **clear:** Clears the text from the element.
6. **Keyboard actions:** press_return, press_enter, press_backspace, press_tab, press_escape
7. **pause:** Pauses the execution for a given number of seconds.
8. **screenshot:** Captures a screenshot of the element and attaches it to the Allure report.

## CheckBox
Handle checkboxes form elements.
![alt text](/resources/images/CHECKBOX.png)
### Code
One Line
```python
    self.checkbox().set_locator(locator="{locator}", page="{page_name}").set_value("")
```
Multi-Line using "\" on each line.
```python
    self.checkbox() \
        .set_locator(locator="{locator}", page="{page_name}") \
        .set_text("")
```
### Explanation of Each Method
1. **set_locator:** Sets the locator for the target element, waits for it, and logs the process. Returns self to allow method chaining.
2. **is_displayed:** Checks if the checkbox element is displayed on the page.
3. **is_selected:** Checks if the checkbox element is currently selected.
4. **set_value:** Sets the checkbox value based on the provided boolean.
5. **pause:** Pauses the execution for a given number of seconds.
6. **screenshot:** Captures a screenshot of the element and attaches it to the Allure report.

## Dropdown
Manage dropdown options from a standard web element.
![alt text](/resources/images/DROPDOWN.png)
### Code
One Line
```python
    self.dropdown().set_locator(locator="{locator}", page="{page_name}").by_text("")
```
Multi-Line using "\" on each line.
```python
    self.dropdown() \
        .set_locator(locator="{locator}", page="{page_name}") \
        .by_text("")
```
### Explanation of Each Method
1. **set_locator:** Sets the locator for the target element, waits for it, and logs the process. Returns self to allow method chaining.
2. **by_value:** Selects an option by its 'value' attribute.
3. **by_index:** Selects an option by its index.
4. **by_text:** Selects an option by its visible text.
5. **by_text_contains:** Selects an option that contains specific text.
6. **deselect_all:** Deselects all selected options if the dropdown supports multiple selections.
7. **pause:** Pauses the execution for a given number of seconds.
8. **screenshot:** Captures a screenshot of the element and attaches it to the Allure report.


# TODOs

## **High Priority**
1. **Integration with CI/CD Tools:**
   - Support test execution with Jenkins and other CI/CD environments.
   - Subtasks: Pipeline configuration, reporting integration.
2**Parallelization and Scalability:**
   - Run multiple test cases in parallel across different browsers, virtual machines, or Docker containers.
   - Subtasks: Environment setup, local tests, cloud testing.
3**Reporting:**
   - Right now working with a basic reporting, but research on other possible reporting formats that we can customize.
   - Subtasks: Compare tools, implement new formats.
4**Documentation**
   - Update README file with all the support documentation about framework functionality
   - Comment Code Properly in order to clarify features functionality
5**Research on X-Ray Integration**

## **Low Priority**
1. **Execution Recording:**
   - Implement the ability to record videos of test executions, especially useful for analyzing failures in UI and Desktop tests.

2. **API: Load Testings:**
    - Investigate support for load and performance testing with Python
3. **Downloads/Uploads Folder Configuration**

## **Others Issues**
1. **Add All Possible API Authorization Endpoints:**
    - Research on this issue.

