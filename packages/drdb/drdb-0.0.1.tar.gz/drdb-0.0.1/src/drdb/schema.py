import re

class SchemaValidator:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data):
        errors = []
        for key, validator in self.schema.items():
            value = data.get(key)

            if isinstance(validator, Use):
                try:
                    value = validator.function(value)
                except Exception as e:
                    errors.append(f"Validation failed for '{key}': {e}")
            elif isinstance(validator, Const):
                if value != validator.value:
                    errors.append(f"'{key}' should be {validator.value}")
            elif isinstance(validator, And):
                sub_errors = []
                for sub_validator in validator.validators:
                    try:
                        value = sub_validator(value)
                    except Exception as e:
                        sub_errors.append(f"Validation failed for '{key}': {e}")
                if sub_errors:
                    errors.extend(sub_errors)
            elif isinstance(validator, Schema):
                try:
                    validator.validate(value)
                except ValueError as e:
                    errors.append(f"'{key}': {e}")
            elif callable(validator):
                try:
                    value = validator(value)
                except Exception as e:
                    errors.append(f"Validation failed for '{key}': {e}")
            elif isinstance(validator, type):
                if not isinstance(value, validator):
                    errors.append(f"'{key}' should be of type {validator.__name__}")
            elif isinstance(validator, str) and re.match(validator, str(value)):
                pass
            else:
                errors.append(f"Validation failed for '{key}'")

        if errors:
            raise ValueError('\n'.join(errors))

class Use:
    def __init__(self, function):
        self.function = function

class Const:
    def __init__(self, value):
        self.value = value

class And:
    def __init__(self, *validators):
        self.validators = validators

class Schema:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data):
        validator = SchemaValidator(self.schema)
        validator.validate(data)

