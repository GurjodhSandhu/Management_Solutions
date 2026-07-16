from management_solutions.utils.exceptions import ValidationError

class driver:
    def __init__(self, driver_id = None, assigned_truck_id = None, driver_name = None, driver_licensenumber = None):
        errors = {}
        self.driver_id = driver_id
        self.assigned_truck_id = assigned_truck_id
        self.driver_name = driver_name
        self.driver_licensenumber = driver_licensenumber

        if errors:
            raise ValidationError(errors)  # raises all validation errors as a dictionary


    def to_dict(self):
        return {
                "driver_name": self.driver_name,
                "driver_licensenumber": self.driver_licensenumber}
