# DokuDoku Backend System

## About the Project

-   DokuDoku is a junior project of software engineering courses (KMUTT, CSS321 & CSS322)
-   It's setup to use with flutter mobile application named [DokuDoku](https://github.com/Bug-Is-Feature/DokuDoku)

## Table of Contents

-   [Setup Project](#setting-up-the-project-locally)
-   [Schema](#schema)
-   [API](#api)
    -   [Get JWT Token](#fetch-firebase-auth-token)
    -   [Backend API](#dokudoku-backend)
        -   [User Routes](#user-routes)
        -   [Book Routes](#book-routes)
        -   [Author Routes](#author-routes)
        -   [Session Routes](#session-routes)

## Setting up the project locally

1. Python 3.8 & Postgres 15 or later installed
1. Pipenv installed. Alternatively, you can install it by typing this in your CLI: `pip install pipenv`
1. In the root directory, create a virtual environment: `pipenv shell`
1. Install dependencies: `pipenv install`
1. Setup Database
    1. Start CLI at your Postgresql `/bin` folder
    1. Login as superuser: `psql -U <USERNAME>`
    1. Create database: `CREATE DATABASE <YOUR_DB_NAME>;`
    1. Create DB's user: `CREATE USER <YOUR_DB_USER>;`
    1. Connect to your DB: `\c <YOUR_DB_NAME>`
    1. Grant privileges to user on schema of the DB ('public' is default): `GRANT ALL PRIVILEGES ON SCHEMA public TO <YOUR DB USER>;`
1. Setup .env file
    ```
    export SECRET_KEY = 'django-insecure-<YOUR_DJANGO_SECRET_KEY>'
    export PSQL_DB_NAME = '<YOUR_DB_NAME>'
    export PSQL_DB_USER = '<YOUR_DB_USER>'
    export PSQL_DB_USER_PWD = '<YOURE_DB_USER_PASSWORD>'
    export PSQL_DB_HOST = '<YOUR_DB_HOST>'
    export PSQL_DB_PORT = '<YOUR_DB_PORT>'
    export GOOGLE_APPLICATION_CREDENTIALS = '<YOUR_FIREBASE_ADMIN_SDK_PATH>'
    ```
    - You can download firebase admin sdk from your firebase project site: `Project settings > Service accounts > Firebase Admin SDK > Generate new private key`
    - After download put it somewhere you desired, then copy the path
1. Do the migration (make sure you're at the project root directory): `python manage.py migrate`
1. Run the app: `python manage.py runserver`

## Schema

-   Users (user)

    -   **PK**: uid
    -   email
    -   current_lvl
    -   current_exp
    -   is_admin
    -   date_joined

-   Books (book)

    -   **PK**: id
    -   title
    -   subtitle
    -   category
    -   thumbnail
    -   description
    -   page_count
    -   currency_code
    -   price
    -   google_book_id
    -   **FK** [User]: created_by
    -   created_at

-   Authors (book_author)

    -   **PK**: id
    -   **FK** [Book]: book
    -   name

-   Reading_sessions (session)
    -   **PK**: id
    -   **FK** [User]: user
    -   **FK** [Book]: book
    -   duration
    -   created_at

## API

### **Fetch firebase auth token**

**Host:** https://www.googleapis.com

**Prefix:** /identitytoolkit/v3/relyingparty/verifyPassword?key=<FIREBASE_WEB_API_KEY>

-   POST
    -   Exanmple Request Body:
        ```
        {
            "email":"abc@abc.com",
            "password":"abcabc456",
            "returnSecureToken":true
        }
        ```
    -   Example Response:
        ```
        {
            "kind": "identitytoolkit#VerifyPasswordResponse",
            "localId": "EiDHQmmoMGYldXXXXXXXXXXXXXXX",
            "email": "abc@abc.com",
            "displayName": "",
            "idToken": "<JWT_TOKEN>", <- Use this as auth token
            "registered": true,
            "refreshToken": "<REFRESH_TOKEN>",
            "expiresIn": "3600"
        }
        ```

<hr>

### **DokuDoku Backend**

**Prefix:** /api

<hr>

### User Routes

**/users**

-   GET

    -   Permission: **Admin**

**/users/:id**

-   GET

    -   Permission: Admin, User **[Owner Only]**

-   PATCH (Partial Update)

    -   Permission: Admin, User **[Owner Only]**

-   DELETE

    -   Permission: **Admin**

Example Response:

```
{
    "uid": "kM5cDAwpIiM7YXXXXXXXXXXXXXXX",
    "last_login": "2023-01-13T05:09:28.617875+07:00",
    "email": "abc@abc.com",
    "current_lvl": 1,
    "current_exp": 0,
    "is_admin": false,
    "date_joined": "2023-01-13T05:09:28.617875+07:00"
}
```

<hr>

### Book Routes

Books have 2 types: custom book, and google book

Custom book will have non-null created_by and null google_book_id, vice versa.

**/books**

-   GET

    -   Permission:
        -   Admin: Fetch all books
        -   User: Fetch all their own custom books
    -   Query Parameter (**can only use 1 parameter per request**)
        -   **ggbookid**: Filter by Google Book ID
            -   Permission: Everyone
        -   **owner**: Filter by book owner
            -   Permission: Admin, Owner

-   POST

    -   Permission:
        -   Google Book: Everyone can create
        -   Custom Book: Admin, User **[Owner Only]**
    -   Example Request Body (**Custom Book**): DO NOT INCLUDE google_book_id
        ```
        {
            "title": "",
            "subtitle": "",
            "category": "",
            "thumbnail": "",
            "description": "",
            "page_count": 1,
            "currency_code": "",
            "price": 0,
            "uid": "XXXXXXXXXXXXXXX", <- Include to create custom book
            "authors": [
                {
                    "name": ""
                }
            ]
        }
        ```
    -   Example Request Body (**Google Book**): DO NOT INCLUDE uid
        ```
        {
            "title": "",
            "subtitle": "",
            "category": "",
            "thumbnail": "",
            "description": "",
            "page_count": 1,
            "currency_code": "",
            "price": 0,
            "google_book_id": "XXXXXX", <- Include to create google book
            "authors": [
                {
                    "name": ""
                }
            ]
        }
        ```

**/books/:id**

-   GET

    -   Permission:
        -   Google Book: Everyone can view
        -   Custom Book: Admin, User **[Owner Only]**

-   PUT & PATCH

    -   Permission:
        -   Google Book: Admin
        -   Custom Book: Admin, User **[Owner Only]**

-   DELETE
    -   Permission:
        -   Google Book: Admin
        -   Custom Book: Admin, User **[Owner Only]**

Example **Custom Book** Response:

```
{
    "id": 2,
    "title": "book title",
    "subtitle": "book subtitle",
    "category": "some category",
    "thumbnail": "surely valid thumbnail",
    "description": "tl dr",
    "page_count": 100,
    "currency_code": "THB",
    "price": 150.0,
    "created_by": {
        "uid": "kM5cDAwpIiM7YXXXXXXXXXXXXXXX",
        "last_login": "2023-01-13T05:09:28.617875+07:00",
        "email": "abc@abc.com",
        "current_lvl": 1,
        "current_exp": 0,
        "is_admin": false,
        "date_joined": "2023-01-13T05:09:28.617875+07:00"
    },
    "google_book_id": null,
    "authors": [
        {
            "id": 1,
            "name": "author 1"
        },
        {
            ...
        }
    ],
    "created_at": "2023-01-13T18:43:50.632678+07:00"
}
```

Example **Google Book** Response:

```
{
    "id": 3,
    "title": "book title",
    "subtitle": "book subtitle",
    "category": "some category",
    "thumbnail": "surely valid thumbnail",
    "description": "tl dr",
    "page_count": 100,
    "currency_code": "THB",
    "price": 150.0,
    "created_by": null,
    "google_book_id": "XXXXXXXXXXXX",
    "authors": [
        {
            "id": 2,
            "name": "author 2"
        },
        {
            ...
        }
    ],
    "created_at": "2023-01-13T18:43:50.632678+07:00"
}
```

<hr>

### Author Routes

**/authors**

-   GET

    -   Permission: Admin

-   POST
    -   Permission:
        -   Google Book Author: Admin
        -   Custom Book Author: Admin, User **[Owner Only]**
    -   Example Request Body:
        ```
        {
            "book_id": 2,
            "name": "asd"
        }
        ```

**/author/:id**

-   GET

    -   Permission:
        -   Google Book Author: Everyone
        -   Custom Book Author: Admin, User **[Owner Only]**

-   PUT & PATCH

    -   Permission:
        -   Google Book Author: Admin
        -   Custom Book Author: Custom Book Author: Admin, User **[Owner Only]**

-   DELETE
    -   Permission:
        -   Google Book Author: Admin
        -   Custom Book Author: Custom Book Author: Admin, User **[Owner Only]**

Example Response:

```
{
    "id": 1,
    "name": "author1"
}
```

<hr>

### Session Routes

**/sessions**

-   GET

    -   Permission:
        -   Admin: Fetch all sessions
        -   User: Fetch all their own sessions
    -   Query Parameter (**can only use 1 parameter per request**)
        -   **bookid**: Filter by Book ID
            -   Permission:
                -   Admin: Fetch all sessions of specific book
                -   Owner: Fetch only their own sessions of specific book
        -   **owner**: Filter by book owner
            -   Permission: Admin, Owner

-   POST
    -   Permission:
        -   Google Book Session: Everyone
        -   Custom Book Session: Admin, User **[Owner Only]**
    -   Example Request Body:
        ```
        {
            "uid": "EiDHQmmoXXXXXXXXXXXXXXXXXXXX",
            "book_id": 2,
            "duration": 600
        }
        ```

**/sessions/:id**

-   GET
    -   Permission: Admin, User **[Owner Only]**
-   PUT & PATCH
    -   Permission: Admin
-   DELETE
    -   Permission: Admin

Example Response:

```
{
    "id": 1,
    "book": {
        "id": 2,
        "title": "",
        "subtitle": "",
        "category": "",
        "thumbnail": "",
        "description": "",
        "page_count": 1,
        "currency_code": "",
        "price": 0.0,
        "created_by": null,
        "google_book_id": "XXXXXXXXXXXX",
        "authors": [
            {
                ...
            }
        ],
        "created_at": "2023-01-13T18:43:50.632678+07:00"
    },
    "duration": 600,
    "created_by": {
        "uid": "EiDHQmmoMGYldtPOGmryK0c3bIw2",
        "last_login": null,
        "email": "",
        "current_lvl": 1,
        "current_exp": 0,
        "is_admin": false,
        "date_joined": "2023-01-13T05:10:05.984843+07:00"
    },
    "created_at": "2023-01-16T19:09:25.502573+07:00"
}
```
