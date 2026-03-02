from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from . import db
from .models import URLMap
from .forms import URLForm, FileUploadForm
from .utils import get_unique_short_id
import asyncio
import aiohttp

views_bp = Blueprint('views', __name__)

YANDEX_DISK_BASE_URL = 'https://cloud-api.yandex.net'


async def upload_file_to_disk(session, token, filename, file_data):
    headers = {'Authorization': f'OAuth {token}'}

    async with session.get(
        f'{YANDEX_DISK_BASE_URL}/v1/disk/resources/upload',
        headers=headers,
        params={'path': f'disk:/{filename}', 'overwrite': 'true'}
    ) as resp:
        if resp.status != 200:
            return None, filename
        data = await resp.json()
        upload_href = data.get('href')

    if not upload_href:
        return None, filename

    async with session.put(upload_href, data=file_data, headers=headers) as resp:
        if resp.status not in (201, 202):
            return None, filename

    async with session.get(
        f'{YANDEX_DISK_BASE_URL}/v1/disk/resources/download',
        headers=headers,
        params={'path': f'disk:/{filename}'}
    ) as resp:
        if resp.status != 200:
            return None, filename
        data = await resp.json()
        download_href = data.get('href')

    return download_href, filename


async def upload_all_files(token, files_data):
    async with aiohttp.ClientSession() as session:
        tasks = [
            upload_file_to_disk(session, token, filename, data)
            for filename, data in files_data
        ]
        results = await asyncio.gather(*tasks)
    return [(url, name) for url, name in results if url is not None]


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
    uploaded_files_info = []

    if form.validate_on_submit():
        token = current_app.config.get('DISK_TOKEN')

        files_data = [
            (file.filename, file.read())
            for file in form.files.data
            if file.filename
        ]

        results = asyncio.run(upload_all_files(token, files_data))

        for download_url, filename in results:
            short_id = get_unique_short_id()
            url_map = URLMap(original=download_url, short=short_id)
            db.session.add(url_map)

            uploaded_files_info.append({
                'filename': filename,
                'short_link': url_for(
                    'views.redirect_view',
                    short_id=short_id,
                    _external=True
                )
            })

        db.session.commit()

    return render_template('files.html', form=form, files=uploaded_files_info)


@views_bp.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)