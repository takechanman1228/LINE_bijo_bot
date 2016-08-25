from linebot import db
from linebot import Woman, Problem2, User
# Woman.query.delete()
# Problem2.query.delete()
# User.query.delete()

db.create_all()
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/1"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/2"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/3"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/4"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/5"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/6"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/7"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/8"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/9"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/10"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/11"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/12"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/13"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/14"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/15"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/16"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/17"))
db.session.add(Woman("美女モデル","https://translate-application.herokuapp.com/static/woman/18"))

db.session.commit()


db.session.add(Problem2('朝食はごはん派?', 1))
db.session.add(Problem2('カフェが好き？', 1))
db.session.add(Problem2('スポーツする？', 0))
db.session.commit()
