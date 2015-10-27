from authentication import BaseHandler
from authentication import app
# from authentication import sendmail


@app.route('/signup', 'signup')
class SignupHandler(BaseHandler):
    def get(self):
        self.render_template('signup.html')

    def post(self):
        user_name = self.request.get('username')
        email = self.request.get('email')
        name = self.request.get('name')
        password = self.request.get('password')
        last_name = self.request.get('lastname')

        unique_properties = ['email_address']
        user_data = self.user_model.create_user(user_name,
          unique_properties,
          email_address=email, name=name, password_raw=password,
          last_name=last_name, verified=False)
        if not user_data[0]:  # user_data is a tuple
            self.display_message('Unable to create user for email %s because of \
              duplicate keys %s' % (user_name, user_data[1]))
            return

        user = user_data[1]
        user_id = user.get_id()

        token = self.user_model.create_signup_token(user_id)

        verification_url = self.uri_for('verification', type='v', user_id=user_id,
          signup_token=token, _full=True)

#         message = """Dear %s
#
# Your Mongoose Moderator Account has been created.
# Click the link below to verify.
#
# [%s]
#
# The Mongoose Moderator""" % (name, verification_url)
#
#         sendmail(email, "Your Mongoose Moderator account", message)

#         self.display_message("Click on the link to verify your account <br/> <a href='%s' class='btn btn-primary'>Verify</a>" % verification_url)
        self.redirect(verification_url)
