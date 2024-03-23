class FieldNotFoundError(Exception):
    """The error of missing a field in the model"""

    pass


class RecordDoesNotExistsError(Exception):
    """Error of an entry not found in the database"""

    pass


class TooManyValuesError(Exception):
    """The error occurs when there are many records in the database"""

    pass
