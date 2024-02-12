"""
Модуль для чтения конфигурационных параметров бота.

Содержит класс:
- Settings: класс для определения конфигурационных параметров.
"""


from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    """
    Класс для определения конфигурационных параметров.

    Определяет параметры:
    - bot_token: токен бота, хранящийся в виде секретной строки.
    - model_config: словарь для настройки чтения параметров из файла .env

    Параметры model_config:
    - env_file: путь к файлу .env, содержащему конфигурацию.
    - env_file_encoding: кодировка файла .env
    """

    bot_token: SecretStr
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


# Создаем экземпляр класса Settings для работы с конфигурацией
config = Settings()
