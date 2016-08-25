from linebot import db
from linebot import Woman
db.create_all()
db.session.add(Woman('朝食はごはん派?', 1))
db.session.commit()
