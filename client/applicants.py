from typing import Dict, List, Union

from .base_api import BaseAPIClass


class Applicants(BaseAPIClass):

    def add(self, account_id: str, last_name: str, first_name: str, **kwargs) -> Dict[str, Union[int, str, List[Dict[str, int]]]]:
        """ Добавить кандидата в базу.

        https://github.com/huntflow/api/blob/master/ru/applicants.md#добавление-кандидата-в-базу

        Остальные именованные параметры в соответствие с документацией.

        :param account_id: идентификатор организации
        :type account_id: str
        :param last_name: фамилия
        :type last_name: str
        :param first_name: имя
        :type first_name: str
        :return: [description]
        :rtype: Dict[str, Union[int, str, List[Dict[str, int]]]]
        """
        # обязательные поля
        body = {
            'last_name': last_name,
            'first_name': first_name
        }
        # опциональные поля
        for field in (
            'middle_name',
            'phone',
            'email',
            'position',
            'company',
            'money',
            'birthday_day',
            'birthday_month',
            'birthday_year',
            'photo',
            'externals'
        ):
            value = kwargs.get(field)
            if value is not None:
                body[field] = value
        # URL
        url = f'account/{account_id}/applicants'
        return self.requester.request(url, http_method='POST', body=body)

    def add_to_vacancy(
            self,
            account_id: str,
            applicant_id: str,
            vacancy: int,
            status: int,
            **kwargs
        ) -> Dict[str, Union[int, str]]:
        """ Добавить кандидата на вакансию.

        https://github.com/huntflow/api/blob/master/ru/applicants.md#добавление-кандидата-на-вакансию

        Остальные именованные параметры в соответствие с документацией.

        :param account_id: идентификатор организации
        :type account_id: str
        :param applicant_id: идентификатор кандидата
        :type applicant_id: str
        :param vacancy: идентификатор вакансии
        :type vacancy: int
        :param status: этап подбора
        :type status: int
        :return: [description]
        :rtype: Dict[str, Union[int, str]]
        """
        # обязательные поля
        body = {
            'vacancy': vacancy,
            'status': status
        }
        # опциональные поля
        for field in (
            'comment',
            'files',
            'rejection_reason',
            'fill_quota'
        ):
            value = kwargs.get(field)
            if value is not None:
                body[field] = value
        # URL
        url = f'account/{account_id}/applicants/{applicant_id}/vacancy'
        return self.requester.request(url, http_method='POST', body=body)
