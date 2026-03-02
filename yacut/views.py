from flask import Blueprint, render_template, redirect, url_for
from . import db
from .models import URLMap
from .forms import URLForm, FileUploadForm
from .utils import get_unique_short_id

views_bp = Blueprint('views', __name__)


@views_bp.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        short_id = custom_id or get_unique_short_id()

        url_map = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(url_map)
        db.session.commit()

        short_link = url_for(
            'views.redirect_view',
            short_id=short_id,
            _external=True
        )
        return render_template('index.html', form=form, short_link=short_link)

    return render_template('index.html', form=form)


@views_bp.route('/files', methods=['GET', 'POST'])
def upload_files():
    form = FileUploadForm()
    return render_template('files.html', form=form)


@views_bp.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)