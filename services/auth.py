from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from models.user import User, SessionUser
from services.user import UserService


class AuthService:
    @staticmethod
    def if_exists(email):
        """Checks if a user with the given email exists."""
        user = User.objects.filter(email=email).first()
        if user:
            return user
        return False

    @staticmethod
    def get_session_user_by_email(email):
        """Returns the session user instance for given user email"""
        user = UserService.get_users(emails=[email], paginate=False, data_objects=True).first()
        if user:
            return SessionUser(email=user.email, name=user.name)
        return None

    @staticmethod
    def login_user_wrapper(email, remember_me=False):
        """Login user and return instance"""
        if email:
            user = AuthService.get_session_user_by_email(email)
            return login_user(user, remember=remember_me)
        return False

    @staticmethod
    def register_user(email, name, password):
        """ This method registers a user for the SignUp process."""
        # Checking if the user is already present in the database
        # if a user is found, we an error message will raise saying user is already present with this email.
        if AuthService.if_exists(email):
            return {'value': False,
                    'error': 'User is already present with this email. Please try with another email or login'}

        new_user = UserService.create_user(email, name, password)

        if AuthService.login_user_wrapper(email, True):
            return {'value': True, 'data': new_user.to_dict(), 'msg': 'User created successfully'}
        return {'value': False, 'error': 'Operation unsuccessful'}

    @staticmethod
    def login(email, password, remember):
        """ Log in a user into the application and returns a session user object."""
        # check if user actually exists
        user = UserService.get_users(emails=[email], paginate=False, data_objects=True).first()
        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user.password, password):
            return {'value': False,
                    'error': 'Please check your login details.'}

        # if the above check passes, then we know the user has the right credentials
        if AuthService.login_user_wrapper(user.email, remember):
            session_user = AuthService.get_session_user_by_email(email)
            return {'value': True, 'data': session_user.to_dict(), 'msg': 'User logged in successfully'}
        return {'value': False, 'error': 'Operation unsuccessful'}

    @staticmethod
    def logout():
        """ Logs out a logged in user."""
        logout_user()
        return

    @staticmethod
    def validate_email(email):
        """Validates email"""
        import re
        # Regular expression for validating an Email
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex, email):
            return True
        return False

