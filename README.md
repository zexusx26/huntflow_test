# Скрипт для загрузки базы кандидатов

Переносит базу кандидатов из Экселя и файлов в Хантфлоу, используя [Хантфлоу API](https://github.com/huntflow/api).

## Аргументы командной строки

Скрипт принимает два обязательных аргумента: индивидуальный токен авторизации и путь до загружаемой базы.

## Описание базы

База&nbsp;&mdash; файл Экселя. В директории с базой находятся резюме кандидатов, сгруппированные по директориям, 
названия которых соответствуют названиям вакансий, на которые претендуют кандидаты. Имена файлов резюме начинаются с 
имен соответствующих кандидатов.

## Особенности запуска

При полной обработки кандидата, следующий запуск начинается со следующего кандидата.

## Требования

Для работы скрипт требует **python3** версии не ниже 3.6.9. Необходимые библиотеки перечислены в файле `requirements.txt`. 
Установка библиотек из корня проекта (требует **python3-pip**):

```bash
python3 -m pip install -r requirements.txt
```

Также для работы требуется утилита **curl**.

## Запуск

Запуск из корня проекта:

```bash
python3 script.py <token> <database_path>
```

Здесь `token`&nbsp;&mdash; индивидуальный токен авторизации, `database_path`&nbsp;&mdash; путь до загружаемой базы.

Например, для загрузки тестовой базы данных и для токена `token` выполните из корня проекта:

```bash
python3 script.py token './data/Тестовая база.xlsx'
```
