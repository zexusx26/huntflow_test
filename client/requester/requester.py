from typing import Dict
from urllib import parse

import requests


class RequesterError(Exception):
    pass


class Requester:
    """ Класс-обертка над библиотекой requests. """

    # имя агента пользователя для отладки
    USER_AGENT = 'TestTask/1.0 (test@huntflow.ru)'

    def __init__(self, token: str, api_endpoint: str):
        """ Инициализация класса-обертки.

        :param token: персональный токен
        :type token: str
        :param api_endpoint: точка доступа к АПИ
        :type api_endpoint: str
        """
        self.token = token
        self.api_endpoint = api_endpoint

    def _get_headers(self, headers: Dict[str, str] = None) -> Dict[str, str]:
        """ Обновление словаря заголовков.

        Добавляет в словарь заголовков данные об авторизации (токен) и агенте пользователя.

        :param headers: входной словарь заголовков, defaults to None
        :type headers: dict, optional
        :return: словарь заголовков
        :rtype: dict
        """
        res = {
            'User-Agent': self.USER_AGENT,
            'Authorization': f'Bearer {self.token}'
        }
        if headers:
            res.update(headers)
        return res

    def request(
            self,
            url: str,
            http_method: str = 'GET',
            body: dict = None,
            headers: dict = None,
            files: dict = None,
            **params
        ) -> dict:
        """ Сделать запрос к АПИ.

        :param url: путь для запроса
        :type url: str
        :param http_method: используемый HTTP метод, defaults to 'GET'
        :type http_method: str, optional
        :param body: тело запроса (json), defaults to None
        :type body: dict, optional
        :param headers: заголовки запроса, defaults to None
        :type headers: dict, optional
        :param files: отправляемые файлы, defaults to None
        :type files: dict, optional
        :raises RequesterError: если получен неудовлетворительный статус
        :return: словарь ответа от API
        :rtype: dict
        """
        url = parse.urljoin(self.api_endpoint, url)
        req = requests.request(
            method=http_method,
            url=url,
            headers=self._get_headers(headers),
            json=body,
            params=params,
            files=files
        )
        if not req.ok:
            message = f'Client get not ok status code "{req.status_code}"\n' + \
            f'Returned content: {req.content.decode()}\n' + \
            f'Sended headers: {dict(req.request.headers)}\n' + \
            f'Sended content: {req.request.body}'
            raise RequesterError(message)
        return req.json()
