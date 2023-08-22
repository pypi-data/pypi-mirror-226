from enum import Enum, EnumMeta


class FormatMeta(EnumMeta):
    def __contains__(cls, item):
        return item in cls.__members__.values()


class Format(int, Enum, metaclass=FormatMeta):
    STANDARD = 1,
    HALF_PPR = 2,
    PPR = 3
