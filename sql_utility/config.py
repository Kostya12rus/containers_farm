import threading

from .sqlite_manager import sql_manager
from typing import Callable, Any, Dict, List


def make_property(key_name: str, type_value: type = str, default_return=None):
    """
    Создаёт свойство для класса с возможностью чтения и записи значения в базу данных.

    Args:
        key_name (str): Ключевое имя для извлечения или записи в базу данных.
        type_value (type): Ожидаемый тип данных значения.
        default_return (str | None): Значение, которое будет возвращено, если значение в базе данных отсутствует.

    Returns:
        property: Свойство для класса с методами getter и setter.
    """

    def getter(self):
        """Метод для получения значения из базы данных."""
        value = sql_manager.get_setting(key_name)
        # Если значение существует, возвращаем его, иначе возвращаем значение по умолчанию
        return value if value is not None else default_return

    def setter(self, value):
        """Метод для записи значения в базу данных."""
        # Если значение соответствует ожидаемому типу, сохраняем его в базу данных
        if isinstance(value, type_value):
            sql_manager.save_setting(key_name, value)

        # Вызов обратных вызовов, если они существуют
        if hasattr(self, '_callbacks') and key_name in self._callbacks:
            for callback in self._callbacks[key_name]:
                threading.Thread(target=callback, args=(value,), daemon=True).start()

    return property(getter, setter)


class Setting:
    time_period_farm = make_property('time_period_farm', float, 60)
    hide_nickname = make_property('hide_nickname', bool, False)
    hide_avatar = make_property('hide_avatar', bool, False)
    delay_add_money = make_property('delay_add_money', float, 0.1)
    auto_use_roulette = make_property('auto_use_roulette', bool, False)
    abuss_use_roulette = make_property('abuss_use_roulette', bool, True)

    # current_account = make_property('current_account', str, '')
    # faseit_token = make_property('faseit_token', dict, {})

    def __init__(self):
        self._callbacks: Dict[str, List[Callable[[Any], None]]] = {}

    def register_callback(self, key_name: str, callback: Callable[[Any], None]):
        if key_name not in self._callbacks:
            self._callbacks[key_name] = []
        self._callbacks[key_name].append(callback)

    def unregister_callback(self, key_name: str, callback: Callable[[Any], None]):
        if key_name in self._callbacks:
            self._callbacks[key_name].remove(callback)
            if not self._callbacks[key_name]:
                del self._callbacks[key_name]

setting = Setting()
