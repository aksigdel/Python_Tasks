class Error(Exception):
    """
    Base class for other exceptions
    """
    pass

class ValueNotFound(Error):
    """
    Raised when value is not found in database
    """
    pass

class ValueDuplicate(Error):
    """
    Raised when value is already present in database
    """
    pass