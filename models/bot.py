from db import db

class BotModel(db.Model):

    __tablename__ = "bots"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platforms.id"))
    pairs = db.Column(db.String())
    strategy = db.Column(db.String())
    current_price = db.Column(db.Float(25))
    first_grid = db.Column(db.Float(25))
    grid_int = db.Column(db.Float(25))
    average_margin = db.Column(db.Float(25))
    current_margin = db.Column(db.Float(25))
    amount = db.Column(db.Float(50))
    quantity = db.Column(db.Float(50))
    sell_margin = db.Column(db.Float(25))
    trades = db.Column(db.Integer())
    renew = db.Column(db.Integer())
    status = db.Column(db.String(200))
    time = db.Column(db.Float(25))

    def __init__(self, platform_id, pairs, strategy, current_price,sell_margin,status, time,amount,quantity, first_grid=0, grid_int=0, average_margin=0, current_margin=0,trades=0,renew=0):
        self.platform_id = platform_id
        self.pairs = pairs
        self.strategy = strategy
        self.current_price = current_price
        self.first_grid = first_grid
        self.grid_int = grid_int
        self.average_margin = average_margin
        self.current_margin = current_margin
        self.amount = amount
        self.quantity = quantity
        self.sell_margin = sell_margin
        self.trades = trades
        self.renew = renew
        self.status = status
        self.time = time

    def json(self):
        return {
                "id": self.id,
                "platform_id": self.platform_id,
                "strategy": self.strategy,
                "pairs": self.pairs,
                "current_price": self.current_price,
                "first_grid": self.first_grid,
                "grid_int": self.grid_int,
                "average_margin": self.average_margin,
                "current_margin": self.current_price,
                "amount": self.amount,
                "quantity": self.quantity,
                "sell_margin": self.sell_margin,
                "trades": self.trades,
                "renew": self.renew,
                "status": self.status,
                "time": self.time
                # "bots": [bot.json() for bot in self.bots]
                }
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()