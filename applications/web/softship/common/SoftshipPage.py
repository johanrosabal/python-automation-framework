from applications.web.softship.actions.SearchAutocomplete import SearchAutocomplete
from applications.web.softship.actions.TableWithControls import TableWithControls
from applications.web.softship.components.search.QuerySearchAdvanceComponent import QuerySearchAdvanceComponent
from core.ui.common.BasePage import BasePage
from applications.web.softship.actions.DropdownAutocomplete import DropdownAutocomplete


class SoftshipPage(BasePage):

    def dropdown_autocomplete(self):
        return DropdownAutocomplete(self.get_driver())

    def search_autocomplete(self):
        return SearchAutocomplete(self.get_driver())

    def table_with_controls(self):
        return TableWithControls(self.get_driver())

    def search_advance_filter(self):
        return QuerySearchAdvanceComponent(self.get_driver())
