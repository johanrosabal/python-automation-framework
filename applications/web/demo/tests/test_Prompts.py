import pytest

from applications.web.demo.config.decorators import demo
from core.config.logger_config import setup_logger
from applications.web.demo.pages.AlertPage import AlertPage
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test

logger = setup_logger('TestLogin')


@pytest.mark.web
@demo
class TestPrompts(BaseTest):
    alertPage = AlertPage.get_instance()

    @test(test_case_id="00001", test_description="Verify Accept Alert")
    def test_accept_simple_prompt(self):
        (self.alertPage
         .load_alert_page()
         .click_try_it()
         .verify_alert_text("I am an alert box!")
         .click_alert_accept()
         )

    @test(test_case_id="00002", test_description="Verify Accept Prompt")
    def test_accept_prompt_text(self):
        (self.alertPage
         .load_prompt_page()
         .click_try_it()
         .verify_alert_text("Please enter your name:")
         .enter_prompt_text("Joe Doe")
         .click_prompt_accept()
         .verify_demo_text("Hello Joe Doe! How are you today?")
         )

    @test(test_case_id="00003", test_description="Verify Cancel Prompt")
    def test_accept_prompt_text(self):
        (self.alertPage
         .load_prompt_page()
         .click_try_it()
         .verify_alert_text("Please enter your name:")
         .enter_prompt_text("Joe Doe")
         .click_prompt_cancel()
         .verify_demo_text("User cancelled the prompt.")
         )
