from enum import Enum


class V1BuildsListBuildType(str, Enum):
    APP_INTERFACE = "APP_INTERFACE"
    BREW = "BREW"
    CENTOS = "CENTOS"
    KOJI = "KOJI"
    # This is a temporary tweak to accept empty Enum
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
