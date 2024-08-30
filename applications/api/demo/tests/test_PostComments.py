from core.api.common.BaseTest import BaseTest
from applications.api.demo.endpoints.Posts import Posts
from applications.api.demo.data.sources_mapping import Payload

from core.config.logger_config import setup_logger
from core.data.sources.JSON_reader import JSONReader
from core.utils.decorator import test
from core.utils.table_formatter import TableFormatter

logger = setup_logger('TestPost')


# @pytest.mark.skip(reason="no way of currently testing this")

class TestPostComments(BaseTest):

    def setup_class(self):
        self.Posts = Posts.get_instance()

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0001", test_description="Create a Post using JSON Data")
    def test_create_posts(self):

        path = "../data/sources/payload.json"
        data = JSONReader().set_file_path(path).read_file(Payload, "tests.payload")
        payload = data[0].to_json()

        # Sending Post Request
        response = self.Posts.create_posts(payload).get_response()

        # Get Json
        response_json = response.json()
        errors = []

        # Validation
        if response_json.get('id') != 101:
            errors.append(f"Expected 'id' to be 101, but got {response_json.get('id')}")

        if response_json.get('title') != "foo":
            errors.append(f"Expected 'title' to be 'foo', but got {response_json.get('title')}")

        if response_json.get('body') != "bar":
            errors.append(f"Expected 'body' to be 'bar', but got {response_json.get('body')}")

        if response_json.get('userId') != 1:
            errors.append(f"Expected 'userId' to be 1, but got {response_json.get('userId')}")

        self.add_report(test_name=self.test_create_posts.test_description, status_code=201, response=response,
                        errors=errors)

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0002", test_description="Test Post Get All")
    def test_post_get_all(self):
        # Sending Get Request
        request = self.Posts.get_all_post()
        response = request.get_response()

        # Standard Validations: Status Code and Content Type
        self.add_report(test_name=self.test_post_get_all.test_description, status_code=200, response=response)
        # self.validations(response).verify_status_code(200)

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0003", test_description="Test Get By ID")
    def test_post_by_id(self):
        # Sending Get Request
        response = self.Posts.get_post_by_id(post_id=1).get_response()

        # Get Json
        response_json = response.json()
        errors = []

        # Validation
        if response_json.get('id') != 1:
            errors.append(f"Expected 'id' to be 1, but got {response_json.get('id')}")

        if response_json.get('title') != "sunt aut facere repellat provident occaecati excepturi optio reprehenderit":
            errors.append(
                f"Expected 'title' to be 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit', but got {response_json.get('title')}")

        if response_json.get('userId') != 1:
            errors.append(f"Expected 'userId' to be 1, but got {response_json.get('userId')}")

        self.add_report(test_name=self.test_post_by_id.test_description, status_code=200, response=response,
                        errors=errors)

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0004", test_description="Test Get Comments By ID")
    def test_comments_by_id(self):
        # URL Example: https://jsonplaceholder.typicode.com/posts/1/comments
        # Sending Get Request with ID
        response = self.Posts.get_comments_by_id(1).get_response()

        # Get Json
        response_json = response.json()[0]
        errors = []

        # Validation
        if response_json.get('postId') != 2:
            errors.append(f"Expected 'postId' to be 1, but got {response_json.get('postId')}")

        if response_json.get('name') != "id labore ex et quam laborum":
            errors.append(
                f"Expected 'name' to be 'id labore ex et quam laborum', but got {response_json.get('name')}")

        if response_json.get('email') != "Eliseo@gardner.biz":
            errors.append(f"Expected 'email' to be 'Eliseo@gardner.biz', but got {response_json.get('email')}")

        self.add_report(test_name=self.test_comments_by_id.test_description, status_code=200, response=response,
                        errors=errors)

    # # @pytest.mark.skip(reason="Skip")
    # @test(test_case_id="API-0005", test_description="Test Get Comments By ID with Params")
    # def test_comments_by_id_with_params(self):
    #     # URL Example: https://jsonplaceholder.typicode.com/posts?postId=1
    #     # Sending Get Request with Param ID
    #     request = self.Posts.get_comments_by_id_params(post_id=1)
    #     response = request.get_response()
    #
    #     # Standard Validations: Status Code and Content Type
    #     self.validations(response) \
    #         .verify_status_success_code(200, print_response_text=False) \
    #         .verify_content_type(self.content_type)
    #
    #     # If PASS: Print the JSON List into a Table on Console using TableFormatter Class
    #     data = request.get_response_json()
    #     TableFormatter().prepare_list(data).to_grid()
    #
    # # @pytest.mark.skip(reason="Skip")
    # @test(test_case_id="API-0006", test_description="Test update a Post")
    # def test_update_posts(self):
    #     payload = {
    #         "title": "foo2",
    #         "body": "bar2",
    #     }
    #
    #     # Sending Put Request with Param ID
    #     request = self.Posts.update_post(post_id=1, json=payload)
    #     response = request.get_response()
    #
    #     # Standard Validations: Status Code and Content Type
    #     self.validations(response) \
    #         .verify_status_success_code(200, print_response_text=False) \
    #         .verify_content_type(self.content_type)
    #
    #     # If PASS: Print the JSON Item into a Table on Console using TableFormatter Class
    #     data = request.get_response_json()
    #     TableFormatter().prepare_single_item(data).to_grid()
    #
    # # @pytest.mark.skip(reason="Skip")
    # @test(test_case_id="API-0007", test_description="Test update a Post")
    # def test_patching_posts(self):
    #     payload = {
    #         "title": "foo3",
    #     }
    #
    #     # Sending Patching Request with Param ID
    #     request = self.Posts.patching_post(post_id=1, json=payload)
    #     response = request.get_response()
    #
    #     # Standard Validations: Status Code and Content Type
    #     self.validations(response) \
    #         .verify_status_success_code(200) \
    #         .verify_content_type(self.content_type)
    #
    #     # If PASS: Print the JSON Item into a Table on Console using TableFormatter Class
    #     data = request.get_response_json()
    #     TableFormatter().prepare_single_item(data).to_grid()
    #
    # # @pytest.mark.skip(reason="Skip")
    # @test(test_case_id="API-0008", test_description="Test delete a Post")
    # def test_delete_posts(self):
    #     # Sending Delete Request with ID
    #     request = self.Posts.delete_post(post_id=1)
    #     response = request.get_response()
    #
    #     # Standard Validations: Status Code and Content Type
    #     self.validations(response) \
    #         .verify_status_success_code(200, print_response_text=True) \
    #         .verify_content_type(self.content_type)
