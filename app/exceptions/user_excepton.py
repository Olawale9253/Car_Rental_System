class UsernameAlreadyExistsException(Exception):
    def __init__(self, message="Username already exists"):
        self.message = message

class EmailAlreadyExistsException(Exception):
    def __init__(self, message="Email already exists"):
        self.message = message

class InvalidCredentialsException(Exception):
    def __init__(self, message="Invalid credentials"):
        self.message = message

class UnauthorizedException(Exception):
    def __init__(self, message="User not logged in"):
        self.message = message
