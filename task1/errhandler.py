def input_error(args_count):
    def decorator(func):
        def wrapper(args, contacts):
            if len(args) != args_count:
                return False, f"Command should have '{args_count}' arguments."
            try:
                return func(args, contacts)
            except InvalidPhoneError:
                return "Invalid phone number format."
            except InvalidBirthdayError:
                return "Invalid date format. Should be DD.MM.YYYY"
            except (KeyError, ValueError, IndexError):
                return "Invalid command or argument. Please try again."
        return wrapper
    return decorator

class InvalidPhoneError(Exception):
    pass

class InvalidBirthdayError(Exception):
    pass
