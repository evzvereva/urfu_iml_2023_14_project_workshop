import typing
from typing import List

from pydantic import BaseModel


class SimpleMessageHistory(BaseModel):
    role: str
    message: str


class SimpleUserState(BaseModel):
    user_id: int
    user_name: str
    voice: bool
    messages: list


class UserState:
    __users = {}

    def init_user(self, user_id: int, user_name: str) -> None:
        if user_id in self.__users:
            return

        self.__users[user_id] = SimpleUserState(
            user_id=user_id,
            user_name=user_name,
            voice=False,
            messages=list()
        )

    def toogle_user_voice_out(self, user_id: int) -> bool:
        if user_id not in self.__users:
            raise Exception(f'Пользователь {user_id} не найден')

        if self.__users[user_id].voice:
            self.__users[user_id].voice = False
        else:
            self.__users[user_id].voice = True

        return self.__users[user_id].voice

    def get_user_voice_out(self, user_id: int) -> bool:
        if user_id not in self.__users:
            raise Exception(f'Пользователь {user_id} не найден')

        return self.__users[user_id].voice

    def clear_history(self, user_id: int) -> None:
        if user_id not in self.__users:
            raise Exception(f'Пользователь {user_id} не найден')

        self.__users[user_id].messages = list()

    def add_history(self, user_id: int, history: SimpleMessageHistory) -> None:
        if user_id not in self.__users:
            raise Exception(f'Пользователь {user_id} не найден')

        self.__users[user_id].messages.append(history)

    def get_history(self, user_id: int) -> list[SimpleMessageHistory]:
        if user_id not in self.__users:
            raise Exception(f'Пользователь {user_id} не найден')

        return self.__users[user_id].messages
