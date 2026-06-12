# Monitoramento Energético com Python e Django

## Estrutura

- `api/`: API Django + DRF + JWT
- `sistema_web/`: templates e estáticos da interface web
- `agente/`: agente Linux para coleta/envio de telemetrias
- `docker-compose.dev.yml`: ambiente de desenvolvimento
- `docker-compose.prod.yml`: ambiente de produção

## API (endpoints)

- `POST /api/autenticacao/cadastro`
- `POST /api/autenticacao/login`
- `POST /api/autenticacao/refresh`
- `GET /api/autenticacao/me`
- `GET /api/maquinas`
- `POST /api/maquinas/registrar`
- `GET /api/maquinas/{id}`
- `PATCH /api/maquinas/{id}`
- `POST /api/telemetrias/lote`
- `GET /api/telemetrias`
- `GET /api/telemetrias/historico`
- `GET/POST /api/configuracoes-energeticas`
- `PATCH /api/configuracoes-energeticas/{id}`

## Desenvolvimento local

```bash
docker compose -f docker-compose.dev.yml up --build
```

## Testes

```bash
cd api
python manage.py test
```
