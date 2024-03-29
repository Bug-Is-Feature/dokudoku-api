# DokuDoku Backend System

<p align='center'>
    <img src='https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10-blue?logo=python&color=0064a5' />
    <img src='https://img.shields.io/badge/django-4.2-green?logo=django&color=092e20' />
    <img src='https://img.shields.io/badge/postgresql-15-green?logo=postgresql&color=336791' />
</p>
<p align='center'>
    <a href='https://github.com/Bug-Is-Feature/dokudoku-api/actions/workflows/django.yml'>
        <img src='https://github.com/Bug-Is-Feature/dokudoku-api/actions/workflows/django.yml/badge.svg?branch=main' />
    </a>
    <a href="https://codecov.io/gh/Bug-Is-Feature/dokudoku-api" > 
        <img src="https://codecov.io/gh/Bug-Is-Feature/dokudoku-api/branch/main/graph/badge.svg?token=KX285P8G80"/> 
    </a>
</p>

## About the Project

-   DokuDoku is a project of software engineering courses (KMUTT, CSS321 & CSS322)
-   It's setup to use with flutter mobile application named [DokuDoku](https://github.com/Bug-Is-Feature/DokuDoku)

## Disclaimer

-   This project is only implemented as REST APIs service, and did not have a webpage.
-   This project did not implement with Django Authentication but use Firebase Authentication instead.
-   This project is built to deploy on [Render](https://render.com), you may need to edit the `/config/settings.py` file if you desire to deploy elsewhere.
-   Please be aware that this project is based on DokuDoku use cases, any use cases that are not mentioned in documentation may cause errors.

## Table of Contents

-   [Setup Project](#setting-up-the-project-locally)
-   [Schema](#schema)
-   [API](#api)
    -   [Get JWT Token](#fetch-firebase-auth-token)
    -   [Backend API](#dokudoku-backend)
        -   [User Routes](#user-routes)
        -   [User Admin Routes](#user-admin-routes)
        -   [Book Routes](#book-routes)
        -   [Author Routes](#author-routes)
        -   [Book Recommender Routes](#book-recommender-routes)
        -   [Session Routes](#session-routes)
        -   [Library Routes](#library-routes)
        -   [Library Books Routes](#library-books-routes)
        -   [Achievement Group Routes](#achievement-group-routes)
        -   [Achievement Routes](#achievement-routes)
        -   [User Achievement Routes](#user-achievement-routes)

## Setting up the project

1. Python 3.8-3.10 & Postgres 15 or later installed
1. Setup [Firebase Authentication](https://firebase.google.com/docs/auth) & [Firebase Storage](https://firebase.google.com/docs/storage)
1. Pipenv installed. Alternatively, you can install it by typing this in your CLI: `pip install pipenv`
1. In the root directory, create a virtual environment: `pipenv shell`
1. Install dependencies: `pipenv install`
1. Setup Database (Skip this if you use default database)
    1. Start CLI at your Postgresql `/bin` folder
    1. Login as superuser (default: postgres): `psql -U <USERNAME>`
    1. Create database: `CREATE DATABASE <YOUR_DB_NAME>;`
    1. Create DB's user: `CREATE USER <YOUR_DB_USER>;`
    1. Connect to your DB: `\c <YOUR_DB_NAME>`
    1. Grant privileges to user on schema of the DB ('public' is default): `GRANT ALL PRIVILEGES ON SCHEMA public TO <YOUR DB USER>;`
    1. (optional) If you want to execute test files, you have to give CREATEDB privilege to user: `ALTER USER <YOUR DB USER> CREATEDB;`
1. Setup .env file
    ```
    export DEBUG = TRUE
    export SECRET_KEY = django-insecure-<YOUR_DJANGO_SECRET_KEY>
    export PSQL_DB_NAME = <YOUR_DB_NAME>
    export PSQL_DB_USER = <YOUR_DB_USER>
    export PSQL_DB_USER_PWD = <YOURE_DB_USER_PASSWORD>
    export PSQL_DB_HOST = <YOUR_DB_HOST>
    export PSQL_DB_PORT = <YOUR_DB_PORT>
    export EXTERNAL_PSQL_URL = <YOUR_CLOUD_DB_URL>
    export FIREBASE_BUCKET_NAME = <YOUR_FIREABSE_BUCKET_NAME>
    export GOOGLE_APPLICATION_CREDENTIALS_BASE64 = <YOUR_BASE64_ENCODED_FIREBASE_ADMIN_SDK>
    ```
    - You can download firebase admin sdk from your firebase project site: `Project settings > Service accounts > Firebase Admin SDK > Generate new private key`.
    - After download encode it to [base64](https://www.base64encode.org/), `REMINDER:` this encoded text still considered a secret.
    - `EXTERNAL_PSQL_URL` is not necessary if you only run with **DEBUG = TRUE**.
    - If `DEBUG = FALSE` the database will change to deployed PostgreSQL (External URL), you can change this behavior by edit code at `/config/settings.py line: 101-117`.
1. Do the migration (make sure you're at the project root directory): `python manage.py migrate`
1. Run the app: `python manage.py runserver`
1. Load achievements data: `python manage.py loaddata achievement_groups` then `python manage.py loaddata achievements`

## Schema

-   Users (table name: user)

    |  Key   | Field       | Type         | Nullable | Constraints |
    | :----: | ----------- | ------------ | :------: | :---------: |
    | **PK** | uid         | VARCHAR(28)  |  FALSE   |             |
    |        | email       | VARCHAR(255) |  FALSE   |             |
    |        | current_lvl | INTEGER      |  FALSE   |    >= 0     |
    |        | current_exp | INTEGER      |  FALSE   |    >= 0     |
    |        | is_admin    | BOOLEAN      |  FALSE   |             |
    |        | last_login  | TIMESTAMP    |   TRUE   |             |
    |        | date_joined | TIMESTAMP    |  FALSE   |             |

-   Books (table name: book)

    |      Key      | Field          | Type         | Nullable |             Default              |      Constraints       |
    | :-----------: | -------------- | ------------ | :------: | :------------------------------: | :--------------------: |
    |    **PK**     | id             | BIGINT       |  FALSE   | Generated by default as identity |                        |
    |               | google_book_id | VARCHAR(12)  |   TRUE   |                                  | UNIQUE(google_book_id) |
    |               | title          | VARCHAR(255) |  FALSE   |                                  |                        |
    |               | subtitle       | VARCHAR(255) |   TRUE   |                                  |                        |
    |               | category       | VARCHAR(40)  |   TRUE   |                                  |                        |
    |               | thumbnail      | TEXT         |   TRUE   |                                  |                        |
    |               | description    | TEXT         |   TRUE   |                                  |                        |
    |               | page_count     | INTEGER      |  FALSE   |                                  |          >= 0          |
    |               | currency_code  | VARCHAR(3)   |   TRUE   |                                  |                        |
    |               | price          | DOUBLE       |  FALSE   |                                  |                        |
    |               | created_at     | TIMESTAMP    |  FALSE   |                                  |                        |
    | **FK (user)** | created_by     | VARCHAR(28)  |   TRUE   |                                  |                        |

-   Authors (table name: book_author)

    |      Key      | Field   | Type        | Nullable |             Default              |      Constraints      |
    | :-----------: | ------- | ----------- | :------: | :------------------------------: | :-------------------: |
    |    **PK**     | id      | BIGINT      |  FALSE   | Generated by default as identity |                       |
    |               | name    | VARCHAR(55) |  FALSE   |                                  | UNIQUE(book_id, name) |
    | **FK (book)** | book_id | BIGINT      |  FALSE   |                                  | UNIQUE(book_id, name) |

-   Reading_sessions (table name: session)

    |      Key      | Field      | Type        | Nullable |             Default              | Constraints |
    | :-----------: | ---------- | ----------- | :------: | :------------------------------: | :---------: |
    |    **PK**     | id         | BIGINT      |  FALSE   | Generated by default as identity |             |
    |               | duration   | INTEGER     |  FALSE   |                                  |    >= 0     |
    |               | timer_type | VARCHAR(2)  |  FALSE   |                                  |             |
    |               | created_at | TIMESTAMP   |  FALSE   |                                  |             |
    | **FK (user)** | created_by | VARCHAR(28) |  FALSE   |                                  |             |
    | **FK (book)** | book_id    | BIGINT      |  FALSE   |                                  |             |

-   Library (table name: user_library)

    |      Key      | Field      | Type        | Nullable |             Default              |    Constraints     |
    | :-----------: | ---------- | ----------- | :------: | :------------------------------: | :----------------: |
    |    **PK**     | id         | BIGINT      |  FALSE   | Generated by default as identity |                    |
    |               | created_at | TIMESTAMP   |  FALSE   |                                  |        >= 0        |
    |               | is_changed | BOOLEAN     |  FALSE   |                                  |                    |
    | **FK (user)** | created_by | VARCHAR(28) |  FALSE   |                                  | UNIQUE(created_by) |

-   LibraryBook (table name: library_book)

    |       Key        | Field        | Type      | Nullable |             Default              |         Constraints         |
    | :--------------: | ------------ | --------- | :------: | :------------------------------: | :-------------------------: |
    |      **PK**      | id           | BIGINT    |  FALSE   | Generated by default as identity |                             |
    |                  | is_completed | BOOLEAN   |  FALSE   |                                  |                             |
    |                  | created_at   | TIMESTAMP |  FALSE   |                                  |                             |
    |  **FK (book)**   | book_id      | BIGINT    |  FALSE   |                                  | UNIQUE(library_id, book_id) |
    | **FK (library)** | library_id   | BIGINT    |  FALSE   |                                  | UNIQUE(library_id, book_id) |

-   Achievement Group (table name: achievement_group)

    |  Key   | Field | Type        | Nullable |             Default              | Constraints  |
    | :----: | ----- | ----------- | :------: | :------------------------------: | :----------: |
    | **PK** | id    | BIGINT      |  FALSE   | Generated by default as identity |              |
    |        | name  | VARCHAR(50) |  FALSE   |                                  | UNIQUE(name) |

-   Achievements (table name: achievement)

    |            Key             | Field              | Type        | Nullable |             Default              | Constraints  |
    | :------------------------: | ------------------ | ----------- | :------: | :------------------------------: | :----------: |
    |           **PK**           | id                 | BIGINT      |  FALSE   | Generated by default as identity |              |
    |                            | name               | VARCHAR(50) |  FALSE   |                                  | UNIQUE(name) |
    |                            | description        | TEXT        |   TRUE   |                                  |              |
    |                            | locked_thumbnail   | TEXT        |  FALSE   |                                  |              |
    |                            | unlocked_thumbnail | TEXT        |  FALSE   |                                  |              |
    |                            | condition          | VARCHAR(4)  |  FALSE   |                                  |              |
    |                            | threshold          | INTEGER     |  FALSE   |                                  |     >= 0     |
    |                            | available          | BOOLEAN     |  FALSE   |                                  |              |
    |                            | created_at         | TIMESTAMP   |  FALSE   |                                  |              |
    | **FK (achievement_group)** | group_id           | BIGINT      |   TRUE   |                                  |              |

-   User Achievements (table name: user_achievement)

    |         Key          | Field          | Type        | Nullable |             Default              |         Constraints         |
    | :------------------: | -------------- | ----------- | :------: | :------------------------------: | :-------------------------: |
    |        **PK**        | id             | BIGINT      |  FALSE   | Generated by default as identity |                             |
    | **FK (achievement)** | achievement_id | BIGINT      |  FALSE   |                                  | UNIQUE(uid, achievement_id) |
    |    **FK (user)**     | uid            | VARCHAR(28) |  FALSE   |                                  | UNIQUE(uid, achievement_id) |

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

> Edit `is_admin` and delete admin accounts are not allowed in this route

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

### User Admin Routes

> Only `is_admin` are allowed for editing in this route

**/user-admin**

-   GET

    -   Purpose: Get all admin in system
    -   Permission: **Admin**

**/user-admin/:id**

-   GET

    -   Purpose: Get specific admin by :id
    -   Permission: **Admin**

-   PATCH (Partial Update)

    -   Purpose: Update user `is_admin` status only, other attribute are not allowed.
    -   Permission: **Admin**

-   DELETE

    -   Purpose: Delete admin account
    -   Permission: **Admin**

Example Response:

```
{
    "uid": "kM5cDAwpIiM7YXXXXXXXXXXXXXXX",
    "last_login": "2023-01-13T05:09:28.617875+07:00",
    "email": "abc@abc.com",
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
        -   User: Fetch all their own **custom books**
    -   Query Parameter (**can only use 1 parameter per request**)
        -   **ggbookid**: Filter by Google Book ID
            -   Permission: Everyone
        -   **owner**: Filter by book owner
            -   Permission: Admin, Owner

-   POST

    -   Permission: Admin Only (User NEED to use [/library-books](#library-books-routes) route to create book)
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
    -   Permission: Admin Only (User NEED to use [/library-books](#library-books-routes) route to delete book)

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
        ... User Data ...
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

### Book Recommender Routes

**/recommendation**

-   GET

    -   NOTE: This route only recommend based-on incomplete book in library and user's most read book, if user have no session system will consider user's first added book to be a target.
    -   NOTE 2: Recommendation result is store as file on cloud and update with cronjob (run at 12:00 and 00:00 GMT+7), if user have less than 2 **incomplete** books at scheduled time, the recommendation result will not update or create.
    -   Permission: Everyone

Example Response:

```
[
    {
        ... Book Data ...
    },
    {
        ... Book Data ...
    },
    {
        ... Book Data ...
    }
]
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
    -   Enum Types:
        -   `timer_type`: ['Stopwatch', 'Hourglass']
    -   Example Request Body:
        ```
        {
            "uid": "EiDHQmmoXXXXXXXXXXXXXXXXXXXX",
            "book_id": 2,
            "timer_type": "Stopwatch",
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
        ... Book Data ...
    },
    "duration": 600,
    "created_by": {
        ... User Data ...
    },
    "timer_type": "Stopwatch",
    "created_at": "2023-01-16T19:09:25.502573+07:00"
}
```

<hr>

### Library Routes

**/library**

-   GET

    -   Permission:
        -   Admin: Fetch all library
        -   User: Fetch their own library
    -   Query Parameter
        -   **uid**: Filter by uid
            -   Permission: Admin, Owner

-   POST

    -   Permission: Admin (For normal user, use POST /library-books/)
    -   Example Request Body:
        ```
        {
            "uid": "XXXXXXXXXXXXXXX"
        }
        ```

**/library/:id**

-   GET

    -   Permission: Admin, User **[Owner Only]**

-   PUT & PATCH

    -   Permission: Admin

-   DELETE
    -   Permission: Admin

Example Response:

```
{
    "id": 2,
    "created_by": {
        ... User Data ...
    },
    "created_at": "2023-01-16T19:09:25.502573+07:00",
    "book_count": 1,
    "completed_count": 1,
    "incomplete_count": 0,
    "books": [
        {
            ... Library Books Data ...
        },
        {
            ...
        }
    ]
}
```

<hr>

### Library Books Routes

**/library-books**

-   GET

    -   Permission:
        -   Admin: Fetch every book in every user library
        -   User: Fetch every book in their own library
    -   Query Parameter:
        -   **library_id**: Filter by library ID
            -   Permission: Admin, User **[Owner Only]**

-   POST
    -   NOTICE: This operation **create user's library and book automatically** if the data not exist in database.
    -   Permission: Everyone
    -   Example Request Body: TRY NOT TO INCLUDE BOTH google_book_id and created_by in `book_data` to avoid any unexpected bug
        ```
        {
            "book_data": {
                "title": "",
                "subtitle": "",
                "category": "",
                "thumbnail": "",
                "description": "",
                "page_count": 1,
                "currency_code": "",
                "price": 0.0,
                "google_book_id": ""
            },
            "is_completed": true
        }
        ```

**/library-books/:id**

-   GET

    -   Permission: Admin, User **[Owner Only]**

-   PUT & PATCH

    -   Permission:
        -   Admin: Can edit every attribute
        -   User **[Owner Only]**: Can edit only `is_completed`

-   DELETE

    -   Permission: Admin, User **[Owner Only]**

Example Response:

```
{
    "library_book_id": 1,
    "is_completed": true,
    "created_at": "2023-02-13T10:51:21.393000+07:00",
    "book": {
        ... Book Data ...
    }
}
```

<hr>

### Achievement Group Routes

**/achievement-groups**

-   GET

    -   Permission: Everyone

-   POST
    -   Permission: Admin
    -   Example Request Body:
        ```
        {
            "name": "achievement_group_name",
        }
        ```

**/achievement-groups/:id**

-   GET

    -   Permission: Everyone

-   PUT & PATCH

    -   Permission: Admin

-   DELETE

    -   Permission: Admin

Example Response:

```
{
    "id": 12,
    "name": "achievement_group_name"
}
```

<hr>

### Achievement Routes

**/achievements**

-   GET

    -   Permission:
        -   Admin: Fetch every achievements in database
        -   User: Fetch every achievements in database that's **available**

-   POST
    -   Permission: Admin
    -   Enum Types:
        -   `condition`: ['Book Amount', 'Incomplete Book Amount', 'Total Reading Hours', 'Stopwatch Reading Hours', 'Hourglass Reading Hours']
    -   Example Request Body:
        ```
        {
            "id": 1,
            "name": "achievement",
            "description": "achievement_desc",
            "group_id": 12,
            "locked_thumbnail": "locked_thumbnail",
            "unlocked_thumbnail": "unlocked_thumbnail",
            "condition": "Book Amount",
            "threshold": 20,
            "available": false
        }
        ```

**/achievements/:id**

-   GET

    -   Permission: Admin, User **[available = true]**

-   PUT & PATCH

    -   Permission: Admin

-   DELETE

    -   Permission: Admin

Example Response:

NOTE: if `group = null` then the achievement is **not belong to any group**.

```
{
    "id": 1,
    "name": "achievement",
    "description": "achievement_description",
    "group": {
        ... Achievement Group Data ...
    },
    "locked_thumbnail": "locked_thumbnail",
    "unlocked_thumbnail": "unlocked_thumbnail",
    "condition": "Hourglass Reading Hours',
    "threshold": 24
}
```

<hr>

### User Achievement Routes

**/user-achievements**

-   GET

    -   Permission:
        -   Admin: Fetch every user's achievements
        -   User: Fetch their own achievements

-   POST
    -   Permission: Everyone
    -   Example Request Body:
        ```
        {
            "uid": "XXXXXXXXXXXXXXX",
            "unlocked_achievement_id": 123,
        }
        ```

**/user-achievements/:id**

-   GET

    -   Permission: Admin, User **[Owner Only]**

-   PUT & PATCH

    -   Permission: Admin

-   DELETE

    -   Permission: Admin

Example Response:

```
{
    "user_achievement_id": 12,
    "achievement_id": 123
}
```

<hr>
<p align='right'><a href='#dokudoku-backend-system'>Back to top</a></p>
