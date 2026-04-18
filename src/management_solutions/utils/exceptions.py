class ValidationError(Exception):
    def __init__(self, errors_dict: dict):
        self.errors = errors_dict
        super().__init__("Validation failed")

