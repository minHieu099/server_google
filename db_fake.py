import sqlite3


conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE search_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keywords TEXT,
    access_time TEXT,
    completed BOOLEAN
)
''')

cursor.execute('''
CREATE TABLE search_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_info_id INTEGER,
    link TEXT,
    title TEXT,
    content TEXT,
    content_processed TEXT,
    keywords_extracted TEXT,
    confidence_level REAL,
    FOREIGN KEY (search_info_id) REFERENCES search_info(id)
)
''')


search_info_data = [
    {
        "keyword": ["học tập", "nghiên cứu", "đào tạo"],
        "access_time": "2024-07-10T10:30:00",
        "completed": True
    },
    {
        "keyword": ["đi du lịch", "khám phá", "du lịch nghỉ dưỡng"],
        "access_time": "2024-07-09T15:45:00",
        "completed": False
    },
    {
        "keyword": ["lập trình", "phát triển ứng dụng", "coding"],
        "access_time": "2024-07-08T08:00:00",
        "completed": True
    }
]


search_details_data = [
    {
        "link": "https://example.com/bai-viet-1",
        "title": "Cách Đạt Được Thành Công Trong Sự Nghiệp",
        "content": "Cá độ bóng đá đa dạng về hình thức quy mô từ tự phát đến nhỏ lẻ ảnh hưởng đến mỗi tổ chức",
        "content_processed": "{cá_độ - V}, {bóng_đá - N}, {đa_dạng - A}, {về - V}, {hình_thức - N}, {quy_mô - N}, {từ - V}, {tự_phát - N}, {nhỏ_lẻ - A}, {cho - V}, {tổ_chức - N}",
        "keywords_extracted": "phát triển sự nghiệp: 0.34, mẹo thành công: 0.21, tăng trưởng chuyên nghiệp: 0.18",
        "confidence_level": 0.85
    }
]


for item in search_info_data:
    cursor.execute('''
    INSERT INTO search_info (keywords, access_time, completed)
    VALUES (?, ?, ?)
    ''', (','.join(item["keyword"]), item["access_time"], item["completed"]))


for item in search_details_data:
    cursor.execute('''
    INSERT INTO search_details (search_info_id, link, title, content, content_processed, keywords_extracted, confidence_level)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (1, item["link"], item["title"], item["content"], item["content_processed"], item["keywords_extracted"], item["confidence_level"]))


conn.commit()


cursor.execute('SELECT * FROM search_info')
search_info_rows = cursor.fetchall()

cursor.execute('SELECT * FROM search_details')
search_details_rows = cursor.fetchall()

print(search_info_rows, search_details_rows)
