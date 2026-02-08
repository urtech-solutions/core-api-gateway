# core-api-gateway

BFF em **Python/FastAPI** com autenticação JWT simples e rotas de proxy para serviços core.

## Imagem Docker no GHCR

A imagem publicada automaticamente pelo GitHub Actions fica em:

- `ghcr.io/<owner>/<repo>:main`

Exemplo para este repositório:

- `ghcr.io/${GITHUB_REPOSITORY}:main`

## Funcionalidades

- Middleware JWT com chave simétrica (`JWT_SECRET`) para endpoints protegidos.
- Endpoints:
  - `GET /healthz`
  - `POST /auth/login` (mock, retorna token)
  - `GET /me`
- Proxy usando `httpx`:
  - `/devices*` -> `DEVICE_REGISTRY_URL`
  - `/status*` -> `TELEMETRY_API_URL`
  - `/telemetry*` -> `TELEMETRY_API_URL`

## Variáveis de ambiente necessárias

- `DEVICE_REGISTRY_URL` (default: `http://localhost:8001`)
- `TELEMETRY_API_URL` (default: `http://localhost:8002`)
- `JWT_SECRET` (default: `change-me`)

> Para ambiente de produção, defina explicitamente as 3 variáveis acima (especialmente `JWT_SECRET`).

## Executar localmente

```bash
make install-dev
make run
```

## Testes e lint

```bash
make lint
make test
```

## Docker

```bash
make build-docker
docker run --rm -p 8000:8000 \
  -e DEVICE_REGISTRY_URL=http://host.docker.internal:8001 \
  -e TELEMETRY_API_URL=http://host.docker.internal:8002 \
  -e JWT_SECRET=super-secret \
  core-api-gateway:latest
```

## Exemplo de login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H 'content-type: application/json' \
  -d '{"username":"admin","password":"123"}'
```
