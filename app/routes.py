from flask import Blueprint, jsonify
from .models import db, SearchInfo, SearchDetails
import json
main = Blueprint('main', __name__)

@main.route('/search_info', methods=['GET'])
def get_search_info():
    search_info = SearchInfo.query.all()
    return jsonify([{'id': info.id, 'keywords': info.keywords, 'access_time': info.access_time, 'completed': info.completed} for info in search_info]), 200, {'Content-Type': 'application/json; charset=utf-8'}

@main.route('/search_details/<int:info_id>', methods=['GET'])
def get_search_details(info_id):
    details = SearchDetails.query.filter_by(search_info_id=info_id).all()
    return jsonify([{
        'id': detail.id,
        'link': detail.link,
        'title': detail.title,
        'keywords_extracted': json.loads(detail.keywords_extracted),
        'confidence_level': detail.confidence_level
    } for detail in details]), 200, {'Content-Type': 'application/json; charset=utf-8'}

@main.route('/search_details/url/<int:detail_id>', methods=['GET'])
def get_detail_url(detail_id):
    detail = SearchDetails.query.get_or_404(detail_id)
    return jsonify({
        'link': detail.link,
        'title': detail.title,
        'content': detail.content,
        'content_processed': json.loads(detail.content_processed) if detail.content_processed else "",
        'keywords_extracted': json.loads(detail.keywords_extracted) if detail.keywords_extracted else [],
        'confidence_level': detail.confidence_level
    }), 200, {'Content-Type': 'application/json; charset=utf-8'}
