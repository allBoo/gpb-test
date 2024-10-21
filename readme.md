# Список сервисов

- database - база данных
- import - сервис [импорта](#Импорт)
- api - API [поиска](#Поиск)
- ui - интерфейс [поиска](#Поиск)

# Импорт

## Импорт по-умолчанию из семпла

```bash 
docker compose up import
```


## Импорт из файла

```bash
docker compose run -v /path/to/file.zip:/tmp/file.zip import python manage.py import -f /tmp/file.zip -z -t -d  
```

### Параметры команды import
`-f|--file <file>` - путь к файлу для импорта

`-z|--zip` - указывает, что файл является zip архивом

`-t|--truncate` - очищает таблицы перед импортом

`-d|--debug` - выводит отладочную информацию

# Поиск

## Запуск АПИ и страницы поиска
```bash
docker compose up ui
```

По-умолчанию интерфейс доступен по адресу http://localhost:3000, АПИ по адресу http://localhost:8000.

Документация к АПИ доступна по адресу http://localhost:8000/docs

