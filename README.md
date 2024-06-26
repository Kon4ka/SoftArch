# Проект: Сайт конференции

## Цель
Целью выполнения практических заданий является получение практических навыков в создании приложений, ориентированных на хранение и обработку больших объемов данных.

## Вариант 3 - Сайт конференций
Приложение должно содержать следующие данные:
- Пользователь
- Доклад
- Конференция

### Реализованные API
- Создание нового пользователя
- Поиск пользователя по логину
- Поиск пользователя по маске имени и фамилии
- Создание доклада
- Получение списка всех докладов
- Добавление доклада в конференцию
- Получение списка докладов в конференции

## Задание 01: Проектирование программной системы (Architecture As A Code)
### Цель
Ознакомиться с инструментами проектирования в формате Architecture As A Code. Получить практический навык в моделировании в нотации C4.

### Задание
1. Установить инструменты из списка:
    - Клиент Git
    - Текстовый редактор (рекомендуется Visual Studio Code)
    - Плагины к Visual Studio Code C4 DSL
2. Зарегистрироваться на github.com (если еще нет учетной записи)
3. Создать публичный репозиторий для выполнения практической работы у себя в аккаунте
4. Скопировать репозиторий https://github.com/DVDemon/hl_mai_lab_00 с примерами задания
5. Создать файлы с описанием "архитектуры" согласно вашему варианту задания в Structurizr Lite.
6. Требования к диаграммам:
    - Должна быть контекстная диаграмма
    - Должна быть диаграмма контейнеров
    - Должна быть диаграмма развертывания
    - Должно быть несколько динамических диаграмм.

## Задание 02: Stateful сервис для RDBMS

### Цель
Получение практических навыков в построении сервисов, работающих с
реляционными данными.

### Задание
Разработать приложение осуществляющее хранение данных о пользователях в
реляционной СУБД. Для выявленных в предыдущем задании вызовов между
сервисами создайте REST интерфейс.

Должны выполняться следующие условия:
- Данные должны храниться в СУБД PostgreSQL;
- Должны быть созданы таблицы для каждой сущности из вашего задания;
- Интерфейс к сущностям должен предоставляться в соответствии со стилем REST;
- API должен быть специфицирован в OpenAPI 3.0 (должен хранится в index.yaml);
- Должен быть создан скрипт по созданию базы данных и таблиц, а также
наполнению СУБД тестовыми значениями;
- Для сущности, отвечающей за хранение данных о пользователе (клиенте), для
пользователей должен быть реализован интерфейс поиска по маске фамилии и
имени, а также стандартные CRUD операции.
- Данные о пользователе должны включать логин и пароль. Пароль должен
храниться в закрытом виде (хэширован)

Рекомендуема последовательность выполнения работы:
1. Создайте схему БД
2. Создайте таблицы
3. Создайте скрипт для первичного наполнение БД и выполните
4. Реализуйте REST-сервис
5. Сделайте спецификацию с OpenAPI с помощью Postman и сохраните ее в
index.yml
6. Протестируйте сервис
7. Создайте Dockerfile для вашего сервиса
8. Протестируйте его работу в Docker
9. Опубликуйте на GitHub проект


### Запуск лабораторных
1. Включить docker
2. Зайти в папку app
3. docker-compose up в папке app (все лабы до 4 включительно в этой папке)
4. Дождаться пока все развернется и все всех увидят (lab4_data_generator - загрузчик данных)
5. http://localhost:8080/docs - swagger со списком api
   - по отдельным портам доступны отдельные контейнеры (user_service - 8080, conferences - 8081, reports - 8082)
   - Для загрузки данных есть отдельный контейнер lab4_data_generator
   - Можно создать юзера в /api/users/new_user
   - Потом залогиниться используя логин и пароль из предыдущего пункта /api/login_router/login - вернётся JWT токен
   - Найти пользователя по логину /api/login_router/login - вернется информация о пользователе, в том числе id
   - В методе /api/users/delete сначала ввести JWT токен и другой id - пользователь не будет удалён
   - В методе /api/users/delete сначала ввести JWT токен и id текущего пользователя - пользователь удалиться
6. (Опционально) Проверить БД:
    1. docker exec -it postgres /bin/bash
    2. psql -U stud -d postgres - подключться к postgres
    3. \c conference_db - зайти базу данных conference_db
    4. \dt - посмотреть какие там таблицы командой
    5. Выполнить SELECT * FROM users;

