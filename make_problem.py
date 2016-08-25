from linebot import db
from linebot import Problem2
db.create_all()
db.session.add(Problem2('LINEは渋谷ヒカリエにある', 1))
db.session.add(Problem2('日本で一番高い山は富士山', 0))
db.session.commit()
