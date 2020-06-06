from typing import Dict, List, Union

from .base_api import BaseAPIClass


class User(BaseAPIClass):

    def me(self) -> Dict[str, Union[str, int]]:
        """ Получить информацию о текущем пользователе.
        https://github.com/huntflow/api/blob/master/ru/user.md#получение-информации-о-текущем-пользователе

        :return: словарь с информацией о текущем пользователе
        :rtype: Dict[str, Union[str, int]]
        """
        return self.requester.request('me')

    def accounts(self) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        """ Получить список доступных организаций текущего пользователя.
        https://github.com/huntflow/api/blob/master/ru/user.md#получение-информации-о-доступных-организациях

        :return: словарь со списком доступных организаций текущего пользователя
        :rtype: Dict[str, List[Dict[str, Union[str, int]]]]
        """
        return self.requester.request('accounts')
