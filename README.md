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
    -v ~/alerte-blanche/alerte-blanche.db:/usr/src/app/alerte_blanche.db \
    --env-file gcm_key.env \
    -p 8080:5000 \
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

## Testing

To run the extensive test suite:

```bash
python3 -m unittest -v tests.py
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
     -d '{ "email": "individu@lambda.net",
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
     -d '{"number": "H20 HCL"}' \
     http://localhost:5000/license-plates
```


`/users/me` gets the authenticated user's profile:

```bash
curl -H 'Cookies: {{A valid session cookie}}' \
     http://localhost:5000/users/me
```

`/users/me/token` registers a device token for the authenticated user:

```bash
curl -X PUT \
     -H 'Cookies: {{A valid session cookie}}' \
     -H 'Content-Type: application/json' \
     -d '{"token": "thisismytokenandimproudofit"}' \
     http://localhost:5000/users/me/token
```

`/signal` signals a license plate to inform the car owner:

```bash
curl -X POST \
     -H 'Cookies: {{A valid session cookie}}' \
     -H 'Content-Type: application/json' \
     -d '{"plate_number": "H20 HCL"}' \
     http://localhost:5000/signal
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
