from flask import Blueprint, render_template, jsonify, request
from http import HTTPStatus

errors_bp = Blueprint('errors', __name__)


def wants_json():
    return request.path.startswith('/api/') or request.is_json


@errors_bp.app_errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    if wants_json():
        return (
            jsonify({'message': 'Указанный id не найден'}),
            HTTPStatus.NOT_FOUND
        )
    return render_template(
        'errors/404.html'
    ), HTTPStatus.NOT_FOUND


@errors_bp.app_errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    if wants_json():
        return (
            jsonify({'message': 'Внутренняя ошибка сервера'}),
            HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return render_template(
        'errors/500.html'
    ), HTTPStatus.INTERNAL_SERVER_ERROR