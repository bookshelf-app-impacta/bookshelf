from marshmallow import Schema, fields, validate


class BookCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    original_title = fields.Str(required=False, allow_none=True, data_key="originalTitle")
    slug = fields.Str(required=False, validate=validate.Length(min=1, max=280))
    release_year = fields.Int(required=False, allow_none=True, data_key="releaseYear",
                              validate=validate.Range(min=1400, max=2200))
    synopsis = fields.Str(required=False, allow_none=True)
    cover_url = fields.Url(required=False, allow_none=True, data_key="coverUrl")
    isbn13 = fields.Str(required=False, allow_none=True, validate=validate.Length(min=13, max=13))
    publisher = fields.Str(required=False, allow_none=True, validate=validate.Length(max=150))
    page_count = fields.Int(required=False, allow_none=True, data_key="pageCount",
                            validate=validate.Range(min=1, max=65535))
    language = fields.Str(required=False, allow_none=True, validate=validate.Length(max=40))
    author_id = fields.Integer(required=False, allow_none=True, data_key="authorId")
    genre_id = fields.Integer(required=False, allow_none=True, data_key="genreId")


class BookUpdateSchema(Schema):
    title = fields.Str(required=False, validate=validate.Length(min=1, max=255))
    original_title = fields.Str(required=False, allow_none=True, data_key="originalTitle")
    slug = fields.Str(required=False, validate=validate.Length(min=1, max=280))
    release_year = fields.Int(required=False, allow_none=True, data_key="releaseYear",
                              validate=validate.Range(min=1400, max=2200))
    synopsis = fields.Str(required=False, allow_none=True)
    cover_url = fields.Url(required=False, allow_none=True, data_key="coverUrl")
    isbn13 = fields.Str(required=False, allow_none=True, validate=validate.Length(min=13, max=13))
    publisher = fields.Str(required=False, allow_none=True, validate=validate.Length(max=150))
    page_count = fields.Int(required=False, allow_none=True, data_key="pageCount",
                            validate=validate.Range(min=1, max=65535))
    language = fields.Str(required=False, allow_none=True, validate=validate.Length(max=40))
    author_id = fields.Integer(required=False, allow_none=True, data_key="authorId")
    genre_id = fields.Integer(required=False, allow_none=True, data_key="genreId")
