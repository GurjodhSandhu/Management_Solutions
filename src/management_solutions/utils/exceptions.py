class TruckValidationError(Exception):
    def __init__(self, errors_dict: dict):
        self.errors = errors_dict
        super().__init__("Validation failed")



class InvalidVinError(Exception):
    pass
class InvalidYearError(Exception):
    pass
class InvalidMileageError(Exception):
    pass
class InvalidPlateError(Exception):
    pass
