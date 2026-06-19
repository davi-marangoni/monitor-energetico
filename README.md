# Monitor Energético

Sistema de monitoramento de consumo energético de computadores utilizando Python e Django.

## Objetivo

Coletar telemetria de hardware (CPU e RAM), calcular consumo energético estimado e exibir os dados em uma interface web com dashboard e gráficos.

## Arquitetura

O projeto é composto por três módulos:

| Módulo | Diretório | Descrição |
|--------|-----------|-----------|
| API + Web | `api/` | Django REST + templates do `sistema_web/` |
| Frontend | `sistema_web/` | Templates HTML, CSS e JavaScript (Chart.js) |
| Agente | `agente/` | Coleta local e envio de telemetrias via API |

### API (Django REST)
- Autenticação JWT
- CRUD de máquinas, telemetrias e configurações energéticas
- Cálculo de consumo via `ServicoCalculoEnergetico`
- Endpoints de dashboard (resumo, ranking, consumo geral)

### Sistema Web
- Interface integrada ao Django (`aplicativos.interface_web`)
- Autenticação híbrida: sessão Django para páginas + JWT para gráficos (Chart.js)
- Dashboard, listagem de máquinas, detalhe, configuração energética, perfil

### Agente Linux
- Coleta CPU/RAM com `psutil`
- Fila local SQLite para retry
- Registro da máquina e envio periódico de telemetrias à API

## Tecnologias

- Python 3.12+, Django 5.0, Django REST Framework
- PostgreSQL
- JWT (SimpleJWT) + sessão Django
- Django Templates + Chart.js
- Docker, Docker Compose
- Agente: psutil, requests

## Estrutura do repositório

```
python-django/
├── api/                 # Django (API REST + app interface_web)
├── agente/              # Agente de coleta
├── sistema_web/       # templates/ e static/
├── docker/              # Dockerfile e nginx (prod)
├── docker-compose.dev.yml
└── docker-compose.prod.yml
```

## Quick Start — Desenvolvimento

### Pré-requisitos
- Docker e Docker Compose
- Python 3.12+ (para rodar o agente localmente)

### 1. Subir API + banco + frontend

```bash
cp api/.env.example api/.env

docker compose -f docker-compose.dev.yml up -d
```

Acesse: http://localhost:8000

- Cadastro: http://localhost:8000/cadastro
- Login: http://localhost:8000/login

As migrations rodam automaticamente na subida do container.

### 2. Configurar e rodar o agente

Na máquina que será monitorada:

```bash
cd agente
cp .env.example .env
pip install -r requirements.txt
python3 main.py
```

Configure no `.env`:

```env
API_URL=http://localhost:8000/api
API_USERNAME=seu_usuario
API_PASSWORD=sua_senha
```

Use o **mesmo usuário** criado no cadastro web. O agente faz login automaticamente e obtém o JWT.

Para desenvolvimento local, ajuste também:

```env
FILA_DB_PATH=./fila.db
LOG_PATH=./logs
```

> **Importante:** endpoints POST da API exigem barra final (`/`). O agente já usa URLs corretas (`/maquinas/registrar/`, `/telemetrias/lote/`).

## Rotas Web

| Rota | Descrição |
|------|-----------|
| `/` | Dashboard |
| `/login` | Login |
| `/logout` | Logout (POST) |
| `/cadastro` | Criar conta |
| `/maquinas` | Listar máquinas |
| `/maquinas/{id}/` | Detalhe da máquina |
| `/maquinas/{id}/editar` | Editar máquina |
| `/maquinas/{id}/configuracao` | Configuração energética |
| `/configuracoes` | Todas as configurações |
| `/perfil` | Perfil do usuário |

## Endpoints da API

Base: `http://localhost:8000/api`

### Autenticação
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/autenticacao/cadastro` | Registrar usuário |
| POST | `/autenticacao/login` | Obter JWT (`access` + `refresh`) |
| POST | `/autenticacao/refresh` | Renovar token |
| GET | `/autenticacao/me` | Dados do usuário logado |

### Máquinas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/maquinas/` | Listar máquinas (filtro: `?machine_id_linux=`) |
| POST | `/maquinas/registrar/` | Registrar/atualizar via agente |
| GET | `/maquinas/{id}/` | Detalhar |
| PATCH | `/maquinas/{id}/` | Atualizar |

### Telemetrias
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/telemetrias/lote/` | Enviar lote (agente) |
| GET | `/telemetrias/` | Listar |
| GET | `/telemetrias/historico/` | Histórico com consumo calculado |

Query params de `historico/`: `filtro` (`ultima_hora`, `ultimas_24_horas`, `ultimos_7_dias`, `ultimos_30_dias`, `personalizado`), `maquina_id`, `data_inicio`, `data_fim`.

### Configurações energéticas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/configuracoes-energeticas/` | Listar |
| POST | `/configuracoes-energeticas/` | Criar |
| PATCH | `/configuracoes-energeticas/{id}/` | Atualizar |

### Dashboard
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/dashboard/resumo/` | Máquinas online/offline, consumo atual e médio |
| GET | `/dashboard/ranking/` | Top 5 e ranking completo |
| GET | `/dashboard/consumo-geral/` | Série temporal de consumo (`?filtro=`) |

## Testes

```bash
# Local (com PostgreSQL configurado)
cd api && python manage.py test

# Via Docker
docker compose -f docker-compose.dev.yml run --rm --no-deps api python manage.py test
```

## Produção

```bash
docker compose -f docker-compose.prod.yml up -d
```

Configure variáveis de ambiente (`.env`) com `SECRET_KEY` segura (mínimo 32 caracteres), credenciais do banco e `ALLOWED_HOSTS`. O build inclui `sistema_web/` na imagem da API; o nginx serve arquivos estáticos.

## Fórmulas de consumo

- `Consumo_CPU = TDP × (α + (1 − α) × Uso_CPU / 100)`
- `Consumo_RAM = RAM_Utilizada × Consumo_Por_GB`
- `Consumo_Total = Consumo_CPU + Consumo_RAM`

Parâmetros configuráveis por máquina em `/maquinas/{id}/configuracao`.
