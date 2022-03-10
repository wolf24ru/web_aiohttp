## Шаги для запуска:

1) Собрать конфигурацию командой:

    * Для первого запуска: 
   ```cmd
    docker-compose up -d --build
    ```
   * Для последующих запусков
   ```cmd
    docker-compose up
    ```
2) Отправить запрос на http://0.0.0.0:8080/ :

### Проверка соединения:

## Шаги для запуска:

1) Собрать конфигурацию командой:

    * Для первого запуска: 
   ```cmd
    docker-compose up -d --build
    ```
   * Для последующих запусков
   ```cmd
    docker-compose up
    ```
2) Отправить запрос на http://0.0.0.0:8080/ :

|Описание                   |Метод |Ссылка              |JSON аргументы | 
|---------------------------|------|--------------------|---------------| 
|Проверка соединения:       | GET  |/health             |                                                |
|Создание пользователя      | POST | /new_user          |<span style="color: #E79234;">**user_name**</span> - имя пользователя;  <span style="color: #E79234;">**password**</span> - пароль|
|Получтиь пользователя по id| GET  | /get_user/<user_id>|                                                |
|Создание рекламного объявления           | POST | /adv_new           |<span style="color: #E79234;">**user_name**</span> - имя пользователя;  <span style="color: #E79234;">**password**</span> - пароль; <span style="color: #E79234;">**title**</span> - название объявления; <span style="color: #E79234;">**description**</span> - описание объвления|
|Получение всех рекламных объявлений|GET|/adv||
|Получение ремногого объявления по id|GET|/adv/<adv_id>||
|Удаление рекламного объявления|DELETE|/adv_del/<adv_id>|<span style="color: #E79234;">**user_name**</span> - имя пользователя;  <span style="color: #E79234;">**password**</span> - пароль;|
|Изменение рекламного объявления|PATCH|\adv_patch\<adv_id>|<span style="color: #E79234;">**user_name**</span> - имя пользователя;  <span style="color: #E79234;">**password**</span> - пароль; <span style="color: #E79234;">**title**</span> - название объявления; <span style="color: #E79234;">**description**</span> - описание объвления|

**<user_id>** - идентификатор пользователя  
**<adv_id>** - идентификатор рекламного объявления
