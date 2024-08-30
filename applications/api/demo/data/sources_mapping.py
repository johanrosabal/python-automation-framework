# mapping -> {'File Column Name' : 'Object Field Key'}
import json


class Payload:
    # Define the mapping fields
    mapping = {
        'id': 'id',
        'title': 'title',
        'body': 'body',
        'userId': 'user_id'
    }

    def __init__(self, id, title, body, user_id):
        self.id = id
        self.title = title
        self.body = body
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "userId": self.user_id
        }

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "userId": self.user_id
        })

    def __repr__(self):
        return f"Payload(id={self.id}, title={self.title}, body={self.body}, userId={self.user_id})"

