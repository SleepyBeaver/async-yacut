from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField
from wtforms.validators import (
    DataRequired, Length, Optional, URL, Regexp
)
from wtforms import ValidationError
from .models import URLMap

MAX_SHORT_LENGTH = 16


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(), URL()]
    )

    custom_id = StringField(
        'Короткая ссылка',
        validators=[
            Optional(),
            Length(max=MAX_SHORT_LENGTH),
            Regexp(
                r'^[a-zA-Z0-9]+$',
                message=(
                    'Короткая ссылка может содержать только '
                    'латинские буквы и цифры.'
                )
            )
        ]
    )

    def validate_custom_id(self, field):
        if not field.data:
            return

        if field.data.lower() == 'files':
            raise ValidationError(
                'Предложенный вариант короткой ссылки уже существует.'
            )

        if URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(
                'Предложенный вариант короткой ссылки уже существует.'
            )


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[DataRequired()]
    )