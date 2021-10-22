from db import db

class UserModel(db.Model):

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.BigInteger())
    password = db.Column(db.String(250))
    status = db.Column(db.String(100))
    platforms = db.relationship("PlatformModel")

    def __init__(self, name, email, phone, password, status):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.status = status

    def json(self):
        return {
                "id": self.id,
                "name": self.name, 
                "email": self.email, 
                "phone": self.phone,
                "status": self.status,
                "platforms": [platform.json() for platform in self.platforms]
                }

    @classmethod           
    def find_by_id(cls, _id):
        return UserModel.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return UserModel.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class PlatformModel(db.Model):

    __tablename__ = "platforms"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    platform = db.Column(db.String(50))
    api_key = db.Column(db.String(300), unique=True)
    secret_key = db.Column(db.String(300))
    passphrase = db.Clolumn(db.String(300))

    bots = db.relationship("BotModel")

    def __init__(self, user_id, platform, api_key, secret_key, passphrase):
        self.user_id = user_id
        self.platform = platform
        self.api_key = api_key
        self.secret_key = secret_key
        self.passpharse = passphrase

    def json(self):
        return {
                "id": self.id,
                "user_id": self.user_id,
                "platform": self.platform,
                "api_key": self.api_key,
                "secret_key": self.secret_key,
                "passphrase": self.passphrase,
                "bots": [bot.json() for bot in self.bots]
                }
    
    @classmethod
    def find_by_id(cls, _id):
        return PlatformModel.query.filter_by(id = _id).first()

    @classmethod
    def find_by_userId_platform(cls, user_id, platform):
        return PlatformModel.query.filter_by(user_id = user_id,platform = platform)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit(self)

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()