from . import db

class SearchInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keywords = db.Column(db.Text)
    access_time = db.Column(db.Text)
    completed = db.Column(db.Boolean)

class SearchDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_info_id = db.Column(db.Integer, db.ForeignKey('search_info.id'))
    link = db.Column(db.Text)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    content_processed = db.Column(db.Text)
    keywords_extracted = db.Column(db.Text)
    confidence_level = db.Column(db.Float)
