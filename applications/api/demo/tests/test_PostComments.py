from core.api.common.BaseTest import BaseTest
from applications.api.demo.endpoints.Posts import Posts
from applications.api.demo.data.sources_mapping import Payload
from core.config.logger_config import setup_logger
from core.data.sources.JSON_reader import JSONReader
from core.utils.decorator import test

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

        asserts = [
            ('id', 101),
            ('title', 'foo'),
            ('body', 'bar'),
            ('userId', 1)
        ]

        errors = self.assert_group_equals(response=response, expected_values=asserts)
        self.add_report(test_data=self.test_create_posts, status_code=201, response=response, errors=errors)

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0002", test_description="Test Post Get All")
    def test_post_get_all(self):
        # Sending Get Request
        request = self.Posts.get_all_post()
        response = request.get_response()

        # Standard Validations: Status Code and Content Type
        self.add_report(test_data=self.test_post_get_all, status_code=200, response=response)

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0003", test_description="Test Get By ID")
    def test_post_by_id(self):
        # Sending Get Request
        response = self.Posts.get_post_by_id(post_id=1).get_response()

        asserts = [
            ('id', 1),
            ('title', 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit'),
            ('userId', 1)
        ]
        errors = self.assert_group_equals(response=response, expected_values=asserts)
        self.add_report(test_data=self.test_post_by_id, status_code=200, response=response, errors=errors)

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0004", test_description="Test Get Comments By ID")
    def test_comments_by_id(self):
        # URL Example: https://jsonplaceholder.typicode.com/posts/1/comments
        # Sending Get Request with ID
        response = self.Posts.get_comments_by_id(1).get_response()

        asserts = [
            ('postId', 1),
            ('id', 1),
            ('name', 'id labore ex et quam laborum'),
            ('email', 'Eliseo@gardner.biz'),
            ('body','laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium')
        ]

        errors = self.assert_group_equals(response=response, expected_values=asserts, response_list=True)
        self.add_report(test_data=self.test_comments_by_id, status_code=200, response=response, errors=errors)

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0005", test_description="Test Get Comments By ID with Params")
    def test_comments_by_id_with_params(self):
        # URL Example: https://jsonplaceholder.typicode.com/posts?postId=1
        # Sending Get Request with Param ID
        response = self.Posts.get_comments_by_id_params(post_id=1).get_response()

        asserts = [
            ('userId', 1),
            ('id', 1),
            ('title', 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit'),
            ('body','quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto')
        ]
        errors = self.assert_group_equals(response=response, expected_values=asserts, response_list=True)
        self.add_report(test_data=self.test_comments_by_id_with_params, status_code=200, response=response,
                        errors=errors)

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0006", test_description="Test Update a Post")
    def test_update_posts(self):
        payload = {
            "title": "foo2",
            "body": "bar2",
        }

        asserts = [
            ('title', 'foo2'),
            ('body', 'bar2')
        ]

        # Sending Put Request with Param ID
        response = self.Posts.update_post(post_id=1, json=payload).get_response()
        errors = self.assert_group_equals(response=response, expected_values=asserts)
        self.add_report(test_data=self.test_update_posts, status_code=200, response=response, errors=errors)

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0007", test_description="Test Patching a Post")
    def test_patching_posts(self):
        payload = {
            "title": "foo3",
        }

        asserts = [
            ('title', 'foo3'),
        ]

        # Sending Patching Request with Param ID
        response = self.Posts.patching_post(post_id=1, json=payload).get_response()
        errors = self.assert_group_equals(response=response, expected_values=asserts)
        self.add_report(test_data=self.test_patching_posts, status_code=200, response=response, errors=errors)

    # @pytest.mark.skip(reason="Skip")
    @test(test_case_id="API-0008", test_description="Test Delete a Post")
    def test_delete_posts(self):
        # Sending Delete Request with ID
        response = self.Posts.delete_post(post_id=1).get_response()
        self.add_report(test_data=self.test_delete_posts, status_code=200, response=response)

