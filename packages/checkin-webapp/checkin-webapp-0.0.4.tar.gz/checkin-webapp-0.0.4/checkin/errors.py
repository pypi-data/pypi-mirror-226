# ------------------------------ Some Exceptions ----------------------------- #
class UserNameTakenError(Exception):
    pass

class EmailTakenError(Exception):
    """Used to indicate that the email is already taken"""


