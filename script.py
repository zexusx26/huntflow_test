import argparse
import json
import os
from logging import DEBUG, Logger, StreamHandler, Formatter
from sys import stdout

from client import Client
from reader import FullNameField, Salary, StatsField, StringField, XLSXReader
from utils import find_resume, update_applicant_from_resume

#################
# ИНИЦИАЛИЗАЦИЯ #
#################

# парсинг аргументов командной строки
arg_parser = argparse.ArgumentParser(
    description='Candidate loader.'
)
arg_parser.add_argument(
    'token',
    help='Personal token'
)
arg_parser.add_argument(
    'database_path',
    help='Path to database'
)
args = arg_parser.parse_args()
base_path, _ = os.path.split(args.database_path)

# инициализация логгера
logger = Logger('Applicants loader', DEBUG)
fmt = '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s'
formatter = Formatter(fmt)
handler = StreamHandler(stdout)
handler.setFormatter(formatter)
handler.setLevel(DEBUG)
logger.addHandler(handler)

logger.debug('Логгер инициализирован. Загружаю конфигурации, инициализирую чтеца БД и клиента АПИ.')

# загрузка конфига
CFG_FP = 'config.json'
with open(CFG_FP, 'rt') as file:
    config = json.load(file)

# инициализация чтеца и клиента
fields = (
    StringField('vacancy'),
    FullNameField('full name'),
    Salary('money', 'руб'),
    StringField('comment'),
    StatsField('status')
)
reader = XLSXReader(fields)
client = Client(args.token, config['api_endpoint'])

##############################
# ПОЛУЧЕНИЕ ДАННЫХ С СЕРВЕРА #
##############################

logger.debug('Получаю нужные данные с сервера.')

# идентификатор организации
account_id = client.user.accounts()['items'][0]['id']

# словарь вакансий. Ключ - название вакансии, значение - словарь с данными вакансии
vacancies = client.vacancies.get_list(account_id, count=100)['items']
vacancies = {vacancy['position']: vacancy for vacancy in vacancies}

# словарь этапов согласования кандидата. Ключ - название этапа, значение - словарь с данными этапа
statuses = client.directory.statuses(account_id)['items']
statuses = {statuse['name']: statuse for statuse in statuses}

# получение строки, с которой будет начато чтение
status_file = os.path.join(base_path, 'status.txt')
if os.path.exists(status_file):
    with open(status_file) as file:
        row_number = int(file.read())
else:
    row_number = 1

# основной скрипт
logger.debug('Начинаю работу с кандидатами.')
try:
    with reader.open(args.database_path):

        while True:

            # чтение данных о кандидате
            logger.debug(f'Работа с кандидатом №{row_number}.')
            candidate = reader.read_row(row_number)
            if not candidate:
                logger.info('Данные о кандидате не получены, похоже, все кандидаты загружены. Завершаю работу.')
                break
            logger.debug('Из БД получены данные о кандидате.')

            # получаем вакансии и статус
            vacancy = vacancies.get(candidate['vacancy'])
            if vacancy is None:
                logger.warning('Ошибка при опеределении вакансии кандидата, кандидат не будет зарегистрирован на вакансию.')
            else:
                logger.debug('Получены данные о вакансии кандидата.')

            status = statuses.get(candidate['status'])
            if status is None:
                logger.warning('Ошибка при опеределении статуса кандидата, кандидат не будет зарегистрирован на вакансию.')
            else:
                logger.debug('Получены данные о статусе кандидата.')

            # создаем словарь персональных данных
            applicant = {
                'last_name': candidate['last_name'],
                'first_name': candidate['first_name'],
                'money': candidate['money']
            }
            if 'middle_name' in candidate:
                applicant['middle_name'] = candidate['middle_name']

            # получаем файл с резюме и загружаем (запрашиваем парсинг)
            resume_fp = find_resume(
                base_path,
                candidate['vacancy'],
                applicant['last_name'],
                applicant['first_name'],
                applicant.get('middle_name')
            )
            if resume_fp is None:
                logger.warning('Ошибка при получении файла резюме, резюме не будет загружено.')
                resume = {}
            else:
                resume = client.file.upload(account_id, resume_fp)
                logger.debug('Загружено резюме кандидата.')

            # обновляем данные кандидата из БД данными из резюме
            update_applicant_from_resume(applicant, resume)

            # добавляем кандидата в базу
            applicant = client.applicants.add(account_id, **applicant)
            logger.debug('Кандидат добавлен на сервер.')

            if status and vacancy:

                # добавляем кандидата на вакансию
                applicant_to_vacancy_data = {
                    'vacancy': vacancy['id'],
                    'status': status['id'],
                    'comment': candidate['comment'],
                    'files': [{'id': resume['id']}]
                }
                request = client.applicants.add_to_vacancy(account_id, applicant['id'], **applicant_to_vacancy_data)
                logger.debug(f'Кандидат зарегистрирован на вакансию.')

            row_number += 1

# запоминаем строку, на которой остановились
finally:
    with open(status_file, 'wt') as file:
        file.write(str(row_number))
