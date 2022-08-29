from typing import List

from .badge import Badge


class BadgeCollections:
    COLLECTIONS = [
        Badge("legend", "Легендарный игрок",
              "{user.bukkit.nickname} является легендарным и почётным игроком проекта",
              "fad fa-fire-alt fa-1x", "#e76f51"),

        Badge("verification", "Верификация",
              "Профиль пользователя {user.bukkit.nickname} подтверждён администрацией проекта",
              "fas fa-badge-check fa-1x", "#0096c7"),

        Badge("partner", "Партнёр",
              "Пользователь {user.bukkit.nickname} является партнёром проекта",
              "fas fa-infinity fa-1x", "#0096c7"),

        Badge("partner_developer", "Разработчик партнёрского софта",
              "{user.bukkit.nickname} является разработчиком партнёрского приложения",
              "fad fa-meteor fa-1x", "#0096c7"),

        Badge("top_worker", "Почетный участник команды проекта",
              "{user.bukkit.nickname} почетный участник команды Plazmix",
              "fad fa-khanda fa-1x", "#9368E9"),

        Badge("worker", "Участник команды проекта",
              "{user.bukkit.nickname} является частью команды Plazmix",
              "fad fa-hammer fa-1x", "#9368E9"),

        Badge("plus_sub", "Подписка +",
              "{user.bukkit.nickname} самый крутой игрок с подпиской плюс",
              "fad fa-star-shooting fa-1x", "#FF00FF")
        ]

    @staticmethod
    def get_all() -> List[Badge]:
        return BadgeCollections.COLLECTIONS

    @staticmethod
    def get_from_technical_name(name: str) -> Badge:
        badges = BadgeCollections.get_all()
        for badge in badges:
            if name.lower() == badge.technical_name.lower():
                return badge
        raise ValueError("unknown badge")
