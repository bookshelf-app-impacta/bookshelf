from marshmallow import Schema, fields, validate

class BookCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    isbn = fields.Str(required=True, validate=validate.Length(min=10, max=20))
    publication_year = fields.Int(required=False, validate=validate.Range(min=1000, max=2100))
    publisher = fields.Str(required=False, validate=validate.Length(max=100))
    description = fields.Str(required=False)
    cover_url = fields.Str(required=False, validate=validate.URL())

class BookUpdateSchema(Schema):
    title = fields.Str(required=False, validate=validate.Length(min=1, max=200))
    author = fields.Str(required=False, validate=validate.Length(min=1, max=100))
    isbn = fields.Str(required=False, validate=validate.Length(min=10, max=20))
    publication_year = fields.Int(required=False, validate=validate.Range(min=1000, max=2100))
    publisher = fields.Str(required=False, validate=validate.Length(max=100))
    description = fields.Str(required=False)
    cover_url = fields.Str(required=False, validate=validate.URL())