import allure

from applications.web.softship.common.SoftshipBaseTest import SoftshipBaseTest
from applications.web.softship.fixtures.fixtures import *
from applications.web.softship.components.menus.SoftshipMenu import SoftshipMenu
from applications.web.softship.config.decorators import softship
from applications.web.softship.data.address_source_mapping import CustomerAppliersAddressDto
from applications.web.softship.pages.masterdata.basic.customer_suppliers.address.AddressFormPage import AddressFormPage
from applications.web.softship.pages.masterdata.basic.customer_suppliers.address.AddressPage import AddressPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import user
from core.utils.decorator import test

logger = setup_logger('TestMasterDataCustomerSuppliersAddress')


@pytest.mark.web
@softship
class TestMasterDataCustomerSuppliersAddress(SoftshipBaseTest):
    # Init App
    menu = SoftshipMenu.get_instance()
    address_new = AddressPage.get_instance()
    address_form = AddressFormPage.get_instance()

    @test(test_case_id="MDS-0001", test_description="Customer Suppliers Basic New Address.")
    def test_basic_customer_suppliers_address(self, softship_login_master_data):
        # Load Randon Data From List
        address = CustomerAppliersAddressDto.get_random_address()
        # 01. Click on "New Address" Link
        self.menu.app_master_data.menu_basic.link_address_new()
        # 02. Click on "New" Button on New Address page
        self.address_new.click_new(pause=5)
        # 03. Verify Form Page Loads
        self.address_form.is_address_form_displayed()
        # 04. Fill out Address Information Data and Confirmation
        self.address_form.fill_out_address_form(address)
        self.address_form.click_save()
        self.address_form.verify_saved_data()
        # 05. Close Form Page
        self.address_form.click_close()
        self.address_form.click_confirm_yes()
        # 06. Shows SearchBox on Address Page
        self.address_new.click_select_toggle(show=True)
        # 07. Enter Search Criteria
        self.address_new.query_search(
            field_name="Address Code",
            field_operator="starts with",
            field_value=address.address_code
        )
        # 08. Read Row Data
        self.address_new.print_row(2)
        self.pause(3)
        # 05. Logout User from application
        self.menu.logout()

