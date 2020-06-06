from typing import Dict, List, Union

from .base_api import BaseAPIClass


class Directory(BaseAPIClass):

    def statuses(self, account_id: str) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        """ Получить этапы подбора организации.

        https://github.com/huntflow/api/blob/master/ru/dicts.md#vacancy_statuses

        :param account_id: идентификатор организации
        :type account_id: str
        :return: список этапов подбора организаций
        :rtype: Dict[str, Union[int, List[Dict[str, Union[str, int]]]]]
        """
        url = f'account/{account_id}/vacancy/statuses'
        return self.requester.request(url)

    def sources(self, account_id: str) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        """ Получить список источников резюме.

        https://github.com/huntflow/api/blob/master/ru/dicts.md#источники-резюме

        :param account_id: идентификатор организации
        :type account_id: str
        :return: список источников резюме
        :rtype: Dict[str, List[Dict[str, Union[str, int]]]]
        """
        url = f'/account/{account_id}/applicant/sources'
        return self.requester.request(url)
