from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField
from wtforms.validators import DataRequired, Length, Optional, URL
from wtforms import ValidationError
import re
from .models import URLMap

MAX_SHORT_LENGTH = 16
ALLOWED_CHARS_REGEX = re.compile(r'^[a-zA-Z0-9]+$')


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(), URL()]
    )

    custom_id = StringField(
        'Короткая ссылка',
        validators=[Optional(), Length(max=MAX_SHORT_LENGTH)]
    )

    def validate_custom_id(self, field):
        if not field.data:
            return

        if field.data.lower() == 'files':
            raise ValidationError(
                'Предложенный вариант короткой ссылки уже существует.'
            )

        if not ALLOWED_CHARS_REGEX.match(field.data):
            raise ValidationError(
                'Короткая ссылка может содержать только '
                'латинские буквы и цифры.'
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