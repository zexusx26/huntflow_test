from typing import Dict, List, Union

from .base_api import BaseAPIClass


class Vacancies(BaseAPIClass):

    def get_list(
            self,
            account_id: str,
            mine: bool = False,
            opened: bool = False,
            count: int = 1,
            page: int = 1
        ) -> Dict[str, Union[int, List[Dict[str, Union[str, int]]]]]:
        """ Получить список вакансий.

        https://github.com/huntflow/api/blob/master/ru/vacancies.md#получение-списка-вакансий

        :param account_id: идентификатор организации
        :type account_id: str
        :param mine: вернуть вакансии, над которыми работает текущий пользователь, defaults to False
        :type mine: bool, optional
        :param opened: вернуть только открытые вакансии, defaults to False
        :type opened: bool, optional
        :param count: число объектов на странице, defaults to 1
        :type count: int, optional
        :param page: номер страницы, defaults to 1
        :type page: int, optional
        :return: список вакансий
        :rtype: Dict[str, Union[int, List[Dict[str, Union[str, int]]]]]
        """
        url = f'/account/{account_id}/vacancies'
        body = {}
        if mine:
            body['mine'] = True
        if opened:
            body['opened'] = True
        return self.requester.request(url, body=body, count=count, page=page)
