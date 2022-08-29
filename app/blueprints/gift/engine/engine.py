from .types import GroupGift, MoneyGift
from .error import GiftNotFound


class GiftEngine:
    COLLECTIONS = [
        GroupGift,
        MoneyGift
    ]

    @staticmethod
    def get_from_models(model):
        for gift in GiftEngine.COLLECTIONS:
            if gift.get_technical_name() == model.technical_name:
                return gift.get_from_model(model)
        raise GiftNotFound()
