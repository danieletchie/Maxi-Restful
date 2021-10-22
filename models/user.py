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
        