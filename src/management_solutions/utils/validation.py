def validate_int(obj, errors: dict, field_name: str):
    value = getattr(obj, field_name)
    # If it's already an int, it's valid
    if isinstance(value, int):
        return True
    # If it's a string of digits, convert it
    try:
        setattr(obj, field_name, int(value))
        return True
    except(ValueError, TypeError):
        errors.setdefault(field_name, []).append(f"{field_name} inputted is not a valid number")
        return False

def validate_str(obj, errors: dict, field_name: str):
    value = getattr(obj, field_name)
    # If it's already an int, it's valid
    if isinstance(value, str):
        return True
    # If it's a string of digits, convert it
    try:
        setattr(obj, field_name, str(value))
        return True
    except(ValueError, TypeError):
        errors.setdefault(field_name, []).append(f"{field_name} inputted is not a valid string")
        return False


