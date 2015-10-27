from webapp2_extras import auth
from BaseHandler import BaseHandler
from application import app
from application import sendmail
import logging


def user_required(handler):
    """
      Decorator that checks if there's a user associated with the current session.
      Will also fail if there's no session present.
    """
    def check_login(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect(self.uri_for('login'), abort=True)
        else:
            return handler(self, *args, **kwargs)

    return check_login


from SignupHandler import SignupHandler
from VerificationHandler import VerificationHandler
from PasswordHandler import ForgotPasswordHandler, SetPasswordHandler
from LoginLogoutHandler import LoginHandler, LogoutHandler
