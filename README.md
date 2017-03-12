# Alerte Blanche API

API for the Alert Blanche application.

## Build

```bash
docker build -t alerte-blanche-api .
```

## Run

"Production" mode:

```bash
docker run -d \
    -p 5000:5000 \
    --name alerte-blanche \
    alerte-blanche-api
```

Development mode:

```bash
docker run -d \
    -p 5000:5000 \
    -e FLASK_DEBUG=1 \
    --name alerte-blanche \
    -v $PWD:/usr/src/app \
    alerte-blanche-api
```

## API

`/version` returns version information:

```bash
curl http://localhost:5000/version
```

`/users` registers a new user:

```bash
curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{ "email": "indidu@lambda.net",
           "first_name": "Tart",
           "last_name": "Empion",
           "plate_number": "H2O HCL",
           "telephone_number": "555-666-7777" }' \
     http://localhost:5000/users
```

`/license-plates` registers a license plate for the authenticated user:

```bash
curl -X POST \
     -H 'Cookies: {{A valid session cookie}}' \
     -H 'Content-Type: application/json' \
     -d '{ "number": "H20 HCL"}' \
     http://localhost:5000/license-plates
```

`/users/me/token` registers a device token for the authenticated user:

```bash
curl -X PUT \
     -H 'Cookies: {{A valid session cookie}}' \
     -H 'Content-Type: application/json' \
     -d '{ "token": "thisismytokenandimproudofit"}' \
     http://localhost:5000/users/me/token
```

`/login` creates a user session, and returns the user:

```bash
curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{"email": "individu@lambda.net","password": "fidelio"}' \
     http://localhost:5000/login
```

`/logout` deletes the user session:

```bash
curl -X POST http://localhost:5000/logout
```
