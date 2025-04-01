## _Веб-Приложение реферальной системы_

### Реализован API для следующего функционала:

- Авторизация по номеру телефона (отправка 4хзначного кода авторизации);
- Хранение данных пользователя в БД;
- Профиль пользователя(наличие своего 6-значного инвайт-кода, возможность активировать 1 инвайт- код и список пользователей(номеров телефона), которые ввели инвайт-код текущего пользователя).

### Технологии:

Python3, Django, MySQL, Postman, Pytest, Selenium

### Тестирование:

На основании тех.задания было выполнено тестирование двух основных поинтов приложения - user_login, user_authentication и account_access на предмет корректности работы API.

Выполнено:
1.	Анализ требований
2.	Создание тестовой документации (тест-кейсы)
3.	Выполнение тестов (коллекция запросов в Postman)
4.	Фиксация дефектов – оформление баг-репортов (Yougile)

При тестировании использовались техники тест-дизайна:

Для работы с БД (отслеживание изменений) использовался - DBeaver.

Использован Pytest для написания интеграционных тестов и создания тестовой бд.


![Screenshot from 2024-05-16 13-09-38](https://github.com/ElenaGlu/Referral-system/assets/123466535/447b6f47-5a95-4677-a4fc-281206357cd4)

