workspace {
    name "Умный дом"
    description "Простая система управления умного дома с базовыми функциями контроля состояния атмосферы в помещении"

    # включаем режим с иерархической системой идентификаторов
    !identifiers hierarchical

    # Модель архитектуры
    model {
        properties { 
            structurizr.groupSeparator "/"
        }

        user = person "Пользователь" {
            description "Пользователь конференции"
        }

        conference_system = softwareSystem "Система конференций" {
            description "Система для управления конференциями и докладами"

            user_service = container "User Service" {
                description "Сервис для управления пользователями"
                technology "REST API"
            }

            report_service = container "Report Service" {
                description "Сервис для управления докладами"
                technology "REST API"
            }

            conference_service = container "Conference Service" {
                description "Сервис для управления конференциями"
                technology "REST API"
            }

            group "Слой данных" {
                postgres_database = container "PostgreSQL Database" {
                    description "База данных PostgreSQL с пользователями, конференциями и ID докладов"
                    technology "PostgreSQL"
                    tags "database"
                }

                mongo_database = container "MongoDB Database" {
                    description "База данных MongoDB со всеми докладами"
                    technology "MongoDB"
                    tags "database"
                }

                redis_cache = container "Redis Cache" {
                    description "Кеш Redis для ускорения авторизации"
                    technology "Redis"
                    tags "cache"
                }
            }

            user_service -> postgres_database "CRUD операции с пользователями и конференциями"
            user_service -> redis_cache "Авторизация пользователей"
            report_service -> mongo_database "CRUD операции с докладами"
            conference_service -> postgres_database "Связывание докладов с конференциями"

            user -> user_service "Регистрация, поиск"
            user -> report_service "Создание, получение списка докладов"
            user -> conference_service "Добавление доклада, получение списка докладов в конференции"
        }
    }

    views {
        themes default

        properties { 
            structurizr.tooltips true
        }


        !script groovy {
            workspace.views.createDefaultViews()
            workspace.views.views.findAll { it instanceof com.structurizr.view.ModelView }.each { it.enableAutomaticLayout() }
        }

        dynamic conference_system "UC01" "Регистрация нового пользователя" {
            autoLayout
            user -> conference_system.user_service "Создать нового пользователя (POST /users)"
            conference_system.user_service -> conference_system.postgres_database "Сохранить данные о пользователе"
            conference_system.user_service -> conference_system.redis_cache "Кэшировать данные о пользователе"
}

        dynamic conference_system "UC02" "Поиск пользователя по логину" {
            autoLayout
            user -> conference_system.user_service "Поиск пользователя (GET /users/{login})"
            conference_system.user_service -> conference_system.redis_cache "Проверить кэш пользователя"
            conference_system.user_service -> conference_system.postgres_database "Получить данные о пользователе"
        }

        dynamic conference_system "UC03" "Создание доклада" {
            autoLayout
            user -> conference_system.report_service "Создать доклад (POST /reports)"
            conference_system.report_service -> conference_system.mongo_database "Сохранить доклад"
        }

        dynamic conference_system "UC04" "Добавление доклада в конференцию" {
            autoLayout
            user -> conference_system.conference_service "Добавить доклад в конференцию (POST /conferences/{id}/reports)"
            conference_system.conference_service -> conference_system.postgres_database "Связать доклад с конференцией"
        }


        styles {
            element "database" {
                shape cylinder
            }
        }
    }
}