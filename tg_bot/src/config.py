from pydantic import BaseModel

import yaml
import os


class TGBotConfig(BaseModel):
    """
    Конфигурация бота ТГ
    """
    token: str


class YSpeechKitConfig(BaseModel):
    """
    Конфигурация подключения к SpeechKit
    """
    cloud_folder: str
    api_key: str


class CustomGPTConfig(BaseModel):
    """
    Конфигурация подключения к GPT
    """
    api_key: str


class Config(BaseModel):
    """
    Настройки приложения
    """
    tg_bot_config: TGBotConfig
    speechkit_config: YSpeechKitConfig
    custom_gpt_config: CustomGPTConfig


def load_config() -> Config:
    """
    Чтение конфигурации
    """
    config_file: dict
    with open(f'{os.path.dirname(__file__)}/config.yaml', 'r') as f:
        config_file = yaml.safe_load(f)

    return Config(**config_file)
