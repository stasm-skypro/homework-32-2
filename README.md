# Домашняя работа к модулю 8
# Тема 32.2 Документирование и безопасность

## 1. Настройка вывода документации для проекта (Swagger)
Документация будет доступна по адресу http://127.0.0.1:8000/swagger

## 2. Оплата курсов
Оплата курсов осуществляется через сервис Stripe.
Для начала оплаты необходимо зарегистрироваться в сервисе.
Создать цену и сессию.

#### Получаем токен

#### Создаем цену

```POST``` ```http://127.0.0.1:8000/users/payment/```

body:
```json
{
    "amount": 50000,
    "payment_method": "transfer",
    "course": 1,
    "user": 1
}
```

Ответ:
```json
{
    "id": 45,
    "date": "2025-04-02T19:22:53.941936+05:00",
    "amount": "50000.00",
    "payment_method": "transfer",
    "session_id": "cs_test_a1aTzM37ZCo2rUbtFSuFKl2FXWESW12pQUg77pcHWrDf8jlyEAdjs5JUL5",
    "link": "https://checkout.stripe.com/c/pay/cs_test_a1aTzM37ZCo2rUbtFSuFKl2FXWESW12pQUg77pcHWrDf8jlyEAdjs5JUL5#fidkdWxOYHwnPyd1blpxYHZxWjA0Vz1ybG9UX1NrRGNOS3U2YUBwdjBhMXd1SWx9aEFSUjJwalN3M3JRfHxpaXNnY1ZHTUFsa0dXQUQ9aWF1T2N9Vn9pMH9UTUZxVERoTFxSVXdyZkhzNzJoNTVRVDxAZ05fUycpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl",
    "user": 1,
    "course": 1,
    "lesson": null
}
```
![payment1](/media/readme/payment1.png)

!![payment2](/media/readme/payment2.png)

## Дополнительное задание 
### Проверка статуса
