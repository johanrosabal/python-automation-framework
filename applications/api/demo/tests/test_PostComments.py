import pytest

from applications.api.demo.endpoints.posts import Post
from core.api.common.BaseTest import BaseTest

from core.config.logger_config import setup_logger
from core.utils.decorator import test

logger = setup_logger('TestPost')


class TestPostComments(BaseTest):

    def setup_class(self):
        self.Post = Post.get_instance()
        self.content_type = "application/json; charset=utf-8"

    # @pytest.mark.skip(reason="no way of currently testing this")
    @test(test_case_id="API-0001", test_description="Test Post Get All")
    def test_post_get_all(self):
        response = self.Post.get_all_post()
        validation = self.response().set_response(response)
        validation \
            .verify_status_success_code(200) \
            .verify_content_type(self.content_type) \

        # print(f"Time Response: {response.elapsed.total_seconds()}")

        # data = response.json()

    # @pytest.mark.skip(reason="no way of currently testing this")
    @test(test_case_id="API-0002", test_description="Test Get By ID")
    def test_post_by_id(self):
        response = self.Post.get_post_by_id(1)
        validation = self.response().set_response(response)
        validation \
            .verify_status_success_code(200) \
            .verify_content_type(self.content_type)

    # @pytest.mark.skip(reason="no way of currently testing this")
    @test(test_case_id="API-0003", test_description="Test Get Comments By ID")
    def test_comments_by_id(self):
        response = self.Post.get_comments_by_id(1)
        validation = self.response().set_response(response)
        validation \
            .verify_status_success_code(200) \
            .verify_content_type(self.content_type)

    # @pytest.mark.skip(reason="no way of currently testing this")
    @test(test_case_id="API-0004", test_description="Test Get Comments By ID with Params")
    def test_comments_by_id(self):
        response = self.Post.get_comments_by_id_params(1)
        validation = self.response().set_response(response)
        validation \
            .verify_status_success_code(200) \
            .verify_content_type(self.content_type)

    # @pytest.mark.skip(reason="no way of currently testing this")
    @test(test_case_id="API-0004", test_description="Test create a Post")
    def test_create_posts(self):
        payload = {
            "id": 101,
            "title": "foo",
            "body": "bar",
            "userId": 1
        }

        headers = {
            "Content-type": self.content_type
        }

        response = self.Post.create_posts(json=payload, headers=headers)
        validation = self.response().set_response(response)
        validation \
            .verify_status_success_code(201) \
            .verify_content_type(self.content_type)

    # @pytest.mark.skip(reason="no way of currently testing this")
    @test(test_case_id="API-0005", test_description="Test update a Post")
    def test_update_posts(self):
        id_post = 1

        payload = {
            "title": "foo2",
            "body": "bar2",
        }

        headers = {
            "Content-type": self.content_type
        }

        response = self.Post.update_post(id_post=id_post, json=payload, headers=headers)
        validation = self.response().set_response(response)
        validation \
            .verify_status_success_code(200) \
            .verify_content_type(self.content_type)

        logger.info(f"RESPONSE:\n{response.text}")

    # @pytest.mark.skip(reason="no way of currently testing this")
    @test(test_case_id="API-0006", test_description="Test update a Post")
    def test_patching_posts(self):
        id_post = 1

        payload = {
            "title": "foo3",
        }

        headers = {
            "Content-type": self.content_type
        }

        response = self.Post.patching_post(id_post=id_post, json=payload, headers=headers)
        validation = self.response().set_response(response)
        validation \
            .verify_status_success_code(200) \
            .verify_content_type(self.content_type)

        logger.info(f"RESPONSE:\n{response.text}")

    @test(test_case_id="API-0006", test_description="Test delete a Post")
    def test_delete_posts(self):
        id_post = 1
        response = self.Post.delete_post(id_post)
        validation = self.response().set_response(response)
        validation \
            .verify_status_success_code(200) \
            .verify_content_type(self.content_type)



