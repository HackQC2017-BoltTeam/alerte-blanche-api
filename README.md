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
    alerte-blanche
```

Development mode:

```bash
docker run -d \
    -p 5000:5000 \
    -e FLASK_DEBUG=1 \
    --name alerte-blanche \
    -v $PWD:/usr/src/app \
    alerte-blanche
```

## API

`/version` returns version information:

```bash
curl http://localhost:5000/version
```
