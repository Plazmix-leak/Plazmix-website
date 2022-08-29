from flask import g

from app.blueprints.store.engine.collection._abstract_collection import AbstractStoreCollection
from app.blueprints.store.engine.products.iml.group import GroupStoreProduct
from app.core.permissions.groups import PermissionGroups
from app.core.user import User


class GroupStoreCollection(AbstractStoreCollection):
    STAR = GroupStoreProduct(group=PermissionGroups.STAR, technical_name="STAR", name="STAR",
                             html="star.html",
                             image="STAR.png",
                             price=199, sale_percent=0)

    COSMO = GroupStoreProduct(group=PermissionGroups.COSMO, technical_name="COSMO", name="COSMO",
                              html="cosmo.html",
                              image="COSMO.png",
                              price=499, sale_percent=0)

    GALAXY = GroupStoreProduct(group=PermissionGroups.GALAXY, technical_name="GALAXY", name="GALAXY",
                               html="galaxy.html",
                               image="GALAXY.png",
                               price=999, sale_percent=0)

    UNIVERSE = GroupStoreProduct(group=PermissionGroups.UNIVERSE, technical_name="UNIVERSE", name="UNIVERSE",
                                 html="universe.html",
                                 image="UNIVERSE.png",
                                 price=2999, sale_percent=0)

    LUXURY = GroupStoreProduct(group=PermissionGroups.LUXURY, technical_name="LUXURY", name="LUXURY",
                               html="luxury.html",
                               image="LUXURY.png",
                               price=9999, sale_percent=0)

    @classmethod
    def get_final_price(cls, select_product):
        user: User = g.user

        group_product: GroupStoreProduct = select_product

        if user is None:
            return group_product.price

        user_group = user.permission_group

        if group_product.group.value <= user_group:
            return -1

        try:
            user_pay_group = cls.get_from_technical_name(user_group.get_technical_name)
        except ValueError:
            return group_product.price

        current_price = group_product.price - user_pay_group.value.price
        return current_price
