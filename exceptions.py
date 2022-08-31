class GetException(Exception):
    """Исключение для проблем доступа."""
    pass


class UnavailableException(GetException):
    """Исключение для неправильного кода доступа."""
    pass


class ParseException(Exception):
    """Исключение для неудачного парсинга."""
    pass


def err_msg(error):
    """Генерация сообщения об ошибке."""
    return f'Сбой в работе программы: {error}'
