from marshmallow import Schema, fields, validate, ValidationError

class RecipeSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    text = fields.Str()
    url = fields.Url()
    receivedAt = fields.Str()
