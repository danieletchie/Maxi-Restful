from db import db

class OrderModel(db.Model):

    __tablename__ = "orders"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey("bots.id"))
    pairs = db.Column(db.String())
    order_id = db.Column(db.String(200))
    side = db.Column(db.String(100))
    status = db.Column(db.String(100))
    time = db.Column(db.Float(25))

    def __init__(self,  bot_id, pairs, order_id, side,status, time):
        self.bot_id = bot_id
        self.pairs = pairs
        self.order_id = order_id
        self.side = side
        self.status = status
        self.time = time

    def json(self):
        return {
                "id": self.id,
                "bot_id": self.bot_id,
                "pairs": self.pairs,
                "side": self.side,
                "order_id": self.order_id,
                "status": self.status,
                "time": self.time
                }
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()