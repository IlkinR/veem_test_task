class InvalidInputFormat(Exception):
    """ Exception class for handling user input in terminal"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class SecondsSinceUnixNotEven(Exception):
    """ Exception class for handling errors related to total seconds passed since unix time (January 01 1970)."""

    def __init__(self, passed_seconds: int) -> None:
        self.passed_seconds = passed_seconds

    def __repr__(self) -> repr:
        return '{exception}: {seconds} % 2 == 0, since remainder is {remainder}'.format(
            exception=self.__class__.__name__,
            seconds=self.passed_seconds,
            remainder=self.passed_seconds % 2
        )


class SystemRAMLessThanOneGB(Exception):
    """ Exception class for handling errors related to RAM of system of the user """

    def __init__(self, system_ram: int) -> None:
        self.system_ram = system_ram

    def __repr__(self) -> str:
        return '{exception}: {seconds} Gb < 1 Gb '.format(
            exception=self.__class__.__name__,
            seconds=self.system_ram,
        )