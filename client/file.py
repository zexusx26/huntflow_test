import json
import subprocess
from os import path
from typing import Dict, List, Union
from urllib import parse as urllib_parse

from .base_api import BaseAPIClass


class File(BaseAPIClass):

    def upload(self, account_id: str, fp: str, parse: bool = True) -> Dict[str, Union[str, int, Dict[str, Union[str, int, List[str], Dict[str, Union[str, int]]]]]]:
        """ Загрузить файл.
        https://github.com/huntflow/api/blob/master/ru/upload.md#загрузка-и-распознавание-файлов

        :param account_id: идентификатор организации
        :type account_id: str
        :param fp: путь до файла
        :type fp: str
        :param parse: распознать поля, defaults to True
        :type parse: bool, optional
        :return: ответ на запрос
        :rtype: Dict[str, Union[str, int, Dict[str, Union[str, int, List[str], Dict[str, Union[str, int]]]]]]
        """
        url = f'account/{account_id}/upload'
        return self.upload_file(fp, url, parse)

    def upload_file(self, fp: str, url: str, parse: bool = True) -> Dict[str, Union[str, int, Dict[str, Union[str, int, List[str], Dict[str, Union[str, int]]]]]]:
        """ Загрузить файл на сервер.

        Читерский способ, использует curl в подпроцессе.

        :param fp: путь до файла
        :type fp: str
        :param url: путь для запроса
        :type url: str
        :param parse: True, чтобы парсить файл, иначе False, defaults to True
        :type parse: bool, optional
        :return: ответ на запрос
        :rtype: Dict[str, Union[str, int, Dict[str, Union[str, int, List[str], Dict[str, Union[str, int]]]]]]
        """
        url = urllib_parse.urljoin(self.requester.api_endpoint, url)
        if parse:
            parse = 'true'
        else:
            parse = 'false'
        command = [
            'curl', '-s', '-X', 'POST',
            '-H', 'User-Agent: {}'.format(self.requester.USER_AGENT),
            '-H', 'Content-Type: multipart/form-data',
            '-H', 'X-File-Parse: {}'.format(parse),
            '-H', 'Authorization: Bearer {}'.format(self.requester.token),
            '-F', 'file=@{}'.format(fp),
            url
        ]
        popen = subprocess.Popen(command, stdout=subprocess.PIPE)
        data = popen.stdout.read()
        if popen.poll() is None:
            popen.terminate()
            popen.wait(1)
            popen.kill()
            popen.wait(1)
        return json.loads(data)
