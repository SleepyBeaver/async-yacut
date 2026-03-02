from flask import Blueprint, render_template, jsonify, request

errors_bp = Blueprint('errors', __name__)


def wants_json():
    return request.path.startswith('/api/') or request.is_json


@errors_bp.app_errorhandler(404)
def page_not_found(error):
    if wants_json():
        return jsonify({'message': 'Указанный id не найден'}), 404
    return render_template('errors/404.html'), 404


@errors_bp.app_errorhandler(500)
def internal_error(error):
    if wants_json():
        return jsonify({'message': 'Внутренняя ошибка сервера'}), 500
    return render_template('errors/500.html'), 500