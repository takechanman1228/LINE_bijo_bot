from linebot import db
from linebot import Woman
Woman.query.delete()
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman_test","location_1","location_2","location_3","location_4","location_5","location_6","location_7","location_8","location_9"))
db.session.commit()
