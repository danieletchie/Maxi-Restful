from db import db

class PlatformModel(db.Model):

    __tablename__ = "platforms"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(50))
    api_key = db.Column(db.String(300), unique=True)
    secret_key = db.Column(db.String(300))
    passphrase = db.Column(db.String(300))

    # bots = db.relationship("BotModel")

    def __init__(self, name, user_id, api_key, secret_key, passphrase):
        self.name = name
        self.user_id = user_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def json(self):
        return {
                "id": self.id,
                "name": self.name,
                "user_id": self.user_id,
                "api_key": self.api_key,
                "secret_key": self.secret_key,
                "passphrase": self.passphrase
                # "bots": [bot.json() for bot in self.bots]
                }
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id = user_id).all()

    @classmethod
    def find_by_name_user_id(cls, name, user_id):
        return cls.query.filter_by(name=name, user_id = user_id).first()

    @classmethod
    def find_by_api_key(cls, api_key):
        return cls.query.filter_by(api_key=api_key).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()