# Itsolutions test

## Table of Contents

- [Description](#description)
- [Done](#done)
- [Demonstration](#demonstration)
- [Requirements](#requirements)
- [Improvements](#improvements)

## Description

API service to obtain data on the first 10 ads at the [link](https://www.farpost.ru/vladivostok/service/construction/guard/+/Video+surveillance+Systems/).

**Ad** required fields:

- id
- header
- author
- number of ad views;
- ad position.

API implementation requirements:

- [x] Python and the Django/FAST Api framework must be used during development.
- [x] A repository on GitHub must be provided as a result.
- [x] The service must use OOP principles.
- [x] A registration and login system.
- [x] All database calls must be implemented using ORM queries.

## Done

1. Implemented user registration and login system. Endpoints:
  
    - POST `/api/auth/signup` - user signup with email and password.
    - POST `/api/auth/login` - user login with email as username and password.
    - POST `/api/auth/logout` - user logout via `authorization` token.

    Additional:

    - GET `/api/users/me` - retrieve current user internal data.

2. Implemented ads selection functionality. Endpoints:

    - GET `/api/ads` - actual ads list order by position in source.
    - GET `/api/ads/{ad_id}` - retrieve actual ad by id.

3. Implemented Ads unloading from source.

    - created POST `/api/ads/` endpoint to run related celery task.
    - created `Celery` task that:
        - unloads data from [source](https://www.farpost.ru)
        - parsed fetched data
        - enters in into database.

4. Provided Docker for the application.
5. Added linters.

## Demonstration

For demonstration purposes, the file `dump.sql` was created.

You can push it into your database with command:

```bash
cat dump.sql | sqlite3 db.sqlite3
```

### Instances

Demo database contains:

- 1 user with credentials:

  ```console
  login: superuser@email.com
  password: verystrongpas
  ```

- 10 ads with demo data.

## Requirements

Project contains requirements/ folder with:

- `base.txt` with general application requirements
- `dev.txt` with linters
- `test.txt` with test libs

## Improvements

Improvements to be implemented in the future:

- [] Add use of environment variables.
- [] Fix the error when during web scraping the page returns 302 status code.
- [] Add use of PostgreSQL instead of SQLite.
- [] Add use of jwt tokens.
- [] Optimize unloading of current ads from the source.
