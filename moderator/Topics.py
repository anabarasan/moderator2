from collections import namedtuple
from moderator import user_required
from moderator import BaseHandler
from moderator import app
from models import Topic, Like, getKey
import logging

logger = logging.getLogger('Topic')

TOPIC = namedtuple('TOPIC', 'key topic description archived likes')


@app.route('/topic/new', 'create topic')
class CreateTopic(BaseHandler):
    @user_required
    def get(self):
        self.render_template('topiceditor.html')

    def post(self):
        topic = self.request.get('topic')
        description = self.request.get('description')
        if topic:
            user = self.user_info
            new_topic = Topic(topic=topic, description=description, createdBy=user['user_id'], modifiedBy=user['user_id'])
            new_topic.put()
            self.redirect(self.uri_for('home'))
        else:
            params = {
                'error': True,
                'topic': {
                    'topic': topic,
                    'description': description
                }
            }
            self.render_template('topiceditor.html', params)


@app.route('/topic/<topic_id>', 'edit topic')
class EditTopic(BaseHandler):
    @user_required
    def get(self, topic_id):
        key = getKey(topic_id)
        topic = key.get()
        self.render_template('topiceditor.html', {'topic': topic, 'edit': True})

    def post(self, topic_id):
        key = getKey(topic_id)
        topic = key.get()
        topic.topic = self.request.get('topic')
        topic.description = self.request.get('description')
        topic.archived = self.request.get('archive') == 'yes'
        topic.put()
        self.redirect(self.uri_for('home'))


@app.route('/topic/<topic_id>/like', 'like topic')
class LikeTopic(BaseHandler):
    @user_required
    def get(self, topic_id):
        key = getKey(topic_id)
        likes = Like.query().filter(Like.topic == key, Like.createdBy == self.user_info['user_id']).fetch(1)
        if len(likes) == 0:
            Like(topic=key, createdBy=self.user_info['user_id'], modifiedBy=self.user_info['user_id']).put()
        else:
            likes[0].key.delete()
        self.redirect(self.uri_for('home'))


@app.route('/', 'home')
class ListTopic(BaseHandler):
    @user_required
    def get(self):
        qry = Topic.query().order(Topic.topic)
        topics = []
        for row in qry:
            likes = Like.query().filter(Like.topic == row.key).count()
            topics.append(TOPIC(key=row.key, topic=row.topic, description=row.description, archived=row.archived, likes=likes))
        self.render_template('home.html', {'topics': topics})
