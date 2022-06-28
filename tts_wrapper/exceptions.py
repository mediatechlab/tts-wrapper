class BaseException(Exception):
    pass


class SynthError(BaseException):
    pass


class ModuleNotInstalled(BaseException):
    def __init__(self, module: str) -> None:
        message = f'Required module "{module}" is not installed.'
        super().__init__(message)


class UnsupportedFileFormat(BaseException):
    def __init__(self, format: str, engine: str) -> None:
        message = f'Format "{format}" is not supported by engine {engine}.'
        super().__init__(message)
