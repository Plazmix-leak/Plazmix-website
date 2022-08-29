from app import db
from app.core.user import User


class StoreProduct(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    img = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=0)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, default=100)
    type = db.Column(db.Enum('donate', 'coins'))
    data = db.Column(db.JSON)
    action_percent = db.Column(db.Integer, default=0)

    @property
    def can_action(self):
        return True if self.action_percent > 0 else False

    @property
    def final_price(self):
        sale = self.action_percent / 100
        final_sale = 1 - sale
        return self.price * final_sale

    @classmethod
    def get_from_id(cls, identification: int):
        r = StoreProduct.query.filter(StoreProduct.id == identification).first()
        if r is None:
            raise ValueError("Unknown product")
        return r

    @staticmethod
    def get_all_active_products():
        return StoreProduct.query.filter(StoreProduct.active == 1).all()

    def init_give(self, user: User):
        from app.task.bukkit_server import give_group
        data = self.data

        if not data:
            raise RuntimeError("Product data is empty")

        group = self.data.get("group", None)
        if group is None:
            raise RuntimeError("Product unknown group_name")

        give_group.apply_async(
                kwargs={"user_uuid": user.uuid, "group": group},
                ignore_result=True)

