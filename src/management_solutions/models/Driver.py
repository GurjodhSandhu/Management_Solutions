from management_solutions.utils.exceptions import ValidationError

class driver:
    def __init__(self, driver_id = None, driver_name = None, driver_licenseNumber = None):
        errors = {}
        self.driver_id = driver_id
        self.driver_name = driver_name
        self.driver_licenseNumber = driver_licenseNumber

        if errors:
            raise ValidationError(errors)  # raises all validation errors as a dictionary



