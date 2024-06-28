# Ссылка на репозиторий
https://github.com/versuffer/Auth_sprint_1

# Как запустить сервис

```bash
cd infra
```

```bash
docker compose up -d --build
```

# Управление учётными записями
Модуль ```cli.py``` содержит CLI-утилиту для создания / вывода списка учётных записей.

#### Доступные команды:

1) Вывод списка учётных записей:

```bash
python cli.py list-users
```

2) Создание учётной записи суперпользователя:

```bash
python cli.py create-user
```

