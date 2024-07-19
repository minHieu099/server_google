from newspaper import Config, Article
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
def extract_keywords(data):
    search_terms = data["queries"]["request"][0]["searchTerms"]
    keywords = search_terms.replace("\"", "").split(", ")
    modified_keywords = [keyword.replace(" ", "_") for keyword in keywords]
    return modified_keywords
def extract_urls(response):
    urls = []
    if 'items' in response and len(response['items']) > 0:
        for item in response['items']:
            if 'link' in item:
                urls.append(item['link'])
    return urls
def get_word_info(text):
    url = 'http://localhost:8000/words'
    data =text
    
    try:
        response = requests.post(url, data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
def extract_text_and_title_from_url(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10

    page = Article(url, config=config)
    text = ""
    title = ""
    try:
        page.download()
        page.parse()
        text = page.text
        # title = page.title
    except Exception as e:
        print(f"An error occurred: {e}")

    return text
def extract_top_keywords(data):
    # Đọc danh sách stopwords từ file 'stopwords.txt'
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = f.read().split()

    text = ' '.join(item["từ"] for item in data if item["từ"] not in stopwords)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([text] if text else [""])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = X.toarray()[0] if text else [0] * len(feature_names)

    tfidf_dict = dict(zip(feature_names, tfidf_scores))

    sorted_tfidf = sorted(tfidf_dict.items(), key=lambda item: item[1], reverse=True)[:5]

    result = []

    for word, score in sorted_tfidf:
        try:
            loai_tu = next(item["loại từ"] for item in data if item["từ"] == word)
            result.append({"từ khóa": word, "loại từ": loai_tu, "điểm số": float(round(score, 2))})  
        except StopIteration:
            continue

    return result
def calculate_cosine_similarity(array_of_elements, original_keywords):
    for element in array_of_elements:
        extracted_keywords = element['extract_content']
        
      
        all_keywords = {kw['từ khóa']: 0 for kw in extracted_keywords}
        for kw in original_keywords:
            all_keywords[kw] = 0
        
       
        extracted_vector = np.zeros(len(all_keywords))
        for kw in extracted_keywords:
            index = list(all_keywords.keys()).index(kw['từ khóa'])
            extracted_vector[index] = kw['điểm số']
        
      
        original_vector = np.zeros(len(all_keywords))
        for kw in original_keywords:
            if kw in all_keywords:
                index = list(all_keywords.keys()).index(kw)
                original_vector[index] = 1
        

        similarity = cosine_similarity([extracted_vector], [original_vector])[0][0]
    
        element['cosine_degree'] = float(round(similarity, 2))

    return array_of_elements