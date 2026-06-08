from marshmallow import Schema, fields, validate, validates, ValidationError


class StudentRegisterSchema(Schema):
    email    = fields.Email(required=True, error_messages={"required": "Email is required.", "invalid": "Enter a valid email address."})
    password = fields.Str(required=True, validate=validate.Length(min=6, error="Password must be at least 6 characters."), error_messages={"required": "Password is required."})
    full_name = fields.Str(required=True, validate=validate.Length(min=1, error="Full name is required."), error_messages={"required": "Full name is required."})

    @validates("full_name")
    def validate_full_name(self, value):
        if not value.strip():
            raise ValidationError("Full name is required.")


class CompanyRegisterSchema(Schema):
    email    = fields.Email(required=True, error_messages={"required": "Email is required.", "invalid": "Enter a valid email address."})
    password = fields.Str(required=True, validate=validate.Length(min=6, error="Password must be at least 6 characters."), error_messages={"required": "Password is required."})
    name     = fields.Str(required=True, validate=validate.Length(min=1, error="Company name is required."), error_messages={"required": "Company name is required."})

    @validates("name")
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Company name is required.")


class LoginSchema(Schema):
    email    = fields.Email(required=True, error_messages={"required": "Email is required.", "invalid": "Enter a valid email address."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})