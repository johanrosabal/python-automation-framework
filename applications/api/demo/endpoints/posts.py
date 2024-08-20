from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('Post')


class Post(BaseApi):

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = Post()
            cls.name = __class__.__name__
        return cls._instance

    def get_all_post(self):
        logger.info(f"[{self.name}]: Get All Post")
        return self.GET(endpoint="posts")

    def get_post_by_id(self, id_post):
        logger.info(f"[{self.name}]: Get Post By ID")
        return self.GET(endpoint=f"posts/{id_post}")

    def get_comments_by_id(self, id_post):
        logger.info(f"[{self.name}]: Get Comments By ID")
        return self.GET(endpoint=f"posts/{id_post}/comments")

    def get_comments_by_id_params(self, params):
        logger.info(f"[{self.name}]: Get Comments By ID with Params")
        url = "comments"
        params = {'postId': params}
        return self.GET(endpoint=url, params=params)

    def create_posts(self, json, headers):
        logger.info(f"[{self.name}]: Create a Posts")
        return self.POST(endpoint="posts", json=json, headers=headers)

    def update_post(self, id_post, json, headers):
        logger.info(f"[{self.name}]: Update a Posts")
        return self.PUT(endpoint=f"posts/{id_post}", json=json, headers=headers)

    def patching_post(self,id_post, json, headers):
        logger.info(f"[{self.name}]: Patching a Posts")
        return self.PATCH(endpoint=f"posts/{id_post}", json=json, headers=headers)

    def delete_post(self, id_post):
        logger.info(f"[{self.name}]: Delete a Posts")
        return self.DELETE(endpoint=f"posts/{id_post}")


