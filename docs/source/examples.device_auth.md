# Получение токена через Device Flow

Пример получения OAuth-токена через OAuth Device Flow без сторонних инструментов.
Метод `device_auth` блокирующий: он ждёт, пока вы подтвердите вход на странице
Яндекса, и возвращает `OAuthToken` с полями `access_token`, `refresh_token`,
`expires_in`, `token_type`. Сохранять токен (например, в файл или БД) —
ответственность вызывающего кода.

::::{tab-set}

:::{tab-item} Синхронный

```{literalinclude} ../../examples/device_auth.py
:language: python
:caption: examples/device_auth.py
```

:::

:::{tab-item} Асинхронный

```{literalinclude} ../../examples/device_auth_async.py
:language: python
:caption: examples/device_auth_async.py
```

:::

::::
