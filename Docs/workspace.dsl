workspace {
    name "Сервис конференции"
    description "Простая система сбора конференций из докладов и спикеров"

    !identifiers hierarchical


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

            conference_service = container "Conference Service" {
                description "Сервис для управления конференциями"
                technology "REST API"
            }

            report_service = container "Report Service" {
                description "Сервис для управления докладами"
                technology "REST API"
            }

            group "Слой данных" {
                postgres_database = container "PostgreSQL Database" {
                    description "База данных PostgreSQL с пользователями, конференциями и ID докладов"
                    technology "PostgreSQL"
                    tags "database"
                }

                redis_cache = container "Redis Cache" {
                    description "Кеш Redis для ускорения авторизации"
                    technology "Redis"
                    tags "cache"
                }
                
                mongo_database = container "MongoDB Database" {
                    description "База данных MongoDB со всеми докладами"
                    technology "MongoDB"
                    tags "database"
                }
            }

            user_service -> postgres_database "CRUD операции с пользователями и конференциями"
            user_service -> redis_cache "Быстрая авторизация пользователей"
            conference_service -> postgres_database "Связывание докладов с конференциями"
            conference_service -> report_service "Для поиска докладов в конференции"
            report_service -> mongo_database "CRUD операции с коллекцией докладов"
            report_service -> postgres_database "CRUD операции с ID докладов"
            

            user -> user_service "Регистрация пользователя, добавление доклада и получение списка всех своих докладов, получение участия в конференциях"
            user -> conference_service "Добавление доклада в конференцию, получение списка докладов в конференции"
            user -> report_service "Создание, чтение, обновление и удаление докладов"
        }
        deploymentEnvironment "Production" {
    deploymentNode "AWS" {
        deploymentNode "EC2 Cluster" {
            containerInstance conference_system.user_service
            containerInstance conference_system.conference_service
            containerInstance conference_system.report_service
            properties {
                "cpu" "8"
                "ram" "512Gb"
                "hdd" "8Tb"
            }
        }

        deploymentNode "RDS Cluster" {
            containerInstance conference_system.postgres_database
            instances 2
            properties {
                "cpu" "4"
                "ram" "256Gb"
                "hdd" "4Tb"
            }
        }

        deploymentNode "Cache Cluster" {
            containerInstance conference_system.redis_cache
            instances 2
            properties {
                "cpu" "2"
                "ram" "128Gb"
                "hdd" "2Tb"
            }
        }

        deploymentNode "DocumentDB Cluster" {
            containerInstance conference_system.mongo_database
            instances 3
            properties {
                "cpu" "4"
                "ram" "256Gb"
                "hdd" "4Tb"
            }
        }
    }
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
            user -> conference_system.report_service "Создать доклад (POST /reports/{user_id})"
            conference_system.report_service -> conference_system.postgres_database "Проверить, существует ли пользователь с таким ID"
            conference_system.report_service -> conference_system.mongo_database "Сохранить файл доклада"
            conference_system.report_service -> conference_system.postgres_database "Сохранить ID доклада"
        }

        dynamic conference_system "UC04" "Добавление доклада в конференцию" {
            autoLayout
            user -> conference_system.conference_service "Добавить доклад в конференцию (POST /conferences/{conference_id}/reports/{report_id})"
            conference_system.conference_service -> conference_system.postgres_database "Проверить, существуют ли конференция и доклад с такими ID"
            conference_system.conference_service -> conference_system.postgres_database "Связать доклад с конференцией"
        }

        dynamic conference_system "UC05" "Получение доклада по ID" {
            autoLayout
            user -> conference_system.report_service "Получить доклад (GET /reports/{id})"
            conference_system.report_service -> conference_system.mongo_database "Получить файл доклада"
        }

        dynamic conference_system "UC06" "Обновление доклада по ID" {
            autoLayout
            user -> conference_system.report_service "Обновить доклад (PUT /reports/{id})"
            conference_system.report_service -> conference_system.mongo_database "Обновить файл доклада"
        }

        dynamic conference_system "UC07" "Удаление доклада по ID" {
            autoLayout
            user -> conference_system.report_service "Удалить доклад (DELETE /reports/{id})"
            conference_system.report_service -> conference_system.mongo_database "Удалить файл доклада"
            conference_system.report_service -> conference_system.postgres_database "Удалить ID доклада"
        }
        dynamic conference_system "UC08" "Поиск пользователя по маске имени и фамилии" {
            autoLayout
            user -> conference_system.user_service "Поиск пользователя (GET /users?name={name})"
            conference_system.user_service -> conference_system.postgres_database "Получить данные о пользователях, чьи имя и фамилия соответствуют маске"
        }

        dynamic conference_system "UC09" "Получение списка всех докладов" {
            autoLayout
            user -> conference_system.report_service "Получить список всех докладов (GET /reports)"
            conference_system.report_service -> conference_system.mongo_database "Получить все файлы докладов"
        }

        dynamic conference_system "UC10" "Получение списка докладов в конференции" {
            autoLayout
            user -> conference_system.conference_service "Получить список докладов в конференции (GET /conferences/{id}/reports)"
            conference_system.conference_service -> conference_system.postgres_database "Получить ID докладов, связанных с конференцией"
            conference_system.conference_service -> conference_system.report_service "Получить файлы докладов по ID"
        }

        styles {
            element "database" {
                shape cylinder
            }
        }
    }
}
