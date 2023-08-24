class TooManyExtensions(Exception):
    "Raised when the amount of extensions exceeds 1."


class RecursionError(Exception):
    "Raised when a future recursion issue is detected."


class ExtensionNotFound(Exception):
    "Raised when extention is not found."


class PathIsNotPosixPath(Exception):
    "Raised when path supplied is not of type pathlib.PosixPath"
