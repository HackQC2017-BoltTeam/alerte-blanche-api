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

`/login` creates a user session, and returns the user ID:

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
