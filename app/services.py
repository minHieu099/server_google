from flask import Blueprint, jsonify, request  # Import request từ Flask
import requests
from .models import db, SearchInfo, SearchDetails
import json
service = Blueprint('service', __name__)

@service.route('/search', methods=['GET'])
def search():
    api_key = 'AIzaSyAwdj-EI-cklL17C4TlvnxqFIXpgql_AQ8'  
    cx = 'f7b7ab1f41c114b39'  

    # Sử dụng request.args.get để lấy các tham số từ query string
    query = request.args.get('q')
    start = request.args.get('start', default='1')
    num = request.args.get('num', default='10')
    date_restrict = request.args.get('dateRestrict', default='m1')
    lr = request.args.get('lr', default='lang_vi')

    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}&start={start}&num={num}&dateRestrict={date_restrict}&lr={lr}'

    try:
        response = requests.get(url)
        response_data = response.json()

        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@service.route('/add_search_data', methods=['POST'])
def add_search_data():
    data = request.json
    try:
        # Tạo và thêm SearchInfo
        search_info = SearchInfo(
            keywords=data['keywords'],
            access_time=data['access_time'],
            completed=data['completed']
        )
        db.session.add(search_info)
        db.session.flush()  # Để lấy ID cho SearchInfo ngay lập tức

        # Tạo và thêm SearchDetails cho mỗi item trong 'details'
        for detail in data['details']:
            search_detail = SearchDetails(
                search_info_id=search_info.id,
                link=detail['link'],
                title=detail['title'],
                content=detail['content'],
                content_processed=json.dumps(detail['content_processed']),
                keywords_extracted=json.dumps(detail['keywords_extracted']),
                confidence_level=detail['confidence_level']
            )
            db.session.add(search_detail)

        db.session.commit()  # Hoàn tất giao dịch
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        return jsonify({"error": str(e)}), 400
