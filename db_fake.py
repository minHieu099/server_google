import sqlite3
import json

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
        "keyword": ["euro", "cờ bạc", "bóng đá", "tệ nạn", "cá cược"],
        "access_time": "2024-07-10T10:30:00",
        "completed": True
    },
]

search_details_data =[{'url': 'https://vovgiaothong.vn/newsaudio/dung-de-mua-euro-thanh-canh-bac-d39585.html', 'content': 'Tuy nhiên, cùng với không khí thể thao sôi động, tệ nạn cá độ bóng, nhất là cá cược online đã bắt đầu nhức nhối dần lên trong những ngày qua. Và cũng không ít người đã lâm vào cảnh nợ nần vì trò “đỏ đen” này.\n\nHiện nay, chỉ cần gõ từ khóa cá cược bóng đá online trên trang tìm kiếm google, ngay lập tức sẽ có hàng loạt thông tin về hội nhóm, nhà cái uy tín hàng đầu hiện ra dày đặc, với lời mời chào tạo sự tò mò, thích thú cho người xem như: cá cược bóng đá ngoài mang đến cho người chơi những trận đấu kịch tính, còn mang về những khoản tiền cược cao, hay rút trả cược sớm mà không cần xác minh, cơ chế an toàn, bảo mật...\n\nHiện các trận đấu diễn ra với tần suất dày đặc cũng là lúc nhiều website cá độ bóng đá nhân cơ hội mở ra tràn lan, quảng bá rầm rộ trên khắp các nền tảng mạng xã hội, từ Facebook tới Zalo, Telegram... và việc tìm kiếm cũng như đăng ký tham gia những hội nhóm này cũng diễn ra khá đơn giản.\n\nQuảng cáo cá cược tràn lan trên các web xem bóng đá lậu.\n\nPhóng viên VOV Giao thông cũng đã thử gọi vào 1 số điện thoại được giới thiệu trên mạng internet, đường dây bên kia là giọng 1 người đàn ông tư vấn tham gia cá cược với lời khẳng định sẽ không để người chơi thất vọng:\n\nBên mình có phải bên tư vấn kèo cược không?\n\nĐúng rồi em.\n\nCách thức tham gia sao?\n\nTức là nó cũng đơn giản, tại vì đối với năng lực và kinh nghiệm của anh thì anh sẽ soi kèo ra cái tỷ lệ nó ăn cao nhất để cho anh em cùng chơi. Ví dụ như cái trận Anh thì đánh trên với tài, anh cũng chỉ mong muốn có duyên với em, anh em mình đồng hành với nhau lâu dài, em tin tưởng anh thì anh cũng không để em phải thất vọng.\n\nNhưng mà cái tỷ lệ thắng thì sao?\n\nCái tỷ lệ thắng thì tại vì cái kèo anh soi ra anh cũng đánh nên em cũng yên tâm. Với cái kinh nghiệm và năng lực của anh thì gọi là cái kèo mở bát thì tỷ lệ thua nó sẽ thấp. Hoặc anh cảm thấy cái kèo không ok thì để anh em mình đánh cái kèo 2 giờ. Cái quan trọng nhất là tổng kết ngày lại phải có lãi cho em.\n\nLợi dụng tâm lý đam mê bóng đá, đặt niềm tin vào các đội tuyển yêu thích và mong muốn có tiền ăn chơi nên nhiều người đã bị lôi kéo tham gia cá độ bóng đá trực tiếp hoặc trên không gian mạng. Mặc dù các chiêu thức không mới nhưng nhiều người vì ham mê cá độ mà sập bẫy, tin vào những "kèo ngon" mà các đối tượng chiêu dụ để nạp vào tài khoản với hy vọng đổi đời để rồi phải “vỡ mộng” với trò đỏ đen.\n\nNhững lời mời chào tham gia cá cược trên facebook.\n\nCó công việc đang ổn định, anh nhưng những ngày qua, anh Phương (ngụ TP.Thủ Đức) phải chạy xe công nghệ buổi tối để kiếm thêm thu nhập nhằm trả nợ. Nguyên nhân do mùa Euro vừa khai cuộc, anh thường xuyên tụ tập bạn bè rồi “say mê” tham gia cá độ bóng đá khi nào không hay.\n\nBan đầu cũng chỉ đơn giản là một chầu nhậu hay những bữa ăn sáng, dần dần anh cá cược ngày càng cao hơn. Theo chỉ dẫn, anh Phương bắt đầu tham gia cá độ trên mạng. Càng đánh càng ham, số tiền đặt cược mỗi trận của anh càng cao:\n\n“Chơi thì dễ, ai cũng chơi được hết, lúc đầu nạp 500 rồi nạp tiếp 5 triệu. Tội phạm trộm cắp, cướp của giết người, thậm chí là hành vi tự tử cũng theo đó gia tăng, trở thành nối nhức nhối sau mỗi mùa bóng lăn.', 'labeled_pos': [{'từ': 'tuy_nhiên', 'loại từ': 'N'}, {'từ': 'với', 'loại từ': 'V'}], 'extract_content': [{'từ khóa': 'bóng_đá', 'loại từ': 'N', 'điểm số': 0.42}, {'từ khóa': 'cá_độ', 'loại từ': 'V', 'điểm số': 0.32}, {'từ khóa': 'cá_cược', 'loại từ': 'V', 'điểm số': 0.26}, {'từ khóa': 'tham_gia', 'loại từ': 'V', 'điểm số': 0.26}, {'từ khóa': 'kèo', 'loại từ': 'N', 'điểm số': 0.22}], 'cosine_degree': 0.0}]


for item in search_info_data:
    cursor.execute('''
    INSERT INTO search_info (keywords, access_time, completed)
    VALUES (?, ?, ?)
    ''', (','.join(item["keyword"]), item["access_time"], item["completed"]))


for item in search_details_data :
    cursor.execute('''
    INSERT INTO search_details (
        search_info_id, 
        link, 
        title, 
        content, 
        content_processed, 
        keywords_extracted, 
        confidence_level
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (1, item["url"], item.get("title", ""), item["content"], item.get("content_processed", ""), json.dumps(item.get("extract_content", [])), item.get("cosine_degree", 0.0)))

conn.commit()


cursor.execute('SELECT * FROM search_info')
search_info_rows = cursor.fetchall()

cursor.execute('SELECT * FROM search_details')
search_details_rows = cursor.fetchall()

print(search_info_rows, search_details_rows)
