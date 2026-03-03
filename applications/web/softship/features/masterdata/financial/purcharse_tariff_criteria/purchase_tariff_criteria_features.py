from applications.web.softship.pages.masterdata.financial.purchase_tariff_criteria.PurchaseTariffCriteriaPage import PurchaseTariffCriteriaPage
from applications.web.softship.pages.masterdata.financial.purchase_tariff_criteria.PurchaseTariffCriteriaFormPage import PurchaseTariffCriteriaFormPage


class PurchaseTariffCriteria_features:

    purchase_tariff_criteria = PurchaseTariffCriteriaPage.get_instance()
    purchase_tariff_criteria_form = PurchaseTariffCriteriaFormPage.get_instance()

    def create(self):

        self.purchase_tariff_criteria.load_page()
        self.purchase_tariff_criteria.click_new()

        self.purchase_tariff_criteria_form.select_tariff_type("VOYAGE")
        self.purchase_tariff_criteria_form.select_rate_category_assignment("Ocean Additionals")
        self.purchase_tariff_criteria_form.search_rate_available_criteria("Cargo type")
        self.purchase_tariff_criteria_form.search_rate_available_criteria("Commodity")
        self.purchase_tariff_criteria_form.click_save_and_close()

    def delete(self):
        self.purchase_tariff_criteria.click_select()
        self.purchase_tariff_criteria.check_record(2)
        self.purchase_tariff_criteria.click_delete()

    def search(self):
        self.purchase_tariff_criteria.click_select_toggle()
        self.purchase_tariff_criteria.query_search("Tariff Type", "equal", "VOYAGE")
        self.purchase_tariff_criteria.print_row(2)



