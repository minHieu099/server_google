from flask import Blueprint, jsonify, request  # Import request từ Flask
import requests

main = Blueprint('main', __name__)

@main.route('/search', methods=['GET'])
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
