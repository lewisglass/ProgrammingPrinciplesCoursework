from datetime import datetime

def check_input(validation_func, user_prompt):
        """run validation functions whilst also allowing the user to renter information
        when mistakes are made"""
        while True:
            try:
                user_value = validation_func(input(user_prompt))
            except ValueError as error:
                print(f"Invalid value: {error}\n try again")
                continue
            except TypeError as error:
                print(f"Invalid type: {error}\n try again")
                continue
            break
        return user_value

def validate_str(input_str: str, max_length = 70) -> str:
    """Method for validating str"""
    if not isinstance(input_str, str):
        raise TypeError("Input must be a string")
    if not input_str.strip():
        raise ValueError("Input must not be an empty string")
    if not (len(input_str) <= max_length):
        raise ValueError(f"Input must be no more than {max_length} chars")
    return input_str

def validate_y_n(input_str: str) -> str:
    """validate yes(y) or no(n) inputs from the user"""
    try:
        refined_str = validate_str(input_str, 1)
        if refined_str == 'n' or refined_str == 'y':
            return refined_str
        else:
            raise ValueError("Input must be y or n")
    except ValueError as error:
        raise ValueError(f"Invalid value: {error}\n try again")
    except TypeError as error:
        raise TypeError(f"Invalid type: {error}\n try again")

def validate_int(input_int: int | str, min_size = 0, max_size = 100) -> int:
    """validate integer inputs supplied by the user"""
    try:
        input_int = int(input_int)
    except ValueError as error:
        raise ValueError("Could not convert input to integer") from error
    if not (min_size <= input_int <= max_size):
        raise ValueError(f"Input must be between {min_size} and {max_size}")
    return input_int

def validate_date(input_date: str | datetime) -> datetime:
    """Method for validating date"""
    date_format = '%Y-%m-%d'
    try:
        if isinstance(input_date, str):
            date = datetime.strptime(input_date, date_format)
        else:
            date = input_date
    except ValueError as error:
        raise ValueError("Incorrect date format in input") from error
    return date