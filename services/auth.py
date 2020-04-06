from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, SessionUser


class AuthService:
    @staticmethod
    def if_exists(email):
        """Checks if a user with the given email exists."""
        user = User.objects.filter(email=email).first()
        if user:
            return user
        return False

    @staticmethod
    def get_user_by_email(email):
        """Return the user instance for given email"""
        return User.objects.filter(email=email).first()

    @staticmethod
    def get_session_user_by_email(email):
        """Returns the session user instance for given user email"""
        user = User.objects.filter(email=email).first()
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
    def create_user(email, name, password):
        """ This method creates a user for the SignUp process."""
        # Checking if the user is already present in the database
        # if a user is found, we an error message will raise saying user is already present with this email.
        if AuthService.if_exists(email):
            return {'value': False,
                    'error': 'User is already present with this email. Please try with another email or login'}

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256')).save()

        if AuthService.login_user_wrapper(email, True):
            return {'value': True, 'data': new_user.to_dict(), 'msg': 'User created successfully'}
        return {'value': False, 'error': 'Operation unsuccessful'}

    @staticmethod
    def login(email, password, remember):
        """ Log in a user into the application and returns a session user object."""
        # check if user actually exists
        user = AuthService.get_user_by_email(email)
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

