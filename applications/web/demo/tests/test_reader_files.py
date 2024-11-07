import pytest

from applications.web.demo.data.source_mapping import UserInformation
from core.data.sources.TABTXT_reader import TABTEXT_Reader
from core.data.sources.XML_reader import XMLReader
from core.data.sources.YAML_reader import YAMLReader
from core.data.sources.EXCEL_reader import EXCELReader
from core.data.sources.JSON_reader import JSONReader
from core.ui.common.BaseTest import BaseTest


@pytest.mark.web
class TestReaderFiles(BaseTest):

    def test_excel_reader(self):
        # 01. Load the Excel File using a relative Path
        path = "../data/sources/user_information_source.xlsx"
        # 02. Specifying the Sheet Name to map UserInformation values
        user_information = EXCELReader().set_file_path(path).read_list_structure(
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

    def test_csv_reader(self):
        # 01. Load the Excel File using a relative Path
        path = "../data/sources/user_information_source.csv"
        # 02. Specifying the Sheet Name to map UserInformation values
        user_information = EXCELReader().set_file_path(path).read_list_structure(
            object_class=UserInformation
        )

        # Assert that the number of UserInformation objects created is correct
        assert len(user_information) == 3

        # Assert that the properties of the first user are correct
        assert user_information[0].username == "user1"
        assert user_information[0].email == "user1@csv.com"
        assert user_information[0].type_of_user == "admin"
        assert user_information[0].enable is True

    def test_json_reader(self):
        # Load the JSON file using a relative path
        path = "../data/sources/user_information_source.json"
        # Read the file and map the data to UserInformation objects

        user_information = JSONReader().set_file_path(path).read_list_structure(
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

    def test_yaml_reader(self):
        # Load the YAML file using a relative path
        path = "../data/sources/user_information_source.yaml"
        # Read the file and map the data to UserInformation objects

        user_information = YAMLReader().set_file_path(path).read_list_structure(
            object_class=UserInformation,
            nested_key="tests.new_users"
        )

        # Assert that the number of UserInformation objects created is correct
        assert len(user_information) == 3

        # Assert that the properties of the first user are correct
        assert user_information[0].username == "user1"
        assert user_information[0].email == "user1@yaml.com"
        assert user_information[0].type_of_user == "admin"
        assert user_information[0].enable is True

    def test_tab_text_reader(self):
        # Load the TAB Text file using a relative path
        path = "../data/sources/user_information_source.txt"
        # Read the file and map the data to UserInformation objects

        user_information = TABTEXT_Reader().set_file_path(path).read_list_structure(
            object_class=UserInformation
        )

        # Assert that the number of UserInformation objects created is correct
        assert len(user_information) == 3

        # Assert that the properties of the first user are correct
        assert user_information[0].username == "user1"
        assert user_information[0].email == "user1@txt.com"
        assert user_information[0].type_of_user == "admin"
        assert user_information[0].enable is True

    def test_xml_reader(self):
        # Load the TAB Text file using a relative path
        path = "../data/sources/user_information_source.xml"
        # Read the file and map the data to UserInformation objects

        user_information = XMLReader().set_file_path(path).read_list_structure(
            object_class=UserInformation,
            section="new_users"
        )

        # Assert that the number of UserInformation objects created is correct
        assert len(user_information) == 3

        # Assert that the properties of the first user are correct
        assert user_information[0].username == "user1"
        assert user_information[0].email == "user1@xml.com"
        assert user_information[0].type_of_user == "admin"
        assert user_information[0].enable is True
