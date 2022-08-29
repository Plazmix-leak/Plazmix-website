from enum import Enum

from .type import BukkitAchievementSection


class BukkitAchievement:
    def __init__(self, description: str, section: BukkitAchievementSection, multilevel: bool = False):
        self._description = description
        self._section = section
        self._multilevel = multilevel

    @property
    def title(self):
        if self._section == BukkitAchievementSection.GLOBAL:
            return "Глобальная"
        elif self._section == BukkitAchievementSection.SECRET:
            return "Секретная"
        elif self._section == BukkitAchievementSection.GAME_BED_WARS:
            return "BedWars"
        elif self._section == BukkitAchievementSection.GAME_SKY_WARS:
            return "SkyWars"
        else:
            return "Неизвестная"

    @property
    def description(self) -> str:
        if self._section == BukkitAchievementSection.SECRET:
            return "Секретная ачивка"
        return self._description

    @property
    def section(self) -> BukkitAchievementSection:
        return self._section

    @property
    def multilevel(self) -> bool:
        return self._multilevel


class AchievementCollection(Enum):
    FIRST_JOIN = BukkitAchievement("Добро пожаловать", BukkitAchievementSection.GLOBAL)
    FIRST_MESSAGE = BukkitAchievement("Любитель поговорить", BukkitAchievementSection.GLOBAL)
    FIRST_FRIEND = BukkitAchievement("Дружба - это сила", BukkitAchievementSection.GLOBAL)
    FRIENDS = BukkitAchievement("Друзья на все времена", BukkitAchievementSection.GLOBAL)
    FIRST_CHEST = BukkitAchievement("Ценитель древностей", BukkitAchievementSection.GLOBAL)
    FOREVER_ALONE = BukkitAchievement("Forever Alone", BukkitAchievementSection.GLOBAL)
    STAR = BukkitAchievement("Местная звездочка", BukkitAchievementSection.GLOBAL)
    COSMO = BukkitAchievement("Лучший из лучших", BukkitAchievementSection.GLOBAL)
    GALAXY = BukkitAchievement("Очень важная персона", BukkitAchievementSection.GLOBAL)
    UNIVERSE = BukkitAchievement(".. all inclusive..", BukkitAchievementSection.GLOBAL)
    YOUTUBE = BukkitAchievement("Свет, камера, мотор, начали!", BukkitAchievementSection.GLOBAL)
    COINS_KEEPER = BukkitAchievement("Держатель казны", BukkitAchievementSection.GLOBAL, True)
    EXPERIENCE_KEEPER = BukkitAchievement("Хранитель опыта", BukkitAchievementSection.GLOBAL, True)
    PARKOUR = BukkitAchievement("Попрыгунчик", BukkitAchievementSection.GLOBAL)
    DROPPER = BukkitAchievement("Точное попадание", BukkitAchievementSection.GLOBAL)
    GIFTS = BukkitAchievement("Время приключений", BukkitAchievementSection.GLOBAL)
    TUTORIAL = BukkitAchievement("Предисловие", BukkitAchievementSection.GLOBAL)
    BEST_PROJECT = BukkitAchievement('Любимый проект', BukkitAchievementSection.SECRET)
    HACKER = BukkitAchievement('Прирожденный хацкер', BukkitAchievementSection.SECRET)
    ROAD_TO_HELL = BukkitAchievement('Бездна', BukkitAchievementSection.SECRET)
    ROAD_TO_SPACE = BukkitAchievement('Почти космонавт', BukkitAchievementSection.SECRET)
    DID_IT = BukkitAchievement('Автограф создателя', BukkitAchievementSection.SECRET)
    YOUTUBE_PLUS = BukkitAchievement('Super Star', BukkitAchievementSection.SECRET)
    STAFF = BukkitAchievement('Часть великолепной команды', BukkitAchievementSection.SECRET)

    SKYWARS_KILLS = BukkitAchievement('Небесный убийца', BukkitAchievementSection.GAME_SKY_WARS, True)
    SKYWARS_WINS = BukkitAchievement('Чемпион поднебесья', BukkitAchievementSection.GAME_SKY_WARS, True)
    SKYWARS_CAGES_HOARDER = BukkitAchievement('Коллекционер клеток', BukkitAchievementSection.GAME_SKY_WARS, True)
    SKYWARS_HEADS_HOARDER = BukkitAchievement('Коллекционер голов', BukkitAchievementSection.GAME_SKY_WARS, True)
    SKYWARS_STARS = BukkitAchievement('Звездная личность', BukkitAchievementSection.GAME_SKY_WARS, True)
    SKYWARS_ANGELS_JOURNEY = BukkitAchievement('Проклятое путешествие', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_DRAGON = BukkitAchievement('Дракон Края', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_GOLDEN_APPLE = BukkitAchievement('Золотое яблочко', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_GOTCHA = BukkitAchievement('Нереальное везение', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_KILL_STOLEN = BukkitAchievement('Ассистент', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_LEGENDARY = BukkitAchievement('Легендарный', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_MAX_PERK = BukkitAchievement('На максималках', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_FULL_SOULS_WELL = BukkitAchievement('Коллеционер душ', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_NO_CHEST_CHALLENGE = BukkitAchievement('ПРО-фессионал', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_ENCHANTED = BukkitAchievement('Зачарованный', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_PEACEMAKER = BukkitAchievement('Миротворец', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_SHINY_STAFF = BukkitAchievement('Блестящие доспехи', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_FAST_AND_FURIOUS = BukkitAchievement('Свирепый убийца', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_SNIPER = BukkitAchievement('Лучник', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_SUPER_KILLER = BukkitAchievement('Чудовище на небесах', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_SPEED_RUN = BukkitAchievement('Соник', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_OPEN_CHEST = BukkitAchievement('3; 2; 1; Начали!', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_CORRUPTION_LORD = BukkitAchievement('Проклятый лорд', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_PORTAL_GAME = BukkitAchievement('Игра телепортов?', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_MOB_SPAWNER = BukkitAchievement('Прислужник', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_SOLD_YOUR_SOUL = BukkitAchievement('Проклятая сделка', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_WELL_DESERVED = BukkitAchievement('Отличная подготовка', BukkitAchievementSection.GAME_SKY_WARS)
    SKYWARS_WELL_WELL = BukkitAchievement('Колодец Душ', BukkitAchievementSection.GAME_SKY_WARS)

    BEDWARS_BED_REMOVAL = BukkitAchievement('Крушитель кроватей', BukkitAchievementSection.GAME_BED_WARS, True)
    BEDWARS_KILLER = BukkitAchievement('Ловец снов', BukkitAchievementSection.GAME_BED_WARS, True)
    BEDWARS_ROAD_TO_PRESTIGE = BukkitAchievement('Престижный рост', BukkitAchievementSection.GAME_BED_WARS, True)
    BEDWARS_VICTORY_DANCER = BukkitAchievement('Диванный покровитель', BukkitAchievementSection.GAME_BED_WARS, True)
    BEDWARS_ALCHEMIST = BukkitAchievement('Алхимик', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_ALREADY_OVER = BukkitAchievement('Быстрая игра', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_BOMBER = BukkitAchievement('TNT', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_BUILDER = BukkitAchievement('Строитель', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_CUTTING_IT_CLOSE = BukkitAchievement('Настоящий ловкач', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_DIAMONDS_HOARDER = BukkitAchievement('Блестяшки', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_EMERALDS_HOARDER = BukkitAchievement('Мастер над изумрудом', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_FIRST_BLOOD = BukkitAchievement('Быстрая смерть', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_GEARED_UP = BukkitAchievement('Вооружен на победу', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_WELL_DONE = BukkitAchievement('Когда очень хочется спать..', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_HALF_OF_BEDS = BukkitAchievement('Отлично сработано', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_GUARDS_ROSE = BukkitAchievement('Ржавое корыто', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_LORD_OF_FIRE = BukkitAchievement('Огненный мастер', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_WITHOUT_BED = BukkitAchievement('Кровать для слабаков', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_IRON_PUNCH = BukkitAchievement('Стальная воля', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_ITS_DARK_DOWN_THERE = BukkitAchievement('Вечная темнота', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_MAGIC_MILK = BukkitAchievement('Как Ниндзя', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_MERCILESS = BukkitAchievement('Беспощадный', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_OUT_OF_STOCK = BukkitAchievement('Нет в наличии', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_SHOPPER = BukkitAchievement('Обновка', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_SHOWOFF = BukkitAchievement('На показ', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_SNEAKY_RUSHER = BukkitAchievement('Подлый крушитель', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_SPEEDY_BRIDGER = BukkitAchievement('Самый первый', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_STRATEGIST = BukkitAchievement('Закаленная броня', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_FIRST_WIN = BukkitAchievement('Первая победа', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_CANNOT_DO_THAT = BukkitAchievement('Хорошая попытка', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_CANNOT_TRAP_ME = BukkitAchievement('Слепой унитожитель', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_JUMPER = BukkitAchievement('Попрыгунчик', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_TRICKED = BukkitAchievement('Попался!', BukkitAchievementSection.GAME_BED_WARS)
    BEDWARS_SHOPKEEPER_DAMAGE = BukkitAchievement('Торговец - часть команды', BukkitAchievementSection.GAME_BED_WARS)

    @classmethod
    def get_from_identification(cls, identification: str):
        for element in cls:
            if element.name == identification:
                return element
        raise ValueError("Unknown achievement")
