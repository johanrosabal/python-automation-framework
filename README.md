# python-automation-framework

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

## Desktop Local Server Configuration with 'Appium Python Client'
1. Requirements: Have Installed 'Node.js' and 'NPM' Package Management 
    ```commandline
    npm install -g appium
    npm install -g appium-doctor
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
   
# Child Page Object

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

| Prefix         | Description                                   | Examples                                                        |
|----------------|-----------------------------------------------|-----------------------------------------------------------------|
| **`_btn_`**    | For buttons                                   | `_btn_login`, `_btn_submit`, `_btn_cancel`                      |
| **`_input_`**  | For input fields                              | `_input_username`, `_input_password`, `_input_search`           |
| **`_link_`**   | For links                                     | `_link_forgot_password`, `_link_home`, `_link_terms_of_service` |
| **`_chk_`**    | For checkboxes                                | `_chk_remember_me`, `_chk_terms`, `_chk_subscribe`              |
| **`_rad_`**    | For radio buttons                             | `_rad_male`, `_rad_female`, `_rad_yes`, `_rad_no`               |
| **`_select_`** | For dropdowns                                 | `_select_country`, `_select_language`, `_select_category`       |
| **`_txt_`**    | For text areas                                | `_txt_description`, `_txt_comment`, `_txt_address`              |
| **`_msg_`**    | For messages (error messages, warnings, etc.) | `_msg_error`, `_msg_success`, `_msg_warning`                    |
| **`_img_`**    | For images                                    | `_img_logo`, `_img_banner`, `_img_profile`                      |
| **`_ico_`**    | For icons                                     | `_ico_settings`, `_ico_notification`, `_ico_search`             |
| **`_div_`**    | For divisions (containers, sections)          | `_div_header`, `_div_footer`, `_div_main_content`               |
| **`_modal_`**  | For modals or pop-ups                         | `_modal_login`, `_modal_alert`, `_modal_confirmation`           |
| **`_tab_`**    | For tabs                                      | `_tab_profile`, `_tab_settings`, `_tab_notifications`           |
| **`_form_`**   | For forms                                     | `_form_login`, `_form_registration`, `_form_feedback`           |
| **`_frame_`**  | For Frames                                    | `_frame_login`, `_frame_registration`, `_frame_feedback`        |
| **`_nav_`**    | For navigation elements                       | `_nav_menu`, `_nav_sidebar`, `_nav_footer`                      |

## Code Example

Here is an example of how you might use these prefixes in a page class for a test:

```python
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

        # Locator definitions
        self._input_username = (By.ID, "username")
        self._input_password = (By.ID, "password")
        self._btn_login = (By.ID, "login-button")
        self._link_forgot_password = (By.LINK_TEXT, "Forgot Password")
        self._msg_error = (By.CSS_SELECTOR, ".error-message")

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

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
           # Relative URL
           self.relative = "/web/index.php/auth/login"
           # Locator definitions
           self._locator_1 = (By.NAME, "...", "Input Locator_1")
           self._locator_2 = (By.NAME, "...", "Input Locator_2")
   
       @classmethod
       def get_instance(cls):
           if not hasattr(cls, '_instance'):
               cls._instance = ${NAME}(BaseApp.get_driver())
               cls.name = __class__.__name__
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

# UI Actions
# AlertPrompt Class

The `AlertPrompt` class is a utility for handling JavaScript alerts, prompts, and confirmation dialogs within a Selenium WebDriver testing environment. This class provides methods for interacting with both simple alerts and confirm dialogs, as well as for sending text input to prompts.

## Features

- **Simple Alert Handling:** Accept simple alerts with a single method call.
- **Confirm Dialog Handling:** Accept or cancel confirmation dialogs easily.
- **Prompt Handling:** Send text input to prompts and retrieve the displayed message.
- **Logging:** Integrated logging for better debugging and traceability.

## Class Structure

### 1. `AlertPrompt`

