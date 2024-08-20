
class MessagingSystemException(Exception):
    def __init__(self, status_code, message, *args: object) -> None:
        super().__init__(*args)
        self.status_code = status_code
        self.message = message

class WrongCredentialsException(MessagingSystemException):
    def __init__(self, *args: object) -> None:
        super().__init__(403,f"Credentials given doesn't match existing user", *args)

class TokenExpiredException(MessagingSystemException):
    def __init__(self, *args: object) -> None:
        super().__init__(401, "Token Expired", *args)

class TokenInvalidException(MessagingSystemException):
    def __init__(self, *args: object) -> None:
        super().__init__(401, "Invalid Token", *args)
        
class UserAlreadyExists(MessagingSystemException):
    def __init__(self, username, *args: object) -> None:
        super().__init__(400, f"{username} already exists", *args)
        
class AlreadyContactException(MessagingSystemException):
    def __init__(self, *args: object) -> None:
        super().__init__(400, "User is a contact already", *args)
        
        
