# bot that deals with interactions with piazza
# sits in between Jarvis and Piazza
from piazza_api import Piazza
import json
import sys
import config
import os.path
from post import Post

from piazza_api.rpc import PiazzaRPC

INF = 100000

class Bot:
    def __init__(self, course_code=config.eecs281):
        self.piazza = Piazza()
        self.piazza.user_login(config.creds['email'], config.creds['password'])
        self.course = self.piazza.network(course_code)

        # rpc api to post notes
        self.piazza_rpc = PiazzaRPC(config.class_code)
        self.piazza_rpc.user_login(config.creds['email'], config.creds['password'])

    def get_all_posts_json(self):
        documents = []
        posts = []
        file_name = '{0}.txt'.format(config.class_code)
        if not os.path.isfile(file_name):
            data = self.course.iter_all_posts(limit=INF)
            for post in data:
                print('downloading post {0}'.format(post['nr']))
                documents.append(post)
                posts.append(Post(post))
            obj = open(file_name, 'wb')
            json.dump(documents, obj)
        else:
            obj = open(file_name, 'r')
            data = json.load(obj)
            for post in data:
                posts.append(Post(post))
        return posts

    def get_all_posts(self, start_id=0, limit=100):
        documents = []
        feed = self.course.get_feed()
        ids = [post['nr'] for post in feed['feed']]
        for post_id in ids:
            if post_id > start_id:
                print('downloading post {0}'.format(post_id))
                post_json = self.course.get_post(post_id)
                documents.append(Post(post_json))

        return documents

    def get_post(self, id):
        return Post(self.course.get_post(id))

    def create_post(self, subject, body, folder=['hw1']):
        params = {'type':'note','subject':subject, 'content':body, 'folders':folder}
        self.piazza_rpc.content_create(params)

    def create_answer(self, post_id, content):
        params = { 'cid': post_id, 'type': 'i_answer', 'content': content, 'revision': 0}
        return self.piazza_rpc.content_instructor_answer(params)