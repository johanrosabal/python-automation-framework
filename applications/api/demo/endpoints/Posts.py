from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('Post')


class Posts(BaseApi):

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = Posts()
            cls.name = __class__.__name__
            cls.endpoint = "posts"
        return cls._instance

    def create_posts(self, data=None, json=None):
        logger.info(f"[{self.name}]: Create a Posts")
        response = self.post_request() \
            .set_endpoint(self.endpoint) \
            .add_header("Content-Type", "application/json") \
            .set_json(json) \
            .set_data(data) \
            .set_timeout(10) \
            .set_allow_redirects(False) \
            .send() \
            .get_response()

        return response

    def get_all_post(self):
        logger.info(f"[{self.name}]: Get All Post")
        response = self.get_request() \
            .set_endpoint(self.endpoint) \
            .set_timeout(10) \
            .send() \
            .get_response()
        return response

    def get_post_by_id(self, post_id):
        logger.info(f"[{self.name}]: Get Post By ID: {post_id}")
        response = (self.get_request()
                    .set_endpoint(self.endpoint + "/{post_id}")
                    .build_url(post_id=post_id)  # Allow Multiple Values -> post_id=1, post_name="my-post"
                    .set_timeout(10)
                    .send()
                    .get_response()
                    )
        return response

    def get_comments_by_id(self, post_id):
        # URL Example: https://jsonplaceholder.typicode.com/posts/1/comments
        logger.info(f"[{self.name}]: Get Comments By ID:{post_id}")
        response = (self.get_request()
                    .set_endpoint(self.endpoint + "/{post_id}/comments")
                    .build_url(post_id=post_id)  # Allow Multiple Values -> post_id=1, post_name="my-post"
                    .set_timeout(10)
                    .send()
                    .get_response()
                    )
        return response

    def get_comments_by_id_params(self, post_id):
        # URL Example: https://jsonplaceholder.typicode.com/posts?postId=1
        logger.info(f"[{self.name}]: Get Comments By ID with Params")
        params = {'postId': post_id}
        response = (self.get_request()
                    .set_endpoint(self.endpoint)
                    .set_params(params)
                    .set_timeout(10).send()
                    .send()
                    .get_response()
                    )
        return response

    def update_post(self, post_id, json):
        logger.info(f"[{self.name}]: Update a Posts")
        response = (self.put_request()
                    .set_endpoint(self.endpoint + "/{id_post}")
                    .add_header("Content-Type", "application/json")
                    .build_url(id_post=post_id)
                    .set_json(json)
                    .send()
                    .get_response()
                    )
        return response

    def patching_post(self, post_id, json):
        logger.info(f"[{self.name}]: Patching a Posts")
        response = (self.patch_request()
                    .set_endpoint(self.endpoint + "/{post_id}")
                    .add_header("Content-Type", "application/json")
                    .build_url(post_id=post_id)
                    .set_json(json)
                    .send()
                    .get_response()
                    )
        return response

    def delete_post(self, post_id):
        logger.info(f"[{self.name}]: Delete a Posts")
        response = (self.delete_request()
                    .set_endpoint(self.endpoint+"/{post_id}")
                    .build_url(post_id=post_id)
                    .send()
                    .get_response())
        return response
        # return self.DELETE(endpoint=f"posts/{id_post}")
