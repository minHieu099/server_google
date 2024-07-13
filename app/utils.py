from newspaper import Config, Article
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
def extract_text_from_url(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10

    page = Article(url, config=config)
    text = ""

    try:
        page.download()
        page.parse()
        text = page.text
    except Exception as e:
        print(f"An error occurred: {e}")

    return text
def extract_top_keywords(data):
    # Đọc danh sách stopwords từ file 'stopwords.txt'
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = f.read().split()

    # Tạo text từ các từ không nằm trong stopwords
    text = ' '.join(item["từ"] for item in data if item["từ"] not in stopwords)

    # Tính toán TF-IDF scores
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([text] if text else [""])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = X.toarray()[0] if text else [0] * len(feature_names)

    # Tạo dictionary TF-IDF
    tfidf_dict = dict(zip(feature_names, tfidf_scores))

    # Sắp xếp theo điểm số TF-IDF giảm dần và chọn top 5
    sorted_tfidf = sorted(tfidf_dict.items(), key=lambda item: item[1], reverse=True)[:5]

    # Tạo kết quả cuối cùng
    result = []

    for word, score in sorted_tfidf:
        try:
            loai_tu = next(item["loại từ"] for item in data if item["từ"] == word)
            result.append({"từ khóa": word, "loại từ": loai_tu, "điểm số": score})
        except StopIteration:
            continue

    return result
def get_word_info(text):
    url = 'http://localhost:8000/words'
    data = text
    
    try:
        response = requests.post(url,data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

# def extract_texts_from_urls(urls):
#     texts = []
#     for url in urls:
#         text = extract_text_from_url(url)
#         texts.append(text)
#     return texts

# texts = extract_texts_from_urls(urls)
# print(len(texts))
# for text in texts:

#     print(text)