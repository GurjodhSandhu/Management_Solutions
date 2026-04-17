
def validate_int(obj, errors: dict, field_name: str):
    value = getattr(obj, field_name)
    # If it's already an int, it's valid
    if isinstance(value, int):
        return True
    # If it's a string of digits, convert it
    if isinstance(value, str) and value.isdigit():
        setattr(obj, field_name, int(value))
        return True
    # Otherwise, it's invalid
    errors.setdefault(field_name, []).append(f"{field_name} inputted is not a valid number")
    return False
