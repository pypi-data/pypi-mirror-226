from enum import Enum


class BuildTypeEnum(str, Enum):
    BREW = "BREW"
    KOJI = "KOJI"
    CENTOS = "CENTOS"
    APP_INTERFACE = "APP_INTERFACE"
    # This is a temporary tweak to accept empty Enum
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
