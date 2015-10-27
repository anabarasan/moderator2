import logging

from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

from authentication import BaseHandler
from authentication import app


@app.route('/login', 'login')
class LoginHandler(BaseHandler):
    def get(self):
        self._serve_page()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        try:
            u = self.auth.get_user_by_password(username, password, remember=True,
              save_session=True)
            self.redirect(self.uri_for('home'))
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Login failed for user %s because of %s', username, type(e))
            self._serve_page(True)

    def _serve_page(self, failed=False):
        username = self.request.get('username')
        params = {
          'username': username,
          'failed': failed
        }
        self.render_template('login.html', params)


@app.route('/logout', 'logout')
class LogoutHandler(BaseHandler):
    def get(self):
        self.auth.unset_session()
        self.redirect(self.uri_for('login'))
