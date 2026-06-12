# Monitor Energético

Sistema completo de monitoramento de consumo energético de computadores utilizando Python e Django.

## 🎯 Objetivo

Desenvolver uma solução completa para monitoramento de consumo energético de computadores, permitindo coleta periódica de informações de hardware, cálculos de consumo energético e visualização através de uma interface web.

## 🏗️ Arquitetura

O sistema é composto por três módulos principais:

### API (Django REST)
- Autenticação JWT
- Gerenciamento de máquinas
- Recebimento e armazenamento de telemetrias
- Cálculos de consumo energético
- Endpoints RESTful

### Sistema Web
- Interface moderna e responsiva
- Dashboard com estatísticas
- Visualização de máquinas
- Configuração de parâmetros energéticos
- Gráficos com Chart.js

### Agente Linux
- Coleta automática de dados
- Fila local SQLite
- Envio periódico de telemetrias
- Integração como serviço systemd

## 📦 Tecnologias

- **Backend**: Python 3.12+, Django 5+, Django REST Framework
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT
- **Frontend**: Django Templates + Chart.js
- **Infraestrutura**: Docker, Docker Compose
- **Agente**: Python com psutil

## 🚀 Quick Start - Desenvolvimento

### Pré-requisitos
- Docker e Docker Compose instalados
- Python 3.12+ (para desenvolvimento local)

### Com Docker

```bash
# Crie arquivo .env baseado no exemplo
cp api/.env.example api/.env

# Inicie os serviços
docker-compose -f docker-compose.dev.yml up -d

# Acesse: http://localhost:8000
```

## 📡 Endpoints da API

### Autenticação
- `POST /api/autenticacao/cadastro` - Registrar novo usuário
- `POST /api/autenticacao/login` - Login (JWT)
- `POST /api/autenticacao/refresh` - Renovar token
- `GET /api/autenticacao/me` - Dados do usuário atual

### Máquinas
- `GET /api/maquinas` - Listar máquinas
- `POST /api/maquinas/registrar` - Registrar/atualizar máquina
- `GET /api/maquinas/{id}` - Detalhar máquina
- `PATCH /api/maquinas/{id}` - Atualizar máquina

### Telemetrias
- `POST /api/telemetrias/lote` - Enviar lote de telemetrias
- `GET /api/telemetrias` - Listar telemetrias
- `GET /api/telemetrias/historico` - Histórico com filtros

### Configurações Energéticas
- `GET /api/configuracoes-energeticas` - Listar configurações
- `POST /api/configuracoes-energeticas` - Criar configuração
- `PATCH /api/configuracoes-energeticas/{id}` - Atualizar configuração

## 🧪 Testes

```bash
cd api && python manage.py test
```

---

**Desenvolvido com ❤️ para monitoramento de energia eficiente**
