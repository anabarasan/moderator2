import logging
from appconfig import LOG_LEVEL, SECRET_KEY
from wsgi import WSGIApplication
from google.appengine.api import mail
from appconfig import EMAIL

config = {
  'webapp2_extras.auth': {
    'user_model': 'models.User',
    'user_attributes': ['name']
  },
  'webapp2_extras.sessions': {
    'secret_key': SECRET_KEY
  }
}

app = WSGIApplication([], debug=True, config=config)

logging.getLogger().setLevel(LOG_LEVEL)


def sendmail(reciever, subject, body):
    message = mail.EmailMessage(sender="Mongoose Moderator <%s>" % (EMAIL),
                                to=reciever,
                                subject=subject,
                                body=body)
    message.send()

from authentication import (ForgotPasswordHandler,
                    LoginHandler, LogoutHandler, SignupHandler,
                    SetPasswordHandler, VerificationHandler)

from moderator import (CreateTopic, EditTopic, LikeTopic, ListTopic)
