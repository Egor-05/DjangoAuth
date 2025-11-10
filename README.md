# Документация API
## Базовый URL

http://localhost:8000/

## Аутентификация
### Регистрация пользователя

Метод: `POST`

URL: `/auth/register/`

Permissions: `AllowAny`

Тело запроса:
```json
{
    "first_name": "string",
    "last_name": "string", 
    "email": "string",
    "password": "string",
    "repeat_password": "string"
}
```

Ответы:

`200 OK - успешная регистрация`

`400 Bad Request - неправильные данные`

### Вход в систему

Метод: `POST`

URL: `/auth/login/`

Permissions: `AllowAny`

Тело запроса:
```json
{
    "email": "string",
    "password": "string"
}
```
Ответы:

`200 OK - успешный вход`

`401 Unauthorized - неверные учетные данные`

### Выход из системы

Метод: `POST`

URL: `/auth/logout/`

Permissions: `IsAuthenticated`

Ответы:

`200 OK - успешный выход`

`403 Forbidden - у пользователя нет разрешения`

### Удаление аккаунта

Метод: `DELETE`

URL: `/auth/delete/`

Permissions: `IsAuthenticated`

Ответы:

`200 OK - аккаунт удален`

`403 Forbidden - у пользователя нет разрешения`

## Продукты
### Создание продукта

Метод: `POST`

URL: `/products/`

Permissions: `IsUser`

Тело запроса:

```json
{
    "name": "string",
    "description": "string", 
    "amount": "integer"
}
```
Ответы:

`201 Created - продукт создан`

`400 Bad Request - неправильные данные`

### Получение продуктов пользователя

Метод: `GET`

URL: `/products/my/`

Permissions: `IsUser`

Ответы:

`200 OK - список продуктов`

`403 Forbidden - у пользователя нет разрешения`

### Обновление продукта

Метод: `PATCH`

URL: `/products/{product_name}/`

Permissions: `IsCreatorOrAdmin`

Тело запроса:
```json
{
    "description": "string",
    "amount": "integer"
}
```

Ответы:

`200 OK - продукт обновлен`

`400 Bad Request - неправильные данные`

`403 Forbidden - у пользователя нет разрешения`

`404 Not Found - продукт не найден`

Удаление продукта

Метод: `DELETE`

URL: `/products/{product_name}/`

Permissions: `IsCreatorOrAdmin`

Ответы:

`200 OK - продукт удален`

`403 Forbidden - у пользователя нет разрешения`

`404 Not Found - продукт не найден`

## Модели данных
### Пользователь (User)

```json
{
    "id": "integer",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "is_active": "boolean",
    "is_staff": "boolean"
}
```

### Сессия (Session)

```json
{
    "id": "integer",
    "session_id": "string",
    "user": "User",
    "created_at": "datetime",
    "expires_at": "datetime"
}
```

### Продукт (Product)
```json
{
    "id": "integer",
    "name": "string",
    "description": "string",
    "creator": "User",
    "amount": "integer"
}
```

## Права доступа
### IsUser

Доступ: все аутентифицированные пользователи являющиеся объектом класса User


### IsCreatorOrAdmin

Доступ: создатель продукта или администратор


### IsAuthenticated

Доступ: все аутентифицированные пользователи


### AllowAny

Доступ: все пользователи

