class BadAuthRequest(Exception):
    message = "No key or wrong key format"


class KeyNotFound(Exception):
    message = "Key not found, disabled or expired"

