class BaseException(Exception):
    pass


class SynthError(BaseException):
    pass


class ModuleNotInstalled(BaseException):
    def __init__(self, module: str) -> None:
        message = f'Required module "{module}" is not installed.'
        super().__init__(message)
