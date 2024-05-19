# Avicenna

Этот проект предназначен для быстрого поиска подходящего для вас доктора 

## Установка

1. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/yourusername/django-disease-management.git
    cd django-disease-management
    ```

2. Создайте виртуальное окружение и активируйте его:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Установите зависимости:

    ```sh
    pip install -r requirements.txt
    ```

4. Выполните миграции базы данных:

    ```sh
    python manage.py migrate
    ```

5. Создайте суперпользователя для админ-панели:

    ```sh
    python manage.py createsuperuser
    ```

6. Запустите сервер разработки:

    ```sh
    python manage.py runserver
    ```

Теперь вы можете открыть браузер и перейти по адресу `http://127.0.0.1:8000/` для просмотра вашего приложения.

## Использование

После запуска сервера вы можете использовать API для управления категориями болезней, постами, вложениями и комментариями.

### Endpoints

- `GET /disease-categories/` - Получить список всех категорий болезней.
- `POST /disease-categories/` - Создать новую категорию болезней.
- `GET /disease-posts/` - Получить список всех постов о болезнях.
- `POST /disease-posts/` - Создать новый пост о болезни.
- `GET /disease-post-attachments/` - Получить список всех вложений к постам.
- `POST /disease-post-attachments/` - Создать новое вложение к посту.
- `GET /comments/` - Получить список всех комментариев.
- `POST /comments/` - Создать новый комментарий.

## Тестирование

Для запуска тестов выполните команду:

```sh
python manage.py test