The `AlertPrompt` class is the main entry point for handling alerts. It requires a WebDriver instance during initialization and provides access to both simple and confirm alert types.

#### **Initialization:**
- **Parameters:** 
  - `driver`: The Selenium WebDriver instance controlling the browser.
- **Attributes:**
  - `_name`: The class name of the instance.
  - `_driver`: The WebDriver instance.
  - `_alert`: The active alert dialog retrieved from the WebDriver.
  - `_simple_alert`: An instance of the `Simple` class for handling simple alerts.
  - `_confirm_alert`: An instance of the `Confirm` class for handling confirm dialogs.

#### **Methods:**
- `simple_accept()`: Accept a simple alert.
- `confirm_accept()`: Accept a confirmation dialog.
- `confirm_cancel()`: Cancel a confirmation dialog.
- `send_keys(text)`: Send text input to a prompt.
- `get_text()`: Retrieve the text from the alert dialog.

### 2. `AlertPrompt.Simple`

This inner class handles simple alerts, which can only be accepted.

#### **Initialization:**
- **Parameters:**
  - `alert`: The active alert dialog retrieved from the WebDriver.

#### **Methods:**
- `accept()`: Accepts the alert. If no alert is present, logs an error.

### 3. `AlertPrompt.Confirm`

This inner class handles confirm dialogs, providing methods to either accept or cancel the dialog.

#### **Initialization:**
- **Parameters:**
  - `alert`: The active alert dialog retrieved from the WebDriver.

#### **Methods:**
- `accept()`: Accepts the confirmation dialog. Logs an error if no alert is present.
- `cancel()`: Cancels the confirmation dialog. Logs an error if no alert is present.

# TODOs

## **High Priority**
1. **Data Injection:**
   - Support data injection from multiple sources like JSON files, CSV, databases, or APIs to feed dynamic tests.
   - Subtasks: Implementation in Web, API, and Desktop tests.
2. **Integration with CI/CD Tools:**
   - Support test execution with Jenkins and other CI/CD environments.
   - Subtasks: Pipeline configuration, reporting integration.
3. **Parallelization and Scalability:**
   - Run multiple test cases in parallel across different browsers, virtual machines, or Docker containers.
   - Subtasks: Environment setup, local tests, cloud testing.
4. **Execution Profiles:**
   - Implement testing in different execution profiles: DEV, QA, UAT, PROD. (Test All Modules)
   - Subtasks: Profile configuration, validation in different environments.
5. **API:**
   - Research and Create a Basic Collection of Data Structure Validation (JSON XPaths for asserts validation)
   - Log Reporting Implementation provide all necessary information to Track Results
   - Research Best Practices Standards For API Testing Implementation 
6. **Reporting:**
   - Right now working with a basic reporting, but research on other possible reporting formats that we can customize.
   - Subtasks: Compare tools, implement new formats.
7. **Documentation**
   - Update README file with all the support documentation about framework functionality
   - Comment Code Properly in order to clarify features functionality
8. **Research on X-Ray Integration**

## **Medium Priority**

1. **Smart Screenshot Capture:**
   - Functionality to capture screenshots at critical points during execution and highlight key elements or UI errors.
   - Subtasks: Implementation in Web, Desktop.
2. **Desktop Object Model:**
   - Complete implementation (work on configuration, setup parameters).
3. **Desktop Applications:**
   - Research Image Recognition for graphical elements.
   - Subtasks: Evaluate tools, prototype integration.

## **Low Priority**
1. **Execution Recording:**
   - Implement the ability to record videos of test executions, especially useful for analyzing failures in UI and Desktop tests.

2. **API: Load Testings:**
    - Investigate support for load and performance testing with Python

3. **Research on AI-based Automation:**
    - Use machine learning to prioritize the execution of test cases based on risk or impact, optimizing execution time.
4. **Downloads/Uploads Folder Configuration**

## **Others Issues**
1. **Add All Possible API Authorization Endpoints:**
    - Research on this issue.

