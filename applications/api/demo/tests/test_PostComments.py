import pytest

from applications.api.demo.endpoints.Posts import Posts
from core.api.common.BaseTest import BaseTest

from core.config.logger_config import setup_logger
from core.utils.decorator import test
from core.utils.table_formatter import TableFormatter

logger = setup_logger('TestPost')


# @pytest.mark.skip(reason="no way of currently testing this")

class TestPostComments(BaseTest):

    def setup_class(self):
        self.Posts = Posts.get_instance()
        self.content_type = "application/json; charset=utf-8"

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0001", test_description="Test create a Post using JSON Data")
    def test_create_posts(self):
        # Payload Information
        payload = {
            "id": 101,
            "title": "foo",
            "body": "bar",
            "userId": 1
        }

        # Sending Post Request with Json Object
        request = self.Posts.create_posts(json=payload)
        response = request.get_info().response

        # Standard Validations: Status Code and Content Type
        error_message = None
        # Standard Validations: Status Code and Content Type
        try:
            self.validations(response) \
                .verify_status_success_code(201, print_response_text=False) \
                .verify_content_type(self.content_type)
        except Exception as e:
            error_message = str(e)

        # Add to report
        self.add_report(
            test_name="Test create a Post using JSON Data",
            url=request.get_info().request_url,
            method=request.get_info().request_method,
            response=request.get_info().response,
            error_message=error_message)

        # If PASS: Print the JSON Item into a Table on Console using TableFormatter Class
        data = request.get_response_json()
        TableFormatter().prepare_single_item(data).to_grid()

    # # @pytest.mark.skip(reason="Skip")
    # @test(test_case_id="API-0002", test_description="Test Post Get All")
    # def test_post_get_all(self):
    #     # Sending Get Request
    #     request = self.Posts.get_all_post()
    #     response = request.get_response()
    #
    #     # Standard Validations: Status Code and Content Type
    #     self.validations(response) \
    #         .verify_status_success_code(200) \
    #         .verify_content_type(self.content_type)
    #
    #     # If PASS: Print the JSON List into a Table on Console using TableFormatter Class
    #     data = request.get_response_json()
    #     TableFormatter().prepare_list(data).to_grid()
    #
    # # @pytest.mark.skip(reason="Skip")
    # @test(test_case_id="API-0003", test_description="Test Get By ID")
    # def test_post_by_id(self):
    #     # Sending Get Request
    #     request = self.Posts.get_post_by_id(post_id=1)
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
    # @test(test_case_id="API-0004", test_description="Test Get Comments By ID")
    # def test_comments_by_id(self):
    #     # URL Example: https://jsonplaceholder.typicode.com/posts/1/comments
    #     # Sending Get Request with ID
    #     request = self.Posts.get_comments_by_id(1)
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
