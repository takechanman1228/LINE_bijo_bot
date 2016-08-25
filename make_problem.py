from linebot import db
from linebot import Problem2
db.create_all()
db.session.add(Problem2('朝食はごはん派?', 1))
db.session.add(Problem2('カフェが好き？', 1))
db.session.add(Problem2('スポーツする？', 0))
db.session.commit()
