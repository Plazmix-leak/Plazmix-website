class HierarchyType:
    def __init__(self, hierarchy: int,  technical_signature: str, signature: str, **kwargs) -> None:
        self._signature = signature
        self._technical_name = technical_signature
        self._hierarchy = hierarchy
        for kw in kwargs.keys():
            self.__dict__[kw] = kwargs[kw]
        # self.__dict__ += kwargs

    @property
    def name(self):
        return self._signature

    @property
    def can_hierarchy_type(self):
        return True

    @property
    def get_technical_name(self):
        return self._technical_name

    @property
    def get_id(self):
        return self._hierarchy

    def __str__(self):
        return self._signature

    def __int__(self):
        return self._hierarchy

    def __float__(self):
        return float(self._hierarchy)

    def __eq__(self, other):
        return self._hierarchy == other.get_id

    def __ne__(self, other):
        return self._hierarchy != other.get_id

    def __gt__(self, other):
        return self._hierarchy > other.get_id

    def __lt__(self, other):
        return self._hierarchy < other.get_id

    def __ge__(self, other):
        return self._hierarchy >= other.get_id

    def __le__(self, other):
        return self._hierarchy <= other.get_id
