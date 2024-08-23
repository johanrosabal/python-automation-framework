from applications.web.demo.data.source_mapping import UserInformation
from core.data.sources.excel_reader import ExcelReader
from core.data.sources.JSON_reader import JSONReader
from core.ui.common.BaseTest import BaseTest
from core.utils.helpers import get_file_path


class TestExcelReader(BaseTest):

    def test_excel_reader(self):
        # 01. Load the Excel File using a relative Path
        path = "../data/sources/user_information_source.xlsx"
        # 02. Specifying the Sheet Name to map UserInformation values
        user_information = ExcelReader().set_file_path(path).read_file(
            object_class=UserInformation,
            sheet_name="UserData"
        )

        # Assert that the number of UserInformation objects created is correct
        assert len(user_information) == 3

        # Assert that the properties of the first user are correct
        assert user_information[0].username == "user1"
        assert user_information[0].email == "user1@excel.com"
        assert user_information[0].type_of_user == "admin"
        assert user_information[0].enable is True

    def test_json_reader(self):
        # Load the JSON file using a relative path
        path = "../data/sources/user_information_source.json"
        # Read the file and map the data to UserInformation objects

        user_information = JSONReader().set_file_path(path).read_file(
            object_class=UserInformation,
            nested_key="tests.new_users"
        )

        # Assert that the number of UserInformation objects created is correct
        assert len(user_information) == 3

        # Assert that the properties of the first user are correct
        assert user_information[0].username == "user1"
        assert user_information[0].email == "user1@json.com"
        assert user_information[0].type_of_user == "admin"
        assert user_information[0].enable is True
