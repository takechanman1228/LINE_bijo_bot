from linebot import db
from linebot import Woman, Problem2, User
# Woman.query.delete()
# Problem2.query.delete()
# User.query.delete()

db.create_all()
db.session.add(Woman("美女モデル","https://internship2016.herokuapp.com/static/woman_test","location_1","location_2","location_3","location_4","location_5","location_6","location_7","location_8","location_9"))
db.session.commit()


db.session.add(Problem2('朝食はごはん派?', 1))
db.session.add(Problem2('カフェが好き？', 1))
db.session.add(Problem2('スポーツする？', 0))
db.session.commit()
