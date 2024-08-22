from applications.web.demo.data.excel_mapping import UserInformation
from core.data.sources.excel_reader import ExcelReader
from core.ui.common.BaseTest import BaseTest
from core.utils.helpers import get_file_path


class TestExcelReader(BaseTest):

    def test_read_file(self):

        reader = ExcelReader("../data/sources/user_information_source.xlsx")

        # Read the file, specifying the sheet name
        user_information = reader.read_file(sheet_name="UserData").map_to_objects(UserInformation)

        # Assert that the DataFrame is not None and contains data
        assert reader.data_frame is not None

        # Assert that the number of UserInformation objects created is correct
        assert len(user_information) == 3

        # Assert that the properties of the first user are correct
        assert user_information[0].username == "jrosabal"
        assert user_information[0].email == "jrosabal@test.com"
        assert user_information[0].type_of_user == "admin"
        assert user_information[0].enable is True
