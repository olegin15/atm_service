## Тестовое задание для Python разработчика

К нам обратился один известный банк с просьбой написать софт для своих банкоматов. Поскольку на дворе 2019 год, разумеется им нужен микросервис. Итак, сервис должен реализовывать HTTP API и поддерживать 2 операции:

1) **Внесение наличных** - принять в банкомат несколько монет/купюр.
Входные параметры:

    - `currency` (_string_): Код валюты
    - `value` (_int_): Номинал купюры
    - `quantity` (_int_): Количество купюр

    Пример запроса:
    ```
    POST /deposit

    {
        "currency": "RUB",
        "value": 100,
        "quantity": 10
    }
    ```
    Успешный ответ:
    ```
    {
        "success": true
    }
    ```
2) **Получение наличных** - выдать из банкомата определенную сумму денег в определенной валюте.
В ответе должен возвращаться набор купюр, которыми банкомат выдаст нужную сумму, т.е. их номиналы и количество.
Входные параметры:

    - `currency` (_string_): Код валюты
    - `amount` (_int_): Сумма

    Пример запроса:
    ```
    POST /withdraw

    {
        "currency": "RUB",
        "amount": 350
    }
    ```
    Успешный ответ:
    ```
    {
        "success": true,
        "result": [
            {
                "value": 100,
                "quantity": 3
            },
            {
                "value": 50,
                "quantity": 1
            }
        ]
    }
    ```

### Технические требования
 - Python 3
 - Любые фреймворки и библиотеки на выбор
 - Формат данных - json
 - Поддерживаемые валюты - RUB, USD, EUR
 - Банкомат обычный, сам деньги не печатает, может выдавать только то, что в него положили. Если выдать требуемую сумму нет возможности - в ответ должна возвращаться ошибка
 - Формат ошибок - на усмотрение разработчика