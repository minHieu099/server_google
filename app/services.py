from flask import Blueprint, jsonify, request 
import requests
from .models import db, SearchInfo, SearchDetails
import json
from .utils import (
    extract_keywords,
    extract_urls,
    get_word_info,
    extract_text_and_title_from_url,
    extract_top_keywords,
    calculate_cosine_similarity
)
service = Blueprint('service', __name__)

@service.route('/search', methods=['GET'])
def search():
    api_key = 'AIzaSyDAqNeQ-272X6sp8DGYu6DDI2Z0vMUEXJY'
    cx = 'e51fe1300c9914e7d'
    query = request.args.get('q')
    start = request.args.get('start', default='1')
    num = request.args.get('num', default='10')
    date_restrict = request.args.get('dateRestrict', default='m1')
    lr = request.args.get('lr', default='lang_vi')

    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}&start={start}&num={num}&dateRestrict={date_restrict}&lr={lr}'

    try:
        response = requests.get(url)
        response.raise_for_status()  
        response_data = response.json()
        items = response_data.get('items', [])
        array_of_elements = []
        for index, item in enumerate(items, start=1):
            element = {
                'stt': index,
                'url': item['link'],
                'title': item['title'],
                'content': '',  
                'snippet': item.get('snippet', ''),
                'labeled_pos': [], 
                'extract_content': [],
                'original_keywords':[],  
                'cosine_degree': 0.0  
            }
            array_of_elements.append(element)
        process_data(array_of_elements, response_data)
 
        filtered_elements = []
        for element in array_of_elements:
            filtered_element = {
                'stt': element['stt'],
                'url': element['url'],
                'title': element['title'],
                # 'content': element['content'],
                'snippet': element['snippet'],
                'extract_content': element['extract_content'],
                'original_keywords':extract_keywords(response_data),
                'cosine_degree': element['cosine_degree']
            }
            filtered_elements.append(filtered_element)

        filtered_elements.sort(key=lambda x: x['cosine_degree'], reverse=True)
        
        return jsonify(filtered_elements)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


def process_data(array_of_elements,response):
    for element in array_of_elements:
        content = extract_text_and_title_from_url(element['url'])
        if content:
   
            element['content'] = content
            content_info = get_word_info(content)
      
            if content_info:
                element['labeled_pos'] = content_info
                top_keywords = extract_top_keywords(content_info)
                print(top_keywords)
                
                if top_keywords:

                    element['extract_content'] = top_keywords
                    calculate_cosine_similarity([element], original_keywords=extract_keywords(response))
                    print("Kết quả: ",calculate_cosine_similarity)
    return array_of_elements

@service.route('/add_search_data', methods=['POST'])
def add_search_data():
    data = request.json
    try:
  
        search_info = SearchInfo(
            keywords=data['keywords'],
            access_time=data['access_time'],
            completed=data['completed']
        )
        db.session.add(search_info)
        db.session.flush()  

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

        db.session.commit()  
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": str(e)}), 400
