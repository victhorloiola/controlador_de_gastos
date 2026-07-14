# API de Controle de Gastos Pessoais

API REST para registrar receitas e despesas pessoais, organizadas por categoria.

O projeto foi feito com foco em aprender uma base real de back-end usando
FastAPI, SQLAlchemy, Pydantic, SQLite e testes automatizados.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Pytest

## Funcionalidades

- Criar e listar categorias
- Criar, listar, buscar, atualizar e remover transacoes
- Filtrar transacoes por categoria, tipo e intervalo de datas
- Consultar resumo mensal
- Consultar resumo por categoria
- Rodar testes automatizados

## Como rodar o projeto

Clone o repositorio:

```powershell
git clone https://github.com/victhorliola/controlador_de_gastos.git
cd controlador_de_gastos
```

Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Inicie a API:

```powershell
uvicorn app.main:app --reload
```

Acesse a documentacao interativa:

```txt
http://127.0.0.1:8000/docs
```

## Endpoints

### Categorias

| Metodo | Rota | Descricao |
| --- | --- | --- |
| POST | `/categories` | Cria uma categoria |
| GET | `/categories` | Lista categorias |

### Transacoes

| Metodo | Rota | Descricao |
| --- | --- | --- |
| POST | `/transactions` | Cria uma transacao |
| GET | `/transactions` | Lista transacoes |
| GET | `/transactions/{id}` | Busca uma transacao |
| PUT | `/transactions/{id}` | Atualiza uma transacao |
| DELETE | `/transactions/{id}` | Remove uma transacao |

Filtros em `GET /transactions`:

```txt
?category_id=1
?type=income
?type=expense
?start_date=2026-07-01&end_date=2026-07-31
```

### Resumos

| Metodo | Rota | Descricao |
| --- | --- | --- |
| GET | `/summary/monthly` | Total de receitas, despesas e saldo por mes |
| GET | `/summary/category` | Total por categoria |

## Exemplos

Criar categoria:

```json
{
  "name": "Alimentacao",
  "type": "expense"
}
```

Criar transacao:

```json
{
  "description": "Mercado",
  "amount": "120.50",
  "date": "2026-07-10",
  "type": "expense",
  "category_id": 1
}
```

Resumo mensal:

```json
[
  {
    "month": "2026-07",
    "income": "3000.00",
    "expense": "450.00",
    "balance": "2550.00"
  }
]
```

## Testes

Rode:

```powershell
python -m pytest
```

Os testes usam um banco SQLite em memoria para nao misturar dados de teste com
o banco local de desenvolvimento.

## Deploy

O projeto esta preparado para deploy no Render usando o arquivo `render.yaml`.

Configuracao usada:

```txt
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Depois do deploy, a documentacao da API fica disponivel em:

```txt
https://seu-link-do-render.onrender.com/docs
```

## O que aprendi

- Estruturar uma API com FastAPI
- Separar models, schemas, routers e funcoes CRUD
- Validar dados com Pydantic
- Persistir dados com SQLAlchemy e SQLite
- Criar filtros usando query parameters
- Gerar resumos usando agregacoes
- Escrever testes automatizados com Pytest

## Proximas melhorias

- Adicionar autenticacao de usuarios
- Impedir categorias duplicadas
- Adicionar paginacao em transacoes
- Criar filtro por mes
